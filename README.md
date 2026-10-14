# Rota do Milho

MVP para localizar processos tributários no DataJud/CNJ, revisar candidatos e exportar consultas em XLSX pelo navegador. Tribunal inicial: TRF4.

**Estado atual:** planejamento e documentação inicial. Houve uma prova de consulta real anterior; a aplicação, o banco persistente, o login e a interface ainda não estão implementados neste repositório. Não há comando de instalação ou execução do aplicativo disponível nesta entrega.

## Documentação

- [Checklist inicial e entregas](docs/CHECKLIST.md)
- [Escopo, telas e critérios de aceite](docs/PLANO_MVP.md)
- [Arquitetura e modelo de dados](docs/ARQUITETURA.md)
- [Conectividade, qualidade e testes](docs/TESTES.md)
- [Configurações e credenciais](docs/SEGURANCA.md)
- [Registro do piloto real](docs/PILOTO.md)
- [Catálogo inicial e regras de pesquisa](docs/CATALOGO.md)
- [103 termos originais em CSV](data/catalogos/termos_originais.csv)

## Primeiro incremento

Configurar a chave DataJud → testar conexão real → consultar uma amostra pequena do TRF4 → validar metadados → revisar resultados → baixar XLSX pelo navegador.

Python 3.12+, Streamlit, cliente HTTP, SQLite e OpenPyXL são as tecnologias propostas. As dependências e suas versões serão fixadas na implementação.

## Limites da fonte

A resposta do piloto forneceu metadados e movimentações. Não forneceu partes, CNPJ, advogados, valor da causa ou teor das decisões. A pesquisa usa assuntos disponíveis; não equivale a busca textual em decisões. Processo candidato não comprova decisão favorável ou crédito recuperável.

Credenciais, JSONs de processos, banco e exportações locais não integram esta publicação. O histórico técnico agregado do piloto está documentado, sem publicar a amostra individual.
