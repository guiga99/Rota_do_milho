"""Autorização da equipe após autenticação OIDC validada pelo Streamlit."""
import time

GOOGLE_METADATA = 'https://accounts.google.com/.well-known/openid-configuration'


def emails(values):
    if isinstance(values, str): values = values.split(',')
    return frozenset(v.strip().casefold() for v in (values or []) if isinstance(v,str) and v.strip())


def autorizar(claims, allowed, admins, now=None):
    if claims.get('iss') not in ('https://accounts.google.com','accounts.google.com'):
        return None
    if claims.get('email_verified') is not True:
        return None
    address = claims.get('email')
    if not isinstance(address,str): return None
    address = address.strip().casefold()
    if address not in emails(allowed): return None
    expiry=claims.get('exp')
    if expiry is not None:
        if not isinstance(expiry,(int,float)) or isinstance(expiry,bool) or expiry <= (now if now is not None else time.time()):
            return None
    return {'email':address,'role':'admin' if address in emails(admins) else 'operator'}


def proteger(st, mode, settings):
    if mode == 'local':
        if st.get_option('server.address') not in ('127.0.0.1','localhost','::1'):
            st.error('Modo local requer servidor em loopback. Para acesso externo, configure Google e usuários autorizados.');st.stop()
        return {'email':'operador local','role':'admin','mode':'local'}
    if mode != 'google':
        st.error('Modo de autenticação inválido. Configure local ou google.');st.stop()
    auth=settings.get('auth',{});provider=auth.get('google',{});access=settings.get('access',{})
    complete=all(auth.get(k) for k in ['redirect_uri','cookie_secret']) and all(provider.get(k) for k in ['client_id','client_secret'])
    if not complete or not str(provider.get('client_id','')).endswith('.apps.googleusercontent.com') or len(str(auth.get('cookie_secret','')))<32 or provider.get('server_metadata_url')!=GOOGLE_METADATA or not emails(access.get('allowed_emails')):
        st.error('Login Google ainda não configurado. Use as instruções de ACESSO_GOOGLE antes de liberar a aplicação para a equipe.');st.stop()
    if not st.user.is_logged_in:
        st.info('Entre com uma conta Google autorizada para acessar as consultas.')
        if st.button('Entrar com Google'): st.login('google')
        st.stop()
    identity=autorizar(dict(st.user),access.get('allowed_emails'),access.get('admin_emails'))
    if not identity:
        st.error('Esta conta não está autorizada, não está verificada ou a sessão expirou.')
        if st.button('Sair'): st.session_state.clear();st.logout()
        st.stop()
    return {**identity,'mode':'google'}
