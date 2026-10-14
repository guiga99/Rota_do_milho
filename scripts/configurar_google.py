"""Prepara configuração privada sem imprimir segredos e sem sobrescrever arquivos."""
import getpass
import json
import secrets
from pathlib import Path
from urllib.parse import urlsplit

root=Path(__file__).resolve().parents[1]
path=root/'.streamlit/secrets.toml'
if path.exists():raise SystemExit('Configuração já existe. Revise-a no local protegido; este script não sobrescreve arquivos.')
client=input('Client ID Google: ').strip()
if not client.endswith('.apps.googleusercontent.com'):raise SystemExit('Client ID não corresponde ao formato Google.')
secret=getpass.getpass('Client secret Google (oculto): ').strip()
if not secret:raise SystemExit('Client secret obrigatório.')
redirect=input('Redirect URI [http://localhost:8501/oauth2callback]: ').strip() or 'http://localhost:8501/oauth2callback'
u=urlsplit(redirect)
if u.scheme!='https' and not (u.scheme=='http' and u.hostname in ('localhost','127.0.0.1')):raise SystemExit('Use HTTPS em produção ou HTTP em localhost para desenvolvimento.')
allowed=[x.strip().casefold() for x in input('E-mails autorizados, separados por vírgula: ').split(',') if x.strip()]
admins=[x.strip().casefold() for x in input('E-mails administradores, separados por vírgula: ').split(',') if x.strip()]
if not allowed or not admins or not set(admins)<=set(allowed):raise SystemExit('Informe usuários e administradores; administradores devem estar na lista autorizada.')
def q(v):return json.dumps(v,ensure_ascii=True)
content=f'''[auth]
redirect_uri = {q(redirect)}
cookie_secret = {q(secrets.token_urlsafe(48))}

[auth.google]
client_id = {q(client)}
client_secret = {q(secret)}
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"

[access]
mode = "google"
allowed_emails = {q(allowed)}
admin_emails = {q(admins)}
'''
path.parent.mkdir(exist_ok=True)
with path.open('x',encoding='utf-8') as f:f.write(content)
path.chmod(0o600)
print('Configuração privada criada em .streamlit/secrets.toml. Nenhum segredo exibido. Reinicie a aplicação e configure a mesma Redirect URI no Google Cloud.')
