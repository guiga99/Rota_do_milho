# Avaliação inicial das fontes complementares

Orientação usada: issues #1 e #2, com precedência da #2. Interpretei “JusBraisk” como Jusbrasil. A preferência é avaliar outras fontes para partes, advogados, valor e decisões. Ainda não há contratação ou credencial de integração complementar.

## Fontes oficiais verificadas

| Fonte | Evidência consultada | Acesso técnico documentado | Próxima validação |
|---|---|---|---|
| Jusbrasil | [Soluções](https://solucoes.jusbrasil.com.br/) e [documentação API](https://api.jusbrasil.com.br/docs/index.html), ambas HTTP 200 | Portfólio de APIs, consulta processual e detalhes do processo; token de acesso e autenticação Bearer na documentação | Confirmar produto, cobertura TRF4, campos, custo e acesso contratado; depois comparar uma consulta por CNJ |
| Escavador | [API Business](https://www.escavador.com/business/api) e [documentação v2](https://api.escavador.com/v2/docs/), HTTP 200 | API estruturada, envolvidos/OAB e autos descritos; autenticação PAT Bearer e recursos de saldo documentados | Confirmar cobertura, acesso aos campos e custo antes do teste autenticado |
| JUDIT | [Introdução](https://docs.judit.io/introduction/introduction) e [criar requisição](https://docs.judit.io/api-reference/endpoint/requests/create), HTTP 200 | Consulta assíncrona por CNJ/CPF/CNPJ/OAB, chave `api-key`; introdução orienta obter a chave com o comercial | Confirmar contrato, cobertura e resposta efetiva para os campos desejados |

Verificações feitas em 13/10/2026, America/Sao_Paulo. As páginas públicas comprovam documentação acessível; não comprovam acesso contratado nem retorno dos dados de um processo. Nenhuma consulta autenticada nesses fornecedores foi executada. Nenhuma credencial com nomes Jusbrasil, Escavador ou JUDIT foi encontrada no processo do ambiente.

## Recomendação

Avaliar primeiro a API oficial do Jusbrasil, conforme a preferência informada, usando os mesmos CNJs da amostra de 20. O login do portal não deve ser presumido como acesso à API. Comparar disponibilidade e qualidade dos campos, atualização, cobertura do TRF4, custo e condições de uso com Escavador e JUDIT.

Scraping fica como alternativa condicionada à existência de acesso permitido e à falta de uma integração adequada. Antes de implementar, verificar os termos do portal, os campos visíveis e a manutenção necessária. Não contornar CAPTCHA, controles de acesso ou solicitar senha pelo painel público. Esta etapa avaliou somente páginas públicas de produtos e documentação, sem coletar processos dos portais.

## Contrato de enriquecimento proposto

Vincular cada observação ao CNJ, fonte, horário e identificador do fornecedor. Manter dados originais e evidências separados da base DataJud. Divergências de parte, valor, fase ou resultado devem aparecer para revisão; não substituir automaticamente uma fonte pela outra.

Para cada campo, distinguir: fornecido, não fornecido, não contratado, acesso negado e pendente de revisão. A existência de uma decisão não implica resultado favorável. A disponibilidade de partes ou CNPJ precisa ser confirmada por consulta real autorizada.
