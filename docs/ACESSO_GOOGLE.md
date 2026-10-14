# Login Google da equipe

Escolha confirmada pela issue #3. O código agora usa OIDC nativo do Streamlit (`st.login`, `st.user` e `st.logout`), com Authlib fixada nas dependências. A assinatura e o fluxo OIDC são tratados pelo framework; a autorização por e-mail e perfil é verificada pela aplicação.

## Configuração necessária

1. Definir onde a aplicação Python será hospedada, com HTTPS e armazenamento persistente. GitHub Pages hospeda somente o painel estático.
2. No Google Cloud, configurar consentimento e um cliente OAuth do tipo aplicação Web, com a mesma Redirect URI usada pelo Streamlit. Para desenvolvimento, a documentação oficial permite `http://localhost:8501/oauth2callback`; em produção usar a URL HTTPS real do aplicativo.
3. Guardar `client_id`, `client_secret`, segredo de cookie e listas de e-mails na configuração protegida do servidor. Não registrar esses valores em issues ou no painel público.
4. Definir `allowed_emails` e `admin_emails`. A aplicação exige conta Google com e-mail verificado e lista exata de endereços; entrar com Google não autoriza qualquer pessoa automaticamente.
5. Configurar a chave DataJud no ambiente do servidor ou na seção privada `[datajud] api_key`. Administradores podem alterar a chave da sessão; operadores não veem o formulário de integração.

Os valores OAuth e a lista da equipe não foram fornecidos no ambiente. O fluxo real Google ainda não foi executado. Não existe URL pública da aplicação Python nesta entrega.

## Preparar localmente

O arquivo `.streamlit/secrets.example.toml` serve como modelo e não é uma configuração ativa. Com cliente OAuth criado, execute:

```bash
.venv/bin/python scripts/configurar_google.py
```

No Windows, use `.venv\Scripts\python.exe`. O script recebe o segredo sem exibição, gera o segredo de cookie, valida listas e grava `.streamlit/secrets.toml` fora do Git. Recusa sobrescrever uma configuração existente. Reinicie o aplicativo, abrindo pelo hostname registrado no Google.

O modo é `google` quando configurado em `[access] mode`, ou por `ROTA_AUTH_MODE=google`. Nesse modo, configuração ausente/interrompida bloqueia o acesso antes de criar banco ou mostrar consultas. O modo `local` exige endereço de servidor de loopback e bloqueia endereços públicos. O config.toml padrão usa 127.0.0.1. Para hospedagem, configure o modo Google e o endereço exigido pelo provedor, com domínio HTTPS e callback correto.

## Perfis e histórico

- Administrador: consultas, resultados e configurações de integração.
- Operador: consultas/resultados e histórico compartilhado da equipe; sem formulário de chaves.
- Conta não autorizada, não verificada, emissor inesperado ou token com expiração já vencida: acesso recusado.

O servidor registra quem executou a consulta. O histórico é compartilhado entre usuários autorizados desta equipe, ainda sem separação por organização. Não foi habilitado cadastro aberto de usuários. O logout limpa a sessão antes de sair pelo provedor.

## Validação e fontes

Testes cobrem autorização exata, roles, e-mail verificado, emissor, expiração, bloqueio sem configuração e ocultação da chave para operador. Esses testes não substituem homologação real do cliente OAuth, callback e logout no domínio hospedado.

Fontes oficiais consultadas com HTTP 200 em 14/10/2026:

- [Streamlit st.login](https://docs.streamlit.io/develop/api-reference/user/st.login)
- [Autenticação OIDC no Streamlit](https://docs.streamlit.io/develop/concepts/connections/authentication)
