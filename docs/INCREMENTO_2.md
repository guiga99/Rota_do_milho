# Incremento orientado pelas issues #1 e #2

As duas issues contêm as mesmas escolhas. Usada a #2 como registro vigente, sem tratar duplicação como duas instruções diferentes.

| Orientação | Resultado nesta entrega |
|---|---|
| Pelo menos 20 processos e todos os campos | Nova consulta real de 20 CNJs, Excel com inventário e dados originais, ZIP com resposta completa e evidências |
| Últimos cinco anos | Período padrão habilitado no aplicativo, com cálculo no fuso America/Sao_Paulo e datas editáveis |
| Avaliar outros portais | Documentação oficial de Jusbrasil, Escavador e JUDIT verificada; avaliação em FONTES_COMPLEMENTARES.md |
| Acesso pela equipe | Requisito registrado; pergunta de provedor de login no painel antes da hospedagem protegida |
| Responsável jurídico ainda indefinido | Classificações continuam técnicas e os resultados continuam candidatos |

## Amostra

TRF4, ajuizamento entre 2021-10-13 e 2026-10-13. Assuntos usados: 6060, 6048, 6045, 6062, 6068, 6037, 6041 e 6038. Ordenação por ajuizamento decrescente com desempate por identificador. A amostra privilegia candidatos recentes dentro do período; não é representativa do acervo nem seleção de casos encerrados.

Resultado: HTTP 200, 20 CNJs únicos, 20 registros de origem, 59 movimentos, 39 caminhos de campos incluindo estruturas e nenhum registro com ressalva técnica. Todos retornaram `nivelSigilo=0`. A revisão jurídica não foi realizada.

## Todos os campos

A exportação agora inclui CAMPOS_DISPONIVEIS com tipos, presença por registro, ocorrências e nulos. DADOS_ORIGINAIS preserva todos os caminhos com índices de listas, inclusive complementos de movimentos. Campos desconhecidos não são descartados. Textos longos são fragmentados sem truncamento; conteúdo externo é protegido contra fórmulas. O JSON no ZIP é a referência original completa, inclusive o envelope da resposta da API.

Há descrição em `movimentos[].complementosTabelados[].descricao` nesta amostra. Ela descreve um complemento de movimentação; não foi tratada como texto de decisão ou assunto jurídico. Nome do assunto continua em `assuntos[].nome`. Partes, CNPJ, advogados, valor e teor/resultado da decisão não vieram na resposta.

## Entrega e decisões seguintes

[Excel de 20 processos](https://github.com/guiga99/Rota_do_milho/releases/download/amostra-trf4-20-v1/TRF4_amostra20.xlsx)

[ZIP com dados completos](https://github.com/guiga99/Rota_do_milho/releases/download/amostra-trf4-20-v1/TRF4_amostra20_dados_completos.zip)

Os dados individuais ficam em assets da Release, fora dos arquivos versionados. O painel público contém somente inventário e resumo agregado, com links para os arquivos.

O painel permite selecionar campos prioritários e registrar essa escolha no GitHub. Também pergunta o provedor de login da equipe. Essas escolhas não são aprovadas automaticamente. O aplicativo de consultas ainda é local e não está pronto para exposição pública com múltiplos usuários; login, permissões, hospedagem e cofre continuam pendentes.

## Validação

16 testes automatizados aprovados, incluindo período/leap day, inventário de listas e exportação de campos novos/nulos/textos longos. Excel real reaberto com 20 registros, 59 movimentos, 39 campos/caminhos no inventário e 907 valores originais. A abertura no Excel do Windows continua pendente.

O download da amostra pelo navegador Chromium foi realizado a partir da interface Streamlit e reaberto: 20 processos, 39 caminhos e 907 valores originais. O teste do painel também confirmou seleção de campos com registro estruturado, links de download e layout mobile.
