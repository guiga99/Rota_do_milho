# Login Google da equipe

Escolha confirmada pela issue #3. O código agora usa OIDC nativo do Streamlit (`st.login`, `st.user` e `st.logout`), com Authlib fixada nas dependências. A assinatura e o fluxo OIDC são tratados pelo framework; a autorização por e-mail e perfil é verificada pela aplicação.

## Configuração necessária

1. Usar o endereço Streamlit informado pelo responsável: `https://rotadomilho-dnvdghu9uyapphcp5gub6xj.streamlit.app`. A hospedagem escolhida é Community Cloud com PostgreSQL da equipe; funcionamento/login ainda precisam de homologação. GitHub Pages hospeda somente o painel de decisões.
2. No Google Cloud, configurar consentimento e um cliente OAuth do tipo aplicação Web, com a mesma Redirect URI usada pelo Streamlit. Para desenvolvimento, a documentação oficial permite `http://localhost:8501/oauth2callback`; em produção usar a URL HTTPS real do aplicativo.
3. Guardar `client_id`, `client_secret`, segredo de cookie e listas de e-mails na configuração protegida do servidor. Não registrar esses valores em issues ou no painel público.
4. Definir `allowed_emails` e `admin_emails`. A aplicação exige conta Google com e-mail verificado e lista exata de endereços; entrar com Google não autoriza qualquer pessoa automaticamente.
5. Configurar a chave DataJud no ambiente do servidor ou na seção privada `[datajud] api_key`. Administradores podem alterar a chave da sessão; operadores não veem o formulário de integração.

Os valores OAuth e a lista da equipe não foram fornecidos no ambiente. O fluxo real Google ainda não foi executado. O endereço da aplicação foi informado; isso não comprova login ou histórico operacional.

## Próxima ação na conta Google

Abra [Google Auth Platform → Clients](https://console.cloud.google.com/auth/clients) e selecione o projeto da equipe. Se o projeto ainda não usa OAuth, configure primeiro **Branding** (nome Rota do Milho, e-mail de suporte e contato), **Audience** e **Data Access**. Escolha External se houver contas pessoais Google; Internal só atende usuários da organização Google Workspace correspondente. No modo de teste, inclua os colegas em **Test users**.

Em **Create client**, escolha **Web application** e registre:

**Authorized JavaScript origins** — sem barra no final:

```text
https://rotadomilho-dnvdghu9uyapphcp5gub6xj.streamlit.app
```

**Authorized redirect URIs** — exatamente:

```text
https://rotadomilho-dnvdghu9uyapphcp5gub6xj.streamlit.app/oauth2callback
```

Para este login, use apenas identidade básica `openid`, `email` e `profile`; acesso a Drive/Gmail não é necessário. Copie Client ID e Client secret somente para **Settings → Secrets** da aplicação Streamlit, na seção `[auth.google]` do [modelo Cloud](../.streamlit/secrets.cloud.example.toml). O `redirect_uri` de `[auth]` já está ajustado para esse endereço. Gere também um segredo aleatório de cookie com pelo menos 32 caracteres; o script local abaixo gera esse segredo sem exibi-lo.

Configure `allowed_emails` com os colegas e `admin_emails` com administradores que também estejam na primeira lista. Essas listas ficam na área privada. Salve e reinicie a aplicação. Com Google configurado, a entrada passa a oferecer login; depois de entrar, falta de banco será diagnosticada sem liberar consultas. A liberação operacional depende também do PostgreSQL.

Se aparecer `redirect_uri_mismatch`, compare a URI nos dois lugares, incluindo protocolo, hostname e `/oauth2callback`. Se uma conta receber acesso negado pelo Google durante os testes, confira Audience/Test users; a lista do Google e a lista autorizada da aplicação são controles distintos. Não alterar permissões nem desativar o login para contornar o erro.

## Preparar localmente

O arquivo `.streamlit/secrets.example.toml` serve como modelo e não é uma configuração ativa. Com cliente OAuth criado, execute:

```bash
.venv/bin/python scripts/configurar_google.py
```

No Windows, use `.venv\Scripts\python.exe`. O script recebe o segredo sem exibição, gera o segredo de cookie, valida listas e grava `.streamlit/secrets.toml` fora do Git. Recusa sobrescrever uma configuração existente. Reinicie o aplicativo, abrindo pelo hostname registrado no Google.

O modo é `google` quando configurado em `[access] mode`, ou por `ROTA_AUTH_MODE=google`. `cloud_app.py` sempre exige Google. Nesse modo, configuração ausente/interrompida bloqueia acesso antes do banco ou consultas. O modo local exige loopback; comandos locais passam `--server.address 127.0.0.1`. O config.toml não fixa esse endereço, para compatibilidade Cloud.

## Perfis e histórico

- Administrador: consultas, resultados, revisão de campos, configuração e importação.
- Operador: consultas/resultados, revisão e histórico compartilhado; sem formulário de chaves ou importação.
- Conta não autorizada, não verificada, emissor inesperado ou token com expiração já vencida: acesso recusado.

O servidor registra quem executou a consulta. O histórico é compartilhado entre usuários autorizados desta equipe, ainda sem separação por organização. Não foi habilitado cadastro aberto de usuários. O logout limpa a sessão antes de sair pelo provedor.

## Validação e fontes

Testes cobrem autorização exata, roles, e-mail verificado, emissor, expiração, bloqueio sem configuração e ocultação da chave para operador. Esses testes não substituem homologação real do cliente OAuth, callback e logout no domínio hospedado.

Fontes oficiais consultadas com HTTP 200 em 14/10/2026:

- [Streamlit st.login](https://docs.streamlit.io/develop/api-reference/user/st.login)
- [Autenticação OIDC no Streamlit](https://docs.streamlit.io/develop/concepts/connections/authentication)

A descoberta OIDC oficial do Google respondeu HTTP 200 neste ambiente, com issuer esperado. Credenciais, callback e login/logout reais continuam não homologados.
