# Arquitetura proposta

## Componentes

Navegador → Streamlit → serviço de consulta → cliente DataJud/CNJ.

O serviço de consulta também aciona normalização, validação, regras de movimentos, SQLite, armazenamento de respostas e exportador OpenPyXL. O navegador nunca chama o CNJ com a chave da integração.

O modo local usa SQLite em loopback. O piloto da equipe no Streamlit Community Cloud usa `cloud_app.py`, Google/allowlist e PostgreSQL externo obrigatório com TLS/CA/hostname verificados. Sem configuração, bloqueia acesso; sem banco externo, não recorre a SQLite. Histórico compartilhado, configurações/importação restritas ao administrador. Ver STREAMLIT_CLOUD.md.

Complementos são snapshots independentes dentro da consulta, com arquivo original, hash, autor/data de importação e observações por caminho/grau/fonte. Append transacional evita perda em importações simultâneas; não sobrescreve fontes DataJud. Importação offline não comprova autenticação do fornecedor. Colunas jurídicas aguardam revisão; candidatos constam em abas próprias. Ver FONTES_COMPLEMENTARES.md.

## Modelo lógico

| Entidade | Identidade e finalidade |
|---|---|
| Consulta | UUID; filtros, limite, horários, status, contagens e versões |
| Resposta | Consulta + página; JSON original, hash SHA-256, HTTP e instante |
| Processo | Número CNJ normalizado como texto; agrupamento lógico |
| Registro de origem | Fonte + identificador fornecido pela fonte; grau e dados observados |
| Observação | Registro + consulta/resposta; preserva alterações entre coletas |
| Movimento | Observação + posição original; preserva ocorrências repetidas sem colapsar eventos legítimos |
| Validação | Observação + regra/versão; resultado, motivo e campo afetado |
| Revisão jurídica | Processo/observação, responsável, data, avaliação e evidência |
| Termo e mapeamento | Termo original, código oficial, justificativa, fonte e status |

Não usar somente CNJ para substituir registros de origem. Manter versões necessárias para reexportar uma consulta histórica. Deduplicação idempotente deve ser definida por identidade da origem e conteúdo, sem perder proveniência.

## Regras de coleta

- Tamanho de página e limite de CNJs são conceitos distintos.
- Paginação e desempate de ordenação devem seguir campos suportados e confirmados na API.
- Preservar o cursor e identificar resultados parciais quando uma página falhar.
- Não prometer snapshot atômico do acervo se a API não oferecer essa garantia.
- Registrar contagem recebida, rejeitada tecnicamente, duplicada, única e exportada.
- Conservar totais e relação `eq`/`gte` conforme retorno original.

## Contrato de dados

Número CNJ: string. Datas: original preservado e representação interpretada separada; não inventar fuso quando ausente. Valores monetários: decimal e moeda apenas quando fornecidos e validados. Campos ausentes: nulos, sem inferência.

Classificação jurídica é derivada e precisa ter versão, evidência e ressalva. Última movimentação disponível não garante atualização em tempo real do tribunal. Data de coleta, atualização informada pela fonte e data do movimento devem aparecer separadamente.

## Excel

Abas previstas: RESUMO, PROCESSOS, MOVIMENTACOES, FONTES, PENDENCIAS, EXECUCAO e VALIDACAO. Incluir os filtros locais de uma seleção exportada. Usar filtros, cabeçalhos congelados e CNJ em texto. Validar limites de linhas/células do formato e reportar qualquer truncamento; manter conteúdo completo na evidência original.
