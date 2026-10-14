import os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from streamlit.testing.v1 import AppTest

class InterfaceTests(unittest.TestCase):
    def test_configuracao_e_erro_sem_chave(self):
        import streamlit as st
        original_get_option=st.get_option
        with tempfile.TemporaryDirectory() as d,patch.dict(os.environ,{'ROTA_DATA_DIR':d,'DATAJUD_API_KEY':''}),patch('streamlit.get_option',side_effect=lambda key:'127.0.0.1' if key=='server.address' else original_get_option(key)):
            app=AppTest.from_file(str(Path(__file__).parents[1]/'app.py')).run()
            self.assertEqual(len(app.exception),0)
            from rota.fields import periodo_cinco_anos
            inicio,fim=periodo_cinco_anos()
            self.assertTrue(app.checkbox[0].value)
            self.assertEqual(app.date_input[0].value,inicio)
            self.assertEqual(app.date_input[1].value,fim)
            self.assertEqual([t.label for t in app.tabs],['Configurações','Pesquisa','Resultados','Histórico'])
            app.button[1].click().run()
            self.assertIn('Configure a chave',app.error[0].value)
            app.text_input[0].set_value('chave-apenas-para-teste');app.button[0].click().run()
            self.assertEqual(app.session_state['api_key'],'chave-apenas-para-teste')
            self.assertEqual(len(app.exception),0)
