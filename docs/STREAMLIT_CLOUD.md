# Piloto no Streamlit Community Cloud

Escolha da [issue #4](https://github.com/guiga99/Rota_do_milho/issues/4): piloto gerenciado com persistência antes de dados operacionais. Código preparado; **nenhuma aplicação Streamlit pública foi criada nesta etapa**. GitHub Pages continua como painel de decisões.

## Configuração concreta

1. Entrar no [Streamlit Community Cloud](https://share.streamlit.io/) com conta autorizada ao repositório. Criar aplicação: **guiga99/Rota_do_milho**, branch **main**, arquivo **cloud_app.py**, Python **3.12**. Escolher subdomínio e obter URL HTTPS.
2. Disponibilizar PostgreSQL gerenciado, usuário exclusivo e banco dedicado. Definir região, retenção/backup, armazenamento/conexões e condições de uso. Banco existente, Neon e Supabase estão no painel para avaliação, sem contratação automática.
3. Configurar cliente Google OAuth web, origem da aplicação e redirect exato `https://SEU_SUBDOMINIO.streamlit.app/oauth2callback`. Em modo de teste, cadastrar usuários de teste. Ver [ACESSO_GOOGLE](ACESSO_GOOGLE.md).
4. Preencher **Settings → Secrets** com [.streamlit/secrets.cloud.example.toml](../.streamlit/secrets.cloud.example.toml): OAuth/cookie, allowlist/admins, DSN e chave DataJud. Valores reais nunca vão ao Git, issues ou painel.
5. DSN requer `sslmode=verify-full` e `sslrootcert=system` ou CA confiável do provedor. Percent-encode caracteres especiais da senha. Não substituir verificação por `sslmode=require`. Validar endpoint/pool, rede e permissões no Cloud.
6. Iniciar aplicação e executar homologação abaixo. Sem OAuth, acesso bloqueia antes do banco; sem PostgreSQL, telas de consulta bloqueiam. Não existe fallback online para SQLite.

Dependências diretas e lock versionados. `cloud_app.py` força Google, independentemente de variável/modo local. Loopback global foi retirado para compatibilidade Cloud; comandos locais e `iniciar_windows.bat` continuam usando `--server.address 127.0.0.1`. `app.py` sem loopback e sem Google bloqueia acesso.

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
