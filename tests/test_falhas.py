import tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import httpx
from rota.core import ConsultaError,DataJud,Store,coletar
from test_mvp import response,source

class FailureTests(unittest.TestCase):
    @patch('rota.core.time.sleep')
    def test_retry_limitado(self,sleep):
        count=0
        def request(req):
            nonlocal count
            count+=1
            return httpx.Response(429,headers={'Retry-After':'120'})
        api=DataJud('key',httpx.MockTransport(request))
        with self.assertRaises(ConsultaError):api.teste()
        self.assertEqual(count,3);self.assertEqual(sleep.call_count,2)
        self.assertEqual(sleep.call_args.args[0],10);api.close()
    def test_timeout(self):
        def request(req):raise httpx.ReadTimeout('key',request=req)
        api=DataJud('key',httpx.MockTransport(request))
        with self.assertRaises(ConsultaError) as e:api.teste()
        self.assertNotIn('key',str(e.exception));api.close()
    def test_cursor_repetido(self):
        api=DataJud('key',httpx.MockTransport(lambda req:httpx.Response(200,json=response([source(),source(1,'G2')]))))
        with tempfile.TemporaryDirectory() as d:
            r=coletar(api,Store(Path(d)/'db'),[6060],2)
            self.assertEqual(r['status'],'Parcial');self.assertIn('cursor',r['erro'])
        api.close()
    def test_paginacao_completa(self):
        queries=[]
        def request(req):
            import json
            queries.append(json.loads(req.content))
            return httpx.Response(200,json=response([source(),source(),source(2)]) if len(queries)==1 else response([source(3)]))
        api=DataJud('key',httpx.MockTransport(request))
        with tempfile.TemporaryDirectory() as d:
            r=coletar(api,Store(Path(d)/'db'),[6060],3)
            self.assertEqual(r['cnjs_unicos'],3);self.assertEqual(r['duplicados'],1)
            self.assertEqual(len(r['paginas']),2);self.assertEqual(queries[1]['search_after'],['20260101120000','r2-G1'])
            self.assertEqual(r['status'],'Limite de amostra atingido')
        api.close()
    def test_shard_failure(self):
        payload=response([]);payload['_shards']={'failed':1}
        api=DataJud('key',httpx.MockTransport(lambda req:httpx.Response(200,json=payload)))
        with self.assertRaises(ConsultaError):api.teste()
        api.close()
