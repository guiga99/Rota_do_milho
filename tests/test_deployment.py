import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
from rota.deployment import validar, testar_banco
from scripts.verificar_streamlit import main


def config():
    return {'access':{'mode':'google','allowed_emails':['admin@example.net','colega@example.net'],'admin_emails':['admin@example.net']},
            'auth':{'redirect_uri':'https://fixture-undeployed.streamlit.app/oauth2callback','cookie_secret':'a'*48,
                    'google':{'client_id':'123-fixture.apps.googleusercontent.com','client_secret':'FAKE_SECRET_TEST',
                              'server_metadata_url':'https://accounts.google.com/.well-known/openid-configuration'}},
            'database':{'url':'postgresql://test:FAKE_SECRET_TEST@db.example.net/test?sslmode=verify-full&sslrootcert=system'},
            'datajud':{'api_key':'FAKE_SECRET_TEST'}}


class DeploymentTests(unittest.TestCase):
    def test_valid_structure_callback_exact_and_no_network(self):
        with patch('psycopg.connect') as connect:
            self.assertEqual(validar(config(),'https://fixture-undeployed.streamlit.app'),[])
            self.assertTrue(validar(config(),'https://outra.streamlit.app'))
            connect.assert_not_called()

    def test_placeholder_model_and_missing_fields_rejected(self):
        import tomllib
        example=Path(__file__).parents[1]/'.streamlit/secrets.cloud.example.toml'
        self.assertTrue(validar(tomllib.loads(example.read_text())))
        for field in ('access','auth','database','datajud'):
            c=config();c[field]={};self.assertTrue(validar(c))

    def test_private_callback_weak_cookie_and_outside_admin_rejected(self):
        for change in ['callback','cookie','admin','tls','url']:
            c=config()
            if change=='callback':c['auth']['redirect_uri']='http://localhost:8501/oauth2callback'
            if change=='cookie':c['auth']['cookie_secret']='tiny'
            if change=='admin':c['access']['admin_emails']=['outside@example.net']
            if change=='tls':c['database']['url']=c['database']['url'].replace('verify-full','require')
            if change=='url':c['database']['url']='FAKE_SECRET_TEST_INVALID'
            errors=validar(c);self.assertTrue(errors);self.assertNotIn('FAKE_SECRET_TEST',' '.join(errors))

    def test_cli_errors_never_echo_invalid_secrets(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'secrets.toml';p.write_text('invalid = "FAKE_SECRET_TEST" trailing invalid')
            buf=io.StringIO()
            with redirect_stdout(buf):code=main(['--config',str(p)])
            self.assertEqual(code,2);self.assertNotIn('FAKE_SECRET_TEST',buf.getvalue())

    def test_database_failure_is_sanitized(self):
        with patch('psycopg.connect',side_effect=RuntimeError('FAKE_SECRET_TEST')):
            ok,message=testar_banco(config()['database']['url'])
        self.assertFalse(ok);self.assertNotIn('FAKE_SECRET_TEST',message)

    def test_database_readonly_and_unverified_tls_rejected_before_connection(self):
        with patch('psycopg.connect') as connect:
            ok,_=testar_banco(config()['database']['url'].replace('verify-full','require'))
            self.assertFalse(ok);connect.assert_not_called()
            c=connect.return_value.__enter__.return_value
            c.execute.return_value.fetchone.side_effect=[(1,),(True,),(True,)]
            ok,_=testar_banco(config()['database']['url']);self.assertTrue(ok)
            queries=[call.args[0] for call in c.execute.call_args_list]
            self.assertEqual(queries[0],'SET TRANSACTION READ ONLY')
            self.assertTrue(all(q.startswith('SELECT') for q in queries[1:]))
