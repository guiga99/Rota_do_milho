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

Nenhuma suíte automatizada da aplicação foi implementada ou executada nesta entrega documental. O piloto anterior gerou um XLSX legível por OpenPyXL, mas o usuário não conseguiu baixá-lo pelo chat. O fluxo de download e a abertura no Excel permanecem pendentes de teste no produto.
