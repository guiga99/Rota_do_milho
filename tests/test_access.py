import os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
from rota.access import autorizar

class AccessTests(unittest.TestCase):
    def test_verified_google_and_exact_allowlist(self):
        claims={'iss':'https://accounts.google.com','email':' ADMIN@EXAMPLE.COM ','email_verified':True,'exp':200}
        self.assertEqual(autorizar(claims,['admin@example.com'],['admin@example.com'],100)['role'],'admin')
        self.assertEqual(autorizar(claims,['admin@example.com'],[],100)['role'],'operator')
        self.assertIsNone(autorizar(claims,['other@example.com'],[],100))
        for change in [{'email_verified':False},{'email_verified':'true'},{'iss':'https://evil.example'},{'email':'admin@example.com.evil'},{'exp':99},{'exp':True}]:
            self.assertIsNone(autorizar({**claims,**change},['admin@example.com'],['admin@example.com'],100))
    def test_google_missing_config_stops_before_database(self):
        with tempfile.TemporaryDirectory() as d,patch.dict(os.environ,{'ROTA_DATA_DIR':d,'ROTA_AUTH_MODE':'google'}):
            app=AppTest.from_file(str(Path(__file__).parents[1]/'app.py')).run()
            self.assertEqual(len(app.exception),0)
            self.assertIn('Login Google ainda não configurado',app.error[0].value)
            self.assertFalse((Path(d)/'consultas.sqlite3').exists())
            self.assertEqual(len(app.tabs),0)
    def test_operator_cannot_see_integration_key(self):
        with tempfile.TemporaryDirectory() as d,patch.dict(os.environ,{'ROTA_DATA_DIR':d,'DATAJUD_API_KEY':'secret-value'}),patch('rota.access.proteger',return_value={'email':'operator@example.com','role':'operator','mode':'google'}):
            app=AppTest.from_file(str(Path(__file__).parents[1]/'app.py')).run()
            self.assertEqual(len(app.exception),0)
            self.assertEqual(len(app.text_input),0)
            self.assertEqual(len(app.tabs),4)
            self.assertNotIn('secret-value',' '.join(x.value for x in app.markdown))

    def test_local_mode_cannot_bind_public_interface(self):
        from rota.access import proteger
        class Screen:
            def get_option(self,key):return '0.0.0.0'
            def error(self,message):self.message=message
            def stop(self):raise RuntimeError('stopped')
        screen=Screen()
        with self.assertRaises(RuntimeError):proteger(screen,'local',{})
        self.assertIn('loopback',screen.message)
