"""Pré-validação da configuração Cloud, sem exibir valores privados."""
import re
from urllib.parse import urlsplit
from sqlalchemy.engine import make_url
from .access import GOOGLE_METADATA, emails


def preenchido(value):
    return isinstance(value,str) and bool(value.strip()) and not any(
        word in value.upper() for word in ('SUBSTITUIR','SEU_','SUA_','PREENCHER','GERAR_'))


def url_aplicacao(value):
    try:
        u=urlsplit(value)
        if u.scheme!='https' or not u.hostname or u.username or u.password or u.query or u.fragment or u.path not in ('','/') or u.port not in (None,443):
            return None
        if u.hostname in ('localhost','127.0.0.1','::1') or not preenchido(u.hostname):return None
        return value.rstrip('/')
    except (ValueError,TypeError):return None


def validar(settings,app_url=None):
    errors=[]
    def section(name):
        v=settings.get(name,{})
        return v if isinstance(v,dict) else {}
    access=section('access');auth=section('auth');database=section('database');datajud=section('datajud')
    google=auth.get('google',{})
    if not isinstance(google,dict):google={}
    if access.get('mode')!='google':errors.append('access.mode: use google para a equipe.')
    def addresses(value):
        return emails(value) if isinstance(value,(str,list,tuple)) else frozenset()
    allowed=addresses(access.get('allowed_emails'));admins=addresses(access.get('admin_emails'))
    if not allowed or not all(re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+',x) for x in allowed):errors.append('access.allowed_emails: informe contas válidas autorizadas.')
    if not admins or not admins<=allowed:errors.append('access.admin_emails: informe administradores também presentes na lista autorizada.')
    if not preenchido(auth.get('cookie_secret')) or len(str(auth.get('cookie_secret','')))<32:errors.append('auth.cookie_secret: gere um segredo aleatório de pelo menos 32 caracteres.')
    if not preenchido(google.get('client_id')) or not str(google.get('client_id','')).endswith('.apps.googleusercontent.com'):errors.append('auth.google.client_id: configure o cliente OAuth web real.')
    if not preenchido(google.get('client_secret')):errors.append('auth.google.client_secret: configure o segredo OAuth privado.')
    if google.get('server_metadata_url')!=GOOGLE_METADATA:errors.append('auth.google.server_metadata_url: use a descoberta oficial Google.')
    redirect=auth.get('redirect_uri','')
    try:
        u=urlsplit(redirect)
        base=url_aplicacao(f'{u.scheme}://{u.netloc}')
        valid=bool(base and u.path=='/oauth2callback' and not u.query and not u.fragment)
    except (ValueError,TypeError):valid=False
    if not valid:errors.append('auth.redirect_uri: use a URL HTTPS real seguida de /oauth2callback.')
    if app_url is not None:
        expected=url_aplicacao(app_url)
        if not expected:errors.append('app_url: informe somente a URL HTTPS da aplicação.')
        elif redirect!=expected+'/oauth2callback':errors.append('auth.redirect_uri: não corresponde à URL desta implantação.')
    dsn=database.get('url')
    try:
        p=make_url(dsn)
        good=preenchido(dsn) and p.drivername in ('postgresql','postgresql+psycopg') and p.host and p.database and p.username and p.password and p.query.get('sslmode')=='verify-full' and p.query.get('sslrootcert')
    except Exception:good=False
    if not good:errors.append('database.url: configure PostgreSQL real, credenciais e TLS verify-full com CA confiável.')
    if not preenchido(datajud.get('api_key')) or re.search(r'[\r\n]',str(datajud.get('api_key',''))):errors.append('datajud.api_key: configure a chave na área privada.')
    return errors


def testar_banco(dsn):
    """Apenas conexão TLS/SELECT; nunca cria tabela, grava ou migra dados."""
    import psycopg
    try:
        p=make_url(dsn)
        if p.drivername not in ('postgresql','postgresql+psycopg') or p.query.get('sslmode')!='verify-full' or not p.query.get('sslrootcert'):
            return False,'Configure PostgreSQL com sslmode=verify-full e CA confiável antes do teste.'
        p=p.set(drivername='postgresql')
        with psycopg.connect(p.render_as_string(hide_password=False),connect_timeout=10) as c:
            c.execute('SET TRANSACTION READ ONLY')
            if c.execute('SELECT 1').fetchone()!=(1,):return False,'Resposta PostgreSQL inesperada.'
            if c.execute('SELECT ssl FROM pg_stat_ssl WHERE pid=pg_backend_pid()').fetchone()!=(True,):return False,'A conexão precisa de TLS verificado.'
            history=c.execute("SELECT to_regclass('consultas') IS NOT NULL").fetchone()[0]
        return True,('Conexão PostgreSQL com TLS validada; tabela consultas presente.' if history else 'Conexão PostgreSQL com TLS validada; histórico será inicializado pela aplicação após login, se o usuário tiver permissão.')
    except Exception:
        return False,'Falha PostgreSQL: confira rede, certificado, credenciais e permissões na configuração privada.'
