# Rota do Milho

MVP para localizar processos tributários no DataJud/CNJ, revisar candidatos e exportar consultas em XLSX pelo navegador. Tribunal inicial: TRF4.

**Estado atual:** primeiro MVP local implementado. Configuração da chave em sessão, teste DataJud, pesquisa TRF4, validação técnica, histórico SQLite e download XLSX pela interface. Login, cadastro persistente de credenciais e hospedagem pública permanecem pendentes.

Para iniciar, siga [Executar no Windows ou Linux](docs/EXECUTAR.md). No Windows com Python 3.12, execute `iniciar_windows.bat`.

## Painel de decisões

[Perguntas, escolhas e orientações do projeto](https://guiga99.github.io/Rota_do_milho/) — painel web estático. As escolhas são confirmadas em issues do GitHub; rascunhos locais não constituem aprovação. Veja [como registrar respostas](docs/DECISOES.md). A aplicação de consultas continua local nesta versão.

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

Python 3.12+, Streamlit, cliente HTTP, SQLite e OpenPyXL são as tecnologias propostas. As dependências diretas estão em `requirements.txt`; o conjunto instalado e testado está fixado em `requirements-lock.txt`.

## Limites da fonte

A resposta do piloto forneceu metadados e movimentações. Não forneceu partes, CNPJ, advogados, valor da causa ou teor das decisões. A pesquisa usa assuntos disponíveis; não equivale a busca textual em decisões. Os assuntos iniciais foram observados no piloto e ainda precisam de revisão jurídica. Processo candidato não comprova decisão favorável ou crédito recuperável.

Credenciais, JSONs de processos, banco e exportações locais não integram esta publicação. O histórico técnico agregado do piloto está documentado, sem publicar a amostra individual.
