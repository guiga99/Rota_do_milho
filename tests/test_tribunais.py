import tempfile,unittest,io
from pathlib import Path
import httpx
from openpyxl import load_workbook
from rota.core import DataJud,Store,coletar,ConsultaError,TRIBUNAIS
from rota.export import exportar
from test_mvp import source,response

class TribunalTests(unittest.TestCase):
    def test_tjsc_query_and_provenance(self):
        s=source();s['tribunal']='TJSC';s['assuntos']=[]
        requests=[]
        def request(req):requests.append(req);return httpx.Response(200,json=response([s]))
        api=DataJud('key',httpx.MockTransport(request),tribunal='TJSC')
        with tempfile.TemporaryDirectory() as d:
            r=coletar(api,Store(Path(d)/'db'),[],limite=1,numero=s['numeroProcesso'])
            self.assertIsNone(r['erro']);self.assertEqual(r['tribunal'],'TJSC')
            self.assertEqual(str(requests[0].url),TRIBUNAIS['TJSC'])
            w=load_workbook(io.BytesIO(exportar(r)))
            self.assertEqual(w['FONTES']['B2'].value,TRIBUNAIS['TJSC'])
        api.close()
    def test_reject_wrong_tribunal_or_cnj(self):
        s=source()
        api=DataJud('key',httpx.MockTransport(lambda req:httpx.Response(200,json=response([s]))),tribunal='TJSC')
        with self.assertRaises(ConsultaError):api.teste()
        api.close()
        s2=source(2)
        api=DataJud('key',httpx.MockTransport(lambda req:httpx.Response(200,json=response([s2]))))
        with tempfile.TemporaryDirectory() as d:
            r=coletar(api,Store(Path(d)/'db'),[],limite=1,numero=s['numeroProcesso'])
            self.assertIsNotNone(r['erro']);self.assertEqual(r['cnjs_unicos'],0)
        api.close()
