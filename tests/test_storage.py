import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
from rota.storage import criar_store, PostgresStore, StorageError


class StorageTests(unittest.TestCase):
    def test_cloud_has_no_local_fallback(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(StorageError):criar_store({},d,cloud=True)
            self.assertEqual(list(Path(d).iterdir()),[])
            local=criar_store({},d)
            local.salvar({'id':'teste','criada':'2026-01-01','status':'Concluída','evidencia':{'original':[1,None]}})
            self.assertEqual(local.obter('teste')['evidencia']['original'],[1,None])
            c={'fornecedor':'TESTE','sha256_arquivo':'hash-sintetico'}
            self.assertTrue(local.complementar('teste',c)[1])
            self.assertFalse(local.complementar('teste',c)[1])
            self.assertEqual(len(local.obter('teste')['complementos']),1)
            self.assertEqual(local.obter('teste')['evidencia']['original'],[1,None])

    def test_postgres_rejects_unverified_tls_and_wrong_driver(self):
        for url in ('sqlite:///test.db','postgresql://user:SECRET@host/db',
                    'postgresql://user:SECRET@host/db?sslmode=require&sslrootcert=system',
                    'postgresql://user:SECRET@host/db?sslmode=verify-full'):
            with self.assertRaises(StorageError) as e:PostgresStore(url)
            self.assertNotIn('SECRET',str(e.exception))

    def test_cloud_forces_google_even_when_local_configured(self):
        from rota.access import proteger
        modes=[]
        def gate(st,mode,settings):
            modes.append(mode)
            return proteger(st,mode,{})
        with patch('rota.access.proteger',side_effect=gate):
            app=AppTest.from_file(str(Path(__file__).parents[1]/'cloud_app.py')).run()
        self.assertEqual(modes,['google'])
        self.assertEqual(len(app.exception),0)
        self.assertEqual(len(app.tabs),0)

    def test_cloud_stops_when_authenticated_but_missing_database(self):
        identity={'email':'admin@example.com','role':'admin','mode':'google'}
        with patch('rota.access.proteger',return_value=identity):
            app=AppTest.from_file(str(Path(__file__).parents[1]/'cloud_app.py')).run()
        self.assertEqual(len(app.exception),0)
        self.assertIn('database.url',app.error[0].value)
        self.assertEqual(len(app.tabs),0)
