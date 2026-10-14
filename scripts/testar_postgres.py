"""Integração com PostgreSQL descartável e TLS verificado (Docker + OpenSSL)."""
import json
import secrets
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from sqlalchemy import text
from sqlalchemy.engine import URL
import psycopg
from rota.storage import PostgresStore, StorageError

IMAGE='postgres:17-alpine@sha256:b0f9560a2de083e2cc7382e75f808c7381a32852a7ec49117deedb300e552b24'


def run(*args):
    return subprocess.run(args,check=True,capture_output=True,text=True).stdout.strip()


def ready(name):
    for _ in range(60):
        p=subprocess.run(['docker','exec',name,'pg_isready','-h','127.0.0.1','-U','postgres'],capture_output=True)
        if p.returncode==0:return
        time.sleep(.5)
    raise RuntimeError('PostgreSQL de teste não iniciou.')


def main():
    name='rota-test-'+secrets.token_hex(6)
    with tempfile.TemporaryDirectory(prefix='rota-pg-') as d:
        root=Path(d)
        password=secrets.token_urlsafe(24)
        (root/'db.env').write_text('POSTGRES_PASSWORD='+password+'\n')
        (root/'db.env').chmod(0o600)
        for label in ('server','untrusted'):
            run('openssl','req','-x509','-newkey','rsa:2048','-nodes','-days','1',
                '-subj','/CN=localhost','-addext','subjectAltName=DNS:localhost,IP:127.0.0.1',
                '-keyout',str(root/(label+'.key')),'-out',str(root/(label+'.crt')))
        started=False;store=None
        try:
            run('docker','run','--detach','--name',name,'--env-file',str(root/'db.env'),
                '-p','127.0.0.1::5432','-v',str(root)+':/tls:ro','--entrypoint','sh',IMAGE,'-c',
                'cp /tls/server.crt /tmp/rota.crt && cp /tls/server.key /tmp/rota.key && '
                'chown postgres:postgres /tmp/rota.crt /tmp/rota.key && chmod 600 /tmp/rota.key && '
                'exec docker-entrypoint.sh postgres -c ssl=on -c ssl_cert_file=/tmp/rota.crt -c ssl_key_file=/tmp/rota.key')
            started=True;ready(name)
            port=json.loads(run('docker','inspect',name))[0]['NetworkSettings']['Ports']['5432/tcp'][0]['HostPort']
            def url(ca):
                return URL.create('postgresql+psycopg',username='postgres',password=password,
                    host='127.0.0.1',port=int(port),database='postgres',
                    query={'sslmode':'verify-full','sslrootcert':str(root/ca)}).render_as_string(hide_password=False)
            try:psycopg.connect(url('untrusted.crt').replace('postgresql+psycopg://','postgresql://'))
            except psycopg.OperationalError as e:assert 'certificate verify failed' in str(e)
            else:raise AssertionError('CA não confiável foi aceita.')
            try:PostgresStore(url('untrusted.crt'))
            except StorageError as e:
                assert password not in str(e)
            else:raise AssertionError('CA não confiável foi aceita.')
            store=PostgresStore(url('server.crt'))
            payload={'id':'fixture-sintetica','criada':'2026-01-01T00:00:00Z','status':'Concluída',
                     'registros':[{'teste':'çã','origem':[None,1]}],'complementos':[]}
            store.salvar(payload)
            payload['status']='Revisão pendente';store.salvar(payload)
            assert len(store.listar())==1
            assert store.obter(payload['id'])==payload
            assert store.obter("'; DROP TABLE consultas; --") is None
            def complementar(i):return store.complementar(payload['id'],{'fornecedor':'TESTE','sha256_arquivo':str(i)})
            with ThreadPoolExecutor(max_workers=4) as pool:assert all(new for _,new in pool.map(complementar,range(4)))
            payload=store.obter(payload['id'])
            assert len(payload['complementos'])==4
            assert store.complementar(payload['id'],payload['complementos'][0])[1] is False
            with store.engine.connect() as c:
                assert c.execute(text('SELECT ssl FROM pg_stat_ssl WHERE pid=pg_backend_pid()')).scalar() is True
            store.close();store=None
            run('docker','restart',name);ready(name)
            port=json.loads(run('docker','inspect',name))[0]['NetworkSettings']['Ports']['5432/tcp'][0]['HostPort']
            store=PostgresStore(url('server.crt'))
            assert store.obter(payload['id'])==payload
            print('PostgreSQL 17: TLS verificado, CA incorreta rejeitada, JSON intacto, upsert, importações concorrentes e persistência após reinício aprovados. Dados sintéticos.')
        finally:
            if store:store.close()
            if started:run('docker','rm','--force','--volumes',name)


if __name__=='__main__':main()
