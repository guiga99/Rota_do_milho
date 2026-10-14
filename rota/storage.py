"""Persistência externa para o piloto, sem fallback silencioso para disco local."""
import json
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import SQLAlchemyError

from .core import Store, conservar_anotacoes


class StorageError(RuntimeError):
    pass


class PostgresStore:
    def __init__(self, url):
        try:
            parsed = make_url(url)
        except Exception:
            raise StorageError('Configuração do PostgreSQL inválida.') from None
        if parsed.drivername not in ('postgresql', 'postgresql+psycopg'):
            raise StorageError('O histórico externo requer PostgreSQL.')
        if parsed.query.get('sslmode') != 'verify-full' or not parsed.query.get('sslrootcert'):
            raise StorageError('Configure PostgreSQL com sslmode=verify-full e sslrootcert (system ou CA do provedor).')
        self.engine = create_engine(parsed.set(drivername='postgresql+psycopg'),
                                    pool_pre_ping=True, pool_size=2, max_overflow=2,
                                    hide_parameters=True, connect_args={'connect_timeout':10})
        try:
            with self.engine.begin() as c:
                c.execute(text('CREATE TABLE IF NOT EXISTS consultas (id TEXT PRIMARY KEY, criada TEXT, status TEXT, payload TEXT)'))
        except SQLAlchemyError:
            self.engine.dispose()
            raise StorageError('Não foi possível conectar ou preparar o histórico PostgreSQL. Verifique rede, CA e permissões na configuração privada.') from None

    def _execute(self, statement, params=None, fetch=False):
        try:
            with self.engine.begin() as c:
                rows = c.execute(text(statement), params or {})
                return rows.fetchall() if fetch else None
        except SQLAlchemyError:
            raise StorageError('Falha no histórico PostgreSQL. A consulta não foi persistida; verifique a conexão antes de continuar.') from None

    def salvar(self, result):
        try:
            with self.engine.begin() as c:
                row=c.execute(text('SELECT payload FROM consultas WHERE id=:id FOR UPDATE'),{'id':result['id']}).fetchone()
                payload=conservar_anotacoes(result,json.loads(row[0]) if row else {})
                c.execute(text('INSERT INTO consultas (id,criada,status,payload) VALUES (:id,:criada,:status,:payload) '
                          'ON CONFLICT(id) DO UPDATE SET criada=excluded.criada,status=excluded.status,payload=excluded.payload'),
                          {'id':result['id'],'criada':result['criada'],'status':result['status'],'payload':json.dumps(payload,ensure_ascii=False)})
        except SQLAlchemyError:
            raise StorageError('Não foi possível salvar a consulta no PostgreSQL. Verifique a conexão antes de continuar.') from None

    def listar(self):
        return self._execute('SELECT id,criada,status FROM consultas ORDER BY criada DESC', fetch=True)

    def obter(self, id):
        rows = self._execute('SELECT payload FROM consultas WHERE id=:id', {'id':id}, fetch=True)
        return json.loads(rows[0][0]) if rows else None

    def complementar(self, id, complemento):
        try:
            with self.engine.begin() as c:
                row=c.execute(text('SELECT payload FROM consultas WHERE id=:id FOR UPDATE'),{'id':id}).fetchone()
                if not row:raise ValueError('Consulta não encontrada no histórico.')
                result=json.loads(row[0]);existing=result.get('complementos',[])
                if any(x['sha256_arquivo']==complemento['sha256_arquivo'] and x['fornecedor']==complemento['fornecedor'] for x in existing):return result,False
                result['complementos']=[*existing,complemento]
                c.execute(text('UPDATE consultas SET payload=:payload WHERE id=:id'),{'payload':json.dumps(result,ensure_ascii=False),'id':id})
                return result,True
        except SQLAlchemyError:
            raise StorageError('Não foi possível persistir a complementação. Verifique a conexão antes de continuar.') from None

    def close(self):
        self.engine.dispose()

    def revisar(self,id,**kwargs):
        from .reviews import registrar
        try:
            with self.engine.begin() as c:
                row=c.execute(text('SELECT payload FROM consultas WHERE id=:id FOR UPDATE'),{'id':id}).fetchone()
                if not row:raise ValueError('Consulta não encontrada no histórico.')
                result=registrar(json.loads(row[0]),**kwargs)
                c.execute(text('UPDATE consultas SET payload=:payload WHERE id=:id'),{'id':id,'payload':json.dumps(result,ensure_ascii=False)})
                return result
        except SQLAlchemyError:
            raise StorageError('Não foi possível salvar a revisão. Verifique a conexão antes de continuar.') from None


def criar_store(settings, data_dir, cloud=False):
    database = settings.get('database', {})
    url = database.get('url')
    if url:
        return PostgresStore(url)
    if cloud:
        raise StorageError('Configure database.url nos Secrets do Streamlit Cloud. O piloto online requer histórico PostgreSQL persistente.')
    return Store(Path(data_dir)/'consultas.sqlite3')
