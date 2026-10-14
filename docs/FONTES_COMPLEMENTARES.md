# Fontes complementares — avaliação da issue #4

Decisões usadas: issues #1–#4 da conta responsável, validadas pelo contrato do painel. A #4 solicita estudo de **evidência de trânsito, empresa, CNPJ, advogado, polo passivo, valor da causa e resultado da decisão**. A tabela sugerida é uma hipótese; suas classificações de escala/adequação não foram demonstradas por testes.

Páginas oficiais abaixo consultadas em **14/10/2026 UTC**, com HTTPS, certificado verificado e HTTP 200. Isso comprova documentação disponível; **não comprova consulta processual autenticada, cobertura TRF4 ou contratação**. Não usamos credenciais comerciais nem executamos requisições que consumam créditos.

## Comparação verificável

| Fonte | Acesso documentado | Campos descritos | Limitação / próximo teste |
|---|---|---|---|
| **Escavador** | [Consulta de processos v2](https://api.escavador.com/v2/docs/consulta-de-processos): GET por CNJ, PAT Bearer; rota explicitamente paga. | `fontes[].envolvidos[]`: nome, tipo de pessoa, polo, CNPJ, advogados/OAB. `fontes[].capa.valor_causa`: valor/moeda. Movimentos/documentos têm recursos próprios. | Confirmar TRF4, graus, atualização e preço; localizar documentos para trânsito/resultado. `status_predito` não comprova conclusão jurídica. |
| **JUDIT** | [Índice](https://docs.judit.io/llms.txt), [OpenAPI Lawsuits](https://lawsuits.production.judit.io/docs/spec), [objeto processual](https://docs.judit.io/schemas/lawsuit-object). Header `api-key`; datalake síncrono e Requests assíncrono são produtos distintos. | `parties`: empresa, documentos, polo, advogados; `amount`, `steps`, `sentence`, `appeal_judgement`, anexos. | Verificar `was_inferred`; GET por CNJ tem `with_inferred_parties` padrão true. Solicitar false no teste e conferir resposta. Datalake pode estar defasado e atualização pode custar separadamente. |
| **Vigilant / TrackJud** | [Site](https://trackjud.com.br/) e [produto Consulta](https://trackjud.com.br/produto/consulta) descrevem API e buscas por CPF/CNPJ/OAB. | Produto anuncia partes/polos, valor, movimentações e PDF da origem. | Não localizamos referência técnica pública suficiente para implementar cliente. Confirmar CNJ, TRF4, documentos/decisões, autenticação e preço. `vigilant.com.br` trata de cibersegurança e não foi usado como fonte deste produto jurídico. |
| **Codilo** | [Introdução](https://docs.codilo.com.br/intro), [autenticação](https://docs.codilo.com.br/authentication), [abrangência](https://docs.codilo.com.br/available), [consulta automática](https://docs.codilo.com.br/api-consulta/consulta-automatica/intro). OAuth2 Client Credentials, Bearer temporário. | Capa, partes, advogados, andamentos e anexos públicos descritos. Consulta automática identifica tribunal/plataforma pelo CNJ. | Verificar cobertura real em `/v1/available`. Resposta da consulta automática lista requisições, não dados processuais: recuperar cada sucesso pela consulta única. Custo pode incluir várias plataformas/graus. |
| **Jusbrasil** | [Soluções](https://solucoes.jusbrasil.com.br/) e [documentação API](https://api.jusbrasil.com.br/docs/index.html). Acesso empresarial, token/Bearer. | Produtos de consulta processual/detalhes; oferta da plataforma não equivale ao conteúdo contratado da API. | Confirmar produto, TRF4, partes/CNPJ, documentos, atualização, preço e termos. Login do portal não concede acesso à API. Ainda não há fundamento para concluir que a API seja mais difícil que as demais. |

Não afirmamos “escala alta”, completude ou desempenho relativo sem medição. Campos podem faltar por sigilo, indisponibilidade na origem, produto contratado ou atraso de atualização.

## Recomendação e piloto

Recomendo **Escavador primeiro**, pela consulta direta por CNJ e exemplo detalhado de envolvidos/valor por fonte e grau; **JUDIT em seguida**, com atenção às inferências e atualização. Codilo merece comparação de coleta por plataforma/grau. TrackJud precisa de documentação técnica; Jusbrasil precisa de esclarecimento do produto contratado. Essa ordem é recomendação técnica, não contratação nem decisão do usuário.

O painel reúne escolhas de fornecedor, persistência e teto financeiro. Nenhuma chave deve ser informada nele. Não há compra, conta externa ou consumo de créditos automático. Não contatar fornecedores em nome do usuário sem instrução.

Depois de obter acesso autorizado e limite de custo, começar com **3 CNJs públicos da amostra de 20**. Conferir custo por consulta/atualização/documento, teto total e retries antes de executar. Preferir créditos de teste sem cobrança; ampliar até 20 só se a primeira etapa passar. Escolha de fornecedor não autoriza adquirir um plano.

Registrar por CNJ: endpoint/status/requisição sem autenticação, identificador/fonte/grau/atualização, corpo/hash privado, presença dos sete campos, documento/texto/URL quando permitido, conflitos/inferências, latência e custo confirmado. Aceite técnico: CNJ exato/válido, contagens, original recuperável, proveniência, TLS, diagnóstico de erros, teto respeitado e XLSX reaberto. Aceite jurídico separado, com responsável ainda a definir. Não publicar conteúdo individual ou contato de partes no Git.

## Interpretação dos sete campos

| Campo | Critério / cuidado |
|---|---|
| Empresa | Todas as pessoas jurídicas são candidatas, inclusive entes públicos; identificar o contribuinte exige polo/contexto. |
| CNPJ | Texto associado à parte. Importação não confirma Receita/titularidade; CPF não será convertido em CNPJ. |
| Advogado | Manter advogado/OAB ligados à parte e grau; vários representantes podem atuar em polos diferentes. |
| Polo passivo | Papel informado pela fonte/grau; não inferir pelo título do processo. |
| Valor da causa | Preservar valor/moeda/instância e divergências. Não equivale a crédito recuperável. |
| Evidência de trânsito | Ato/documento com texto/data/grau/CNJ. Arquivado, inativo, finalizado ou status predito não bastam. Ocorrência textual é candidata: pode negar trânsito ou citar outro ato. |
| Resultado decisão | Teor/dispositivo e contexto com revisão jurídica. Tipo de sentença, fase ou existência de decisão não determinam resultado favorável ao contribuinte. |

## Importador implementado

**Resultados → Complementar informações com JSON de fornecedor** permite ao administrador importar UTF-8 de até 5 MiB de um CNJ da consulta aberta. Sem chamadas comerciais. Rejeita credenciais, CNJ inválido/diferente e estruturas incompatíveis. Aceita Escavador v2 e JUDIT Lawsuits plano ou envelope `response_data` documentado.

Preserva arquivo original UTF-8, objeto JSON, SHA256 dos bytes, fornecedor/documentação, horário de **importação**, administrador, caminhos dos campos, IDs/grau quando presentes. Hash comprova integridade do arquivo recebido, não autenticidade nem consulta real; importação não equivale a coleta judicial. Campos novos ficam no original. Download de evidências JSON permite reconstruir o arquivo e seu hash.

Estados: `pendente_revisao`, `inferido_fornecedor`, `nao_fornecido`. Ausência não é presumida como não contratado/acesso negado/processo inexistente, que exigem evidência da requisição futura. Inferências e conflitos permanecem visíveis; trânsito textual/resultado não viram conclusões jurídicas automaticamente. Documentos/links não são abertos automaticamente.

Mesmo fornecedor/hash não é importado duas vezes. Transação serializa importações concorrentes. Originais DataJud não são alterados. XLSX traz **COMPLEMENTOS** e **FONTES_COMPLEMENTARES** filtrados pelos CNJs exportados, com textos longos fragmentados. Colunas jurídicas de PROCESSOS aguardam aprovação; não recebem candidatos automaticamente.

Scraping só será estudado com acesso permitido e falta de integração adequada, sem contornar CAPTCHA, acesso ou sigilo. O eproc da issue #3 continua como consulta humana separada.
