# Rota do Milho

MVP para localizar processos tributários no DataJud/CNJ, revisar candidatos e exportar consultas em XLSX pelo navegador. Tribunal inicial: TRF4.

**Estado atual:** MVP local disponível; entrada protegida para Streamlit Community Cloud preparada. Configuração da chave em sessão, teste DataJud, pesquisa TRF4/TJSC, validação técnica, tabela configurável e XLSX. Histórico SQLite local ou PostgreSQL externo com TLS; importação de JSON Escavador/JUDIT com proveniência. Google OAuth real, provisionamento do banco, consultas comerciais autenticadas e hospedagem pública da aplicação Python permanecem pendentes.

Para iniciar, siga [Executar no Windows ou Linux](docs/EXECUTAR.md). No Windows com Python 3.12, execute `iniciar_windows.bat`.

## Painel de decisões

[Perguntas, escolhas e orientações do projeto](https://guiga99.github.io/Rota_do_milho/) — painel web estático. As escolhas são confirmadas em issues do GitHub; rascunhos locais não constituem aprovação. Veja [como registrar respostas](docs/DECISOES.md). A aplicação de consultas continua local nesta versão.

[Amostra real de 20 processos e relatório do incremento](docs/INCREMENTO_2.md). O painel permite baixar o Excel e escolher campos prioritários. O período padrão do aplicativo passou a ser os últimos cinco anos.

[Incremento da issue #3: tabela enxuta, login Google e avaliação TJSC/eproc](docs/INCREMENTO_3.md). [Como configurar o login da equipe](docs/ACESSO_GOOGLE.md). TJSC disponível como consulta opcional por número CNJ; o padrão tributário continua no TRF4.

[Incremento da issue #4: Cloud, persistência e fontes complementares](docs/INCREMENTO_4.md). [Implantar no Streamlit Cloud](docs/STREAMLIT_CLOUD.md): usar `cloud_app.py`, Google e PostgreSQL obrigatório. [Comparação dos cinco fornecedores e sete campos faltantes](docs/FONTES_COMPLEMENTARES.md).

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

Python 3.12+, Streamlit, cliente HTTP, SQLite/PostgreSQL e OpenPyXL. Dependências diretas em `requirements.txt`; conjunto instalado/testado em `requirements-lock.txt`.

## Limites da fonte

A resposta do piloto forneceu metadados e movimentações. Não forneceu partes, CNPJ, advogados, valor da causa ou teor das decisões. A pesquisa usa assuntos disponíveis; não equivale a busca textual em decisões. Os assuntos iniciais foram observados no piloto e ainda precisam de revisão jurídica. Processo candidato não comprova decisão favorável ou crédito recuperável.

Credenciais, JSONs de processos, banco e exportações locais não integram esta publicação. O histórico técnico agregado do piloto está documentado, sem publicar a amostra individual.
