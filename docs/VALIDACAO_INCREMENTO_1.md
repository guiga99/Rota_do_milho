# Validação do primeiro incremento

Executado no ambiente Linux, Python 3.12.14. Horários originais armazenados em UTC no histórico local; testes realizados na noite de 13/10/2026 no fuso America/Sao_Paulo.

## Resultados

| Verificação | Resultado |
|---|---|
| Dependências fixadas | Ambiente instalado e instalação repetida por `requirements-lock.txt` |
| Suíte automatizada | 13 testes executados e aprovados; nenhuma falha ou teste ignorado |
| Interface Streamlit | Quatro telas renderizadas sem exceção; configuração de sessão testada |
| Conectividade real | CNJ HTTP 200; um registro TRF4 e esquema conferidos |
| Coleta pelo serviço novo | 10 CNJs únicos; assuntos 6060, 6048 e 6045; limite atingido sem erro |
| Excel da consulta real | Gerado e reaberto; 10 registros, sete abas, conteúdo conferido |
| Download Chromium | Histórico aberto; XLSX transferido sem falha e 10 registros conferidos |
| Fluxo completo Chromium | Chave em sessão → consulta CNJ → resultados → download XLSX com 3 registros |
| Paginação multi-página | Cursor e deduplicação testados com respostas controladas |
| Falhas | 401, resposta inválida, timeout, shard failure, 429 com retry limitado e cursor repetido testados |
| Excel do Windows | Não executado; homologação pendente |
| GitHub Actions | Workflow adicionado; execução remota ainda não verificada |

Os testes reais e o navegador não publicam credenciais nem registros individuais no repositório. Arquivos e banco gerados estão em caminhos ignorados pelo Git.

## Limites de interpretação

A validação automatizada confere integridade técnica. Não atesta pertinência jurídica, procedência, trânsito confirmado ou crédito disponível. O indício de trânsito é textual e explicitamente rotulado. Os 103 termos estão preservados, mas seu mapeamento oficial completo continua pendente.

O histórico SQLite conserva snapshots de consultas e registros de origem. A normalização em tabelas relacionais globais, a revisão jurídica registrada, a política de backup, o login e o cofre de credenciais ainda não fazem parte desta versão local.

Não há URL pública hospedada nesta entrega. O servidor testado usa somente o endereço local. A instrução de execução permite iniciar uma instância no computador do operador; Windows ainda precisa de confirmação prática.
