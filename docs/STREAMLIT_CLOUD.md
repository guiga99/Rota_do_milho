# Piloto no Streamlit Community Cloud

Escolha da [issue #4](https://github.com/guiga99/Rota_do_milho/issues/4): piloto gerenciado com persistência antes de dados operacionais. Código preparado; **nenhuma aplicação Streamlit pública foi criada nesta etapa**. GitHub Pages continua como painel de decisões.

## Ação inicial na conta do responsável

Esta etapa depende da sessão do responsável no Streamlit, que não está conectada a este chat. Em [share.streamlit.io](https://share.streamlit.io/), entre na conta e escolha **Create app**. Preencha:

| Campo | Valor |
|---|---|
| Repository | `guiga99/Rota_do_milho` |
| Branch | `main` |
| Main file path | `cloud_app.py` |
| Python version (Advanced settings) | `3.12` |

Escolha um subdomínio disponível e publique inicialmente **sem Secrets**, se ainda não os tiver. A aplicação mostrará o aviso de login não configurado e bloqueará acesso às consultas/banco. Essa publicação inicial serve para reservar e obter a URL HTTPS; não é homologação nem ativação operacional. **Informe no chat somente a URL pública obtida.** Com ela definimos o callback Google exato. Não informe login/senha nem o conteúdo dos Secrets no chat ou GitHub.

Depois da URL, configure OAuth web e banco da equipe na área privada conforme os passos abaixo. Se o Streamlit não listar o repositório, confira a conta GitHub vinculada e a autorização dessa conta para `guiga99/Rota_do_milho`.

## Configuração concreta

1. Entrar no [Streamlit Community Cloud](https://share.streamlit.io/) com conta autorizada ao repositório. Criar aplicação: **guiga99/Rota_do_milho**, branch **main**, arquivo **cloud_app.py**, Python **3.12**. Escolher subdomínio e obter URL HTTPS.
2. Disponibilizar PostgreSQL gerenciado, usuário exclusivo e banco dedicado. Definir região, retenção/backup, armazenamento/conexões e condições de uso. Banco existente, Neon e Supabase estão no painel para avaliação, sem contratação automática.
3. Configurar cliente Google OAuth web, origem da aplicação e redirect exato `https://SEU_SUBDOMINIO.streamlit.app/oauth2callback`. Em modo de teste, cadastrar usuários de teste. Ver [ACESSO_GOOGLE](ACESSO_GOOGLE.md).
4. Preencher **Settings → Secrets** com [.streamlit/secrets.cloud.example.toml](../.streamlit/secrets.cloud.example.toml): OAuth/cookie, allowlist/admins, DSN e chave DataJud. Valores reais nunca vão ao Git, issues ou painel.
5. DSN requer `sslmode=verify-full` e `sslrootcert=system` ou CA confiável do provedor. Percent-encode caracteres especiais da senha. Não substituir verificação por `sslmode=require`. Validar endpoint/pool, rede e permissões no Cloud.
6. Iniciar aplicação e executar homologação abaixo. Sem OAuth, acesso bloqueia antes do banco; sem PostgreSQL, telas de consulta bloqueiam. Não existe fallback online para SQLite.

Dependências diretas e lock versionados. `cloud_app.py` força Google, independentemente de variável/modo local. Loopback global foi retirado para compatibilidade Cloud; comandos locais e `iniciar_windows.bat` continuam usando `--server.address 127.0.0.1`. `app.py` sem loopback e sem Google bloqueia acesso.

## Verificar os Secrets antes da ativação

O script `scripts/verificar_streamlit.py` verifica configuração real, administradores/usuários, callback exato, campos obrigatórios e DSN com TLS. O modelo de exemplo é rejeitado enquanto contiver placeholders. Lê arquivo privado e informa apenas nomes dos campos pendentes; não imprime credenciais nem realiza login OAuth.

No computador autorizado, com `.streamlit/secrets.toml` privado preenchido:

```bash
.venv/bin/python scripts/verificar_streamlit.py --app-url https://SEU_SUBDOMINIO.streamlit.app
```

No Windows, substitua `.venv/bin/python` por `.venv\Scripts\python.exe`. A verificação padrão é offline. Para testar o banco com a configuração autorizada:

```bash
.venv/bin/python scripts/verificar_streamlit.py --app-url https://SEU_SUBDOMINIO.streamlit.app --testar-banco
```

O teste usa transação somente leitura, SELECT e TLS verificado; não cria tabela, migra ou grava dados. Confirma conexão e presença do histórico, mas não comprova todas as permissões de gravação. Inicialização do banco e coleta precisam de homologação na aplicação. Arquivo com outro nome pode ser informado por `--config`; não copie o arquivo privado ao Git. Cole os valores reais somente nos **Settings → Secrets** da aplicação Streamlit.

Saída 0 significa que as verificações executadas passaram; 2 indica configuração pendente/inválida; 3 indica falha na conexão. Verificação offline não comprova conta Google, banco acessível ou implantação. Dados sintéticos cobrem o script na suite e PostgreSQL descartável; ainda falta validar o banco da equipe.

## Persistência e limites

SQLite destina-se ao uso local. Filesystem/container do Cloud não substitui persistência/backup. Histórico online usa PostgreSQL externo, guardando consultas, páginas DataJud e complementos no payload. Reiniciar/reimplantar a aplicação não deveria apagar o banco externo, mas ainda precisa de teste na implantação real.

Pool por processo: 2 conexões e até 2 adicionais, com verificação antes do uso. Réplicas/processos multiplicam o total. Erros não expõem DSN/credenciais. Não há migração automática do SQLite: preservar backup e migrar com conciliação antes de uso operacional. Crescimento exigirá índices, retenção e armazenamento de arquivos próprios.

Importação e revisão bloqueiam a linha por transação, evitando perder anotações simultâneas. Histórico é compartilhado por usuários autorizados. Operadores consultam/exportam/revisam; administradores também configuram/importam. Separação por cliente/tenant e cofre próprio não foram implementados. Não guardar credenciais de tribunais nos payloads. Nenhum cliente comercial ativo nesta versão.

## Homologação na implantação

- [ ] HTTPS/callback exatos; anônimo vê somente login, sem dados.
- [ ] Google real: autorizado entra; operador/admin corretos; conta fora da lista rejeitada; logout.
- [ ] PostgreSQL real: TLS/CA/hostname, usuário restrito e conexão pelo Cloud; erro sem credenciais nos logs.
- [ ] Consulta pequena TRF4: número/tribunal/contagens/exportação conciliados.
- [ ] Reinício/redeploy preserva histórico; indisponibilidade do banco recebe diagnóstico.
- [ ] Backup e restauração em banco separado, comparando payloads/hashes. Reinício de teste não comprova restauração de backup.
- [ ] Download/reabertura XLSX/JSON; fontes íntegras; nenhum dado privado no painel/Git.
- [ ] Licenças, região/retenção, responsável operacional e revisão jurídica definidos antes de ampliar uso.

## Evidência e requisitos externos

Testes automatizados verificam bloqueio sem OAuth/DB, autorização Google e exportação sintética. `scripts/testar_postgres.py` usa PostgreSQL 17 descartável com TLS: aceita CA/hostname corretos, rejeita CA incorreta, conserva JSON/Unicode, testa upsert/importações concorrentes e compara histórico após reinício. Remove somente seu container/volume; requer Docker/OpenSSL e não acessa produção. CI executa o teste.

Faltam conta/deploy Streamlit, OAuth e banco provisionado com configuração privada. Não há credenciais desses serviços no ambiente. Ainda não há URL da aplicação de pesquisas nem login Google real homologado.

Referências oficiais HTTP 200, 14/10/2026: [preparar/deploy](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app), [Secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management), [configurações](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/app-settings).
