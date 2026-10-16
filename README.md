# Rota do Milho

MVP para localizar processos tributários no DataJud/CNJ, revisar candidatos e exportar consultas em XLSX pelo navegador. Tribunal inicial: TRF4.

**Estado atual:** MVP local disponível; endereço Streamlit informado, com entrada protegida preparada. Configuração da chave em sessão, teste DataJud, pesquisa TRF4/TJSC, validação técnica, tabela configurável e XLSX. Histórico SQLite local ou PostgreSQL externo com TLS; importação JSON Escavador/JUDIT com proveniência. Google OAuth real, banco da equipe, consultas comerciais autenticadas e homologação online permanecem pendentes.

Para iniciar, siga [Executar no Windows ou Linux](docs/EXECUTAR.md). No Windows com Python 3.12, execute `iniciar_windows.bat`.

[Revisão de campos pela equipe](docs/REVISAO_CAMPOS.md): Confirmado, Corrigir ou Informação insuficiente, com comentário, evidência, revisor/data e histórico por pessoa. XLSX inclui REVISOES_CAMPOS. Implantação e login Google reais continuam pendentes.

**Endereço Streamlit informado:** https://rotadomilho-dnvdghu9uyapphcp5gub6xj.streamlit.app/ . Login e banco ainda precisam de configuração/homologação. Para a homologação técnica: [configurar o cliente OAuth Google e os Secrets privados](docs/ACESSO_GOOGLE.md#próxima-ação-na-conta-google). O roteiro inclui verificação dos Secrets e teste PostgreSQL somente leitura.

## Estratégia vigente

A [issue #6](https://github.com/guiga99/Rota_do_milho/issues/6) define atendimento à empresa contribuinte, abordagem inicial ao advogado, acompanhamento da recuperação e remuneração fixa pelo cálculo mais êxito. Escopo: 103 termos, trânsito em julgado nos últimos quatro anos independentemente do ajuizamento, piso de R$ 50 mil no piloto e prioridade para empresas com mais processos. Dois níveis de qualificação e encaminhamento a parceiros compõem o cenário.

Veja [estratégia, implicações e pendências](docs/ESTRATEGIA_NEGOCIO.md). As novas regras estão documentadas para desenvolvimento; o aplicativo ainda usa o filtro anterior de ajuizamento. Responsável jurídico, critérios detalhados e metas comerciais continuam pendentes. O próximo passo de negócio é validar a amostra e esses critérios.

## Painel de decisões

**Reunião de negócio de 15/10/2026:** [20 perguntas para criticar e validar a qualificação de leads](docs/PAUTA_NEGOCIO.md), com 10 essenciais, alternativas e notas no painel. Público/proposta, qualificação, abordagem/responsáveis e viabilidade/piloto; configuração de TI fora da pauta principal.

[Perguntas, escolhas e orientações do projeto](https://guiga99.github.io/Rota_do_milho/) — painel web estático. As escolhas são confirmadas em issues do GitHub; rascunhos locais não constituem aprovação. Veja [como registrar respostas](docs/DECISOES.md). Uso local disponível; acesso operacional no endereço Streamlit depende de homologação.

[Amostra real de 20 processos e relatório do incremento](docs/INCREMENTO_2.md). O painel permite baixar o Excel e escolher campos prioritários. O aplicativo ainda usa cinco anos de ajuizamento; a issue #6 substitui esse recorte no planejamento por quatro anos de trânsito em julgado.

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
