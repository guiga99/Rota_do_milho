# Plano de testes e aceite

Testes com respostas controladas cobrem falhas. A integração real comprova acesso ao CNJ. Um não substitui o outro.

| Camada | Cenário | Resultado esperado |
|---|---|---|
| Conexão | DNS, proxy, TLS e timeout | Diagnóstico específico; verificação TLS preservada |
| Autenticação | Chave válida, inválida ou ausente | Sucesso real ou erro sanitizado; nenhum segredo em logs |
| API | 429 e 5xx | Retry limitado, espera conforme resposta e falha final explícita |
| Estrutura | HTTP 200 com HTML, JSON inválido ou esquema inesperado | Não tratar como consulta válida |
| Consulta | Zero registros | Consulta válida sem resultados, distinta de falha |
| Paginação | Duplicados, limite e falha em página posterior | Contagens reconciliadas; parcial/limite corretamente indicado |
| Normalização | CNJ com zeros, formato e dígito inválidos | Texto preservado; ressalva ou quarentena conforme regra |
| Registros | Mesmo CNJ em graus diferentes | Agrupamento único e registros de origem preservados |
| Datas | Ausentes, inválidas, futuras e sem fuso | Original preservado, sem correção silenciosa |
| Filtros | Assunto, tribunal e período incompatíveis | Divergência detectada e motivo registrado |
| Movimentos | Trânsito, ausência e eventos posteriores | Evidência explícita; não inferir resultado favorável |
| Catálogo | Termo sem código validado | Não habilitar busca como correspondência confirmada |
| Persistência | Repetição e atualização de consulta | Idempotência e histórico, sem sobrescrita indevida |
| XLSX | Exportação total, seleção e consulta parcial | Conteúdo e filtros correspondem ao escopo exportado |
| XLSX | Texto iniciando com =, +, - ou @ | Conteúdo externo não executado como fórmula |
| Segurança | Logs, exceções e arquivos | Nenhuma credencial presente |
| Navegador | Consultar, selecionar e baixar | Arquivo transferido e utilizável |
| Windows | Abrir arquivo no Excel | Sem reparo de arquivo; CNJs e caracteres corretos |
| Operação | Restaurar backup | Histórico e evidências acessíveis após restauração |

## Validação de conteúdo

Comparar todos os registros normalizados da amostra com os campos da resposta original usados na transformação. Conciliar contagens após cada etapa. Processos em quarentena devem permanecer rastreáveis e ser apresentados na aba de validação, sem passarem por registros válidos.

Avaliar pertinência com responsável jurídico: registrar quantidade revisada, pertinentes, falsos positivos e indeterminados. Definir o patamar de aceite depois dessa revisão; não inventar percentual de precisão nem declarar cobertura total do acervo.

## Execução real

Realizar uma consulta mínima para verificar acesso/esquema e uma amostra filtrada limitada. Guardar consulta sem credenciais, horário, HTTP, resposta/hash e contagens. Teste real não deve depender de número fixo de resultados ou processo específico, pois o acervo muda.

## Relatório de teste

Para cada execução registrar versão do código, ambiente, data, alvo, quantidade de testes executados, aprovados, falhos, ignorados e não executados. Separar falha do aplicativo, bloqueio externo e pendência de homologação. Não marcar a abertura no Excel do Windows como aprovada apenas porque OpenPyXL leu o arquivo.

## Situação atual

A suíte atual contém **45 testes automatizados aprovados**, em 14/10/2026 UTC, Python 3.12/Linux. Inclui AppTest, exportação, persistência, paginação, autenticação, timeout/retry, regras Google, bloqueio Cloud sem OAuth/banco, enriquecimento, revisão por campo e pré-validação Streamlit com dados sintéticos. Este é o resultado atual; o primeiro incremento tinha 13 testes.

O primeiro incremento executou consulta real com HTTP 200 e 10 CNJs, gerando XLSX reaberto por OpenPyXL. O download pelo Chromium também foi realizado, com 10 registros conferidos. A confirmação no Excel do Windows permanece pendente. Consulte [Relatório do incremento](VALIDACAO_INCREMENTO_1.md) para limites e evidências.

## Incremento da issue #4

Além da suite, passaram:

- **PostgreSQL 17 / TLS real em Docker**: CA/hostname corretos; CA incorreta rejeitada por verificação de certificado; JSON/Unicode intactos; upsert, append concorrente e deduplicação; dados conservados após reinício. Fixtures sintéticas e container/volume descartáveis. Não comprova backup/restauração nem conectividade do futuro banco Cloud.
- **Painel / Chromium**: 11 perguntas sem pré-aprovação, rascunhos, issue sem rótulo reconhecida após retorno, autor/schema, texto externo seguro, inventário, download, resposta extensa e layout mobile. Mock local de issues, sem publicar decisões fictícias.
- **Aplicação / Chromium**: upload JUDIT sintético, CNJ diferente rejeitado sem gravação, importação preservada no SQLite, original DataJud intacto, candidatos inferidos sinalizados, downloads XLSX/JSON reabertos com arquivo/hash conferidos. Não é consulta comercial real.

Reproduzir (Linux, Python 3.12):

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/testar_postgres.py
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m playwright install chromium
.venv/bin/python tests/browser_decisoes.py
.venv/bin/python tests/browser_enrichment.py
```

PostgreSQL exige Docker/OpenSSL; Chromium exige dependências do sistema. Scripts usam `/usr/bin/chromium` se disponível ou o browser instalado pelo Playwright. Dependências de navegador são de desenvolvimento; não entram no runtime Streamlit. CI executa a suite e integração PostgreSQL. Google OAuth real, consulta comercial e homologação na hospedagem continuam pendentes: STREAMLIT_CLOUD.md.

## Revisão por colegas

Sete testes específicos adicionais verificam identidade/permissão, ausência sem confirmação, comentário/evidência/correção, versões por revisor, snapshot antigo, gravação concorrente/reabertura SQLite e exportação seletiva/segura. Atualização de coleta conserva anotações já gravadas, mesmo com payload antigo. PostgreSQL verifica revisões concorrentes, preservação após atualização e reinício; Chromium salva a revisão e reabre XLSX/JSON. Fluxo Google do operador testado com identidade controlada, sem login Google real. Ver REVISAO_CAMPOS.md.

## Pré-validação Streamlit

Seis testes adicionais verificam callback HTTPS exato, campos obrigatórios/placeholder, administradores autorizados, cookie, TLS e erros sanitizados. O teste de banco é somente leitura e rejeita TLS não verificado antes de conectar; também foi executado contra PostgreSQL 17 descartável com certificado verificado. Essa evidência não comprova conta Streamlit, Google real nem banco da equipe. O roteiro registra a ação do responsável de criar a aplicação e informar sua URL pública.

## Painel de negócio — 15/10/2026

Chromium: 20 perguntas de negócio e 10 essenciais por padrão; filtros não apagam rascunhos; nota escrita antes de escolher uma alternativa é preservada; campos de configuração anteriores ficam recolhidos; registro GitHub mantém schema/autoria/contexto; respostas antigas continuam reconhecidas. Responsável jurídico adiado permanece aberto e uma definição posterior atualiza a pendência. Inventário e downloads anteriores, respostas extensas, texto externo seguro e layout mobile continuam verificados. Issues simuladas no teste não são publicadas.
