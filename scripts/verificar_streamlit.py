"""Valida Secrets localmente sem imprimir credenciais ou fazer login Google."""
import argparse
import sys
import tomllib
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from rota.deployment import validar, testar_banco


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,default=Path(__file__).resolve().parents[1]/'.streamlit/secrets.toml')
    parser.add_argument('--app-url',help='URL HTTPS pública da aplicação (sem credenciais).')
    parser.add_argument('--testar-banco',action='store_true',help='Testar conexão PostgreSQL com SELECT e TLS, sem gravações.')
    args=parser.parse_args(argv)
    try:settings=tomllib.loads(args.config.read_text(encoding='utf-8'))
    except (OSError,ValueError):
        print('Configuração privada ausente ou TOML inválido. Use o modelo Cloud e preencha em local protegido.')
        return 2
    errors=validar(settings,args.app_url)
    if errors:
        for e in errors:print('PENDENTE:',e)
        return 2
    print('Estrutura dos Secrets validada. Valores privados não foram exibidos. OAuth/login/implantação ainda exigem homologação real.')
    if args.testar_banco:
        ok,message=testar_banco(settings['database']['url']);print(message)
        return 0 if ok else 3
    print('Verificação offline: nenhuma conexão externa foi executada.')
    return 0


if __name__=='__main__':raise SystemExit(main())
