# Checklist inicial

Marcado significa concluído com evidência; os demais itens permanecem pendentes. Ver [validação do incremento](VALIDACAO_INCREMENTO_1.md). Paginação multi-página está coberta com respostas controladas; a consulta real validou uma página, sem garantia de snapshot do acervo. Windows documentado, mas execução ainda não homologada. Resultados do piloto não substituem os testes da aplicação futura.

## Preparação

- [x] Definir TRF4 e até 100 candidatos como escopo inicial.
- [x] Extrair e preservar 103 termos do documento enviado.
- [x] Demonstrar consulta autenticada real ao DataJud no piloto (HTTP 200).
- [x] Registrar limitações observadas e tecnologias propostas.
- [ ] Confirmar documentação oficial vigente, autenticação, paginação e limites.
- [ ] Validar hierarquia e códigos oficiais de assuntos; aprovar mapeamentos.
- [ ] Revisar pertinência jurídica de uma amostra com o responsável jurídico.

## Incremento 1 — conexão

- [x] Fixar dependências e documentar execução no Windows e Linux.
- [x] Implementar leitura segura da chave e teste pela interface.
- [x] Distinguir erro de rede/TLS, 401/403, 429, timeout, 5xx e resposta inválida.
- [x] Validar tribunal e estrutura em consulta real de um registro.
- [x] Registrar diagnóstico sem credenciais e sem corpo sensível em logs.

## Incremento 2 — coleta e validação

- [x] Implementar paginação estável conforme API, com limite por CNJs únicos.
- [x] Registrar páginas recebidas, duplicidades e interrupções.
- [x] Preservar diferentes registros/graus do mesmo CNJ.
- [x] Armazenar JSON original, hash, consulta, horário e versão do coletor.
- [x] Validar CNJ, datas, estruturas e aderência aos filtros.
- [ ] Implementar regras de movimentos com códigos validados e evidências.
- [ ] Classificar qualidade técnica e revisão jurídica separadamente.
- [ ] Confirmar repetição sem perda de histórico ou duplicação indevida.

## Incremento 3 — interface e exportação

- [x] Construir Pesquisa, Resultados, Histórico e Configurações.
- [x] Diferenciar filtro remoto de filtro na amostra local.
- [x] Exibir campos indisponíveis e consultas parciais.
- [x] Exportar seleção ou consulta completa, com proveniência.
- [x] Reabrir XLSX e comparar dados, abas, contagens e tipos.
- [x] Preservar CNJ como texto e neutralizar fórmulas em conteúdo externo.
- [x] Testar download real no navegador.
- [ ] Confirmar abertura no Excel do Windows.

## Incremento 4 — publicação

- [ ] Definir hospedagem, persistência e provedor de autenticação.
- [x] Restringir configurações ao administrador.
- [ ] Implementar armazenamento seguro e substituição de credenciais.
- [ ] Verificar ausência de segredos em logs, exportações e Git.
- [ ] Testar backup e restauração do banco e referências a respostas originais.
- [ ] Executar testes automatizados e teste real na hospedagem.
- [ ] Registrar pendências e obter aceite operacional e jurídico da amostra.

## Rotina de cada consulta

- [ ] Conectividade válida ou diagnóstico explícito.
- [ ] Filtros e horário registrados.
- [ ] Resultado: concluída, limite atingido, parcial ou falha.
- [ ] Contagens reconciliadas entre API, registros, CNJs e exportação.
- [ ] Ressalvas e fontes acessíveis ao operador.
- [ ] Arquivo gerado e verificado quando solicitado.

## Orientações das issues #1 e #2

- [x] Consultar novamente a fonte real e preparar pelo menos 20 CNJs únicos.
- [x] Habilitar os últimos cinco anos como período padrão editável.
- [x] Inventariar todos os campos observados e exportar os valores originais, sem descartar campos novos.
- [x] Disponibilizar inventário e seleção de campos no painel de decisões.
- [x] Avaliar documentação oficial de Jusbrasil, Escavador e JUDIT.
- [ ] Confirmar campos prioritários com o responsável, após revisão da amostra.
- [ ] Obter acesso autorizado à fonte complementar escolhida e validar consulta real.
- [ ] Definir provedor de login e implantar acesso protegido para a equipe.
- [ ] Definir responsável pela revisão jurídica.

Evidências e limitações: [Incremento 2](INCREMENTO_2.md). Download público dos dois assets confirmado com HTTP 200, reabertura do Excel, teste do ZIP e conciliação do manifesto.

## Orientações da issue #3

- [x] Preservar JSON e permitir tabela principal personalizada com exportação própria.
- [x] Implementar OIDC Google e roles com allowlist exata, sem cadastro aberto.
- [x] Testar bloqueio sem configuração e ocultação de chave para operador.
- [x] Avaliar o link eproc e distinguir consulta humana de API.
- [x] Validar DataJud/TJSC real e habilitar consulta opcional por CNJ.
- [ ] Escolher hospedagem e configurar cliente OAuth/usuários no servidor.
- [ ] Executar login Google, callback e logout reais em homologação.
- [ ] Confirmar integração oficial eproc para dados complementares.

Evidências: [Incremento 3](INCREMENTO_3.md).

## Orientações da issue #4

- [x] Validar nova issue e registrar Streamlit Community Cloud como hospedagem escolhida.
- [x] Avaliar as cinco fontes em documentação/páginas oficiais, distinguindo documentação de consulta real.
- [x] Implementar PostgreSQL externo com TLS verificado e sem fallback local no Cloud.
- [x] Implementar entrypoint Cloud que exige Google antes de acessar histórico/dados.
- [x] Importar JSON Escavador/JUDIT com CNJ, arquivo original/hash, fonte/grau e inferências sinalizadas.
- [x] Exportar observações complementares sem alterar os originais DataJud.
- [ ] Escolher/provisionar PostgreSQL; configurar Secrets, Google OAuth e deploy na conta Streamlit.
- [ ] Homologar login/banco/consulta/exportação e backup/restauração na implantação real.
- [ ] Definir fornecedor/acesso/teto de custo e testar 3 CNJs antes de ampliar para 20.
- [ ] Aprovar informações e critérios jurídicos com responsável definido.

Detalhes: [Incremento 4](INCREMENTO_4.md), [roteiro Cloud](STREAMLIT_CLOUD.md), [comparação das fontes](FONTES_COMPLEMENTARES.md). Os testes locais/CI não substituem homologação no provedor escolhido.

## Revisão pela equipe — aprovação no chat

- [x] Implementar estados por campo/fonte e registrar comentário, evidência, revisor e data.
- [x] Preservar origem, propostas de correção e histórico separado por revisor.
- [x] Gravação transacional com bloqueio de versão antiga da mesma pessoa.
- [x] Exportar registros de revisão dos CNJs selecionados em XLSX e JSON.
- [ ] Homologar com contas Google reais dos colegas após ativação da aplicação.

Issue #5: Escavador, banco da equipe e teste sem cobrança escolhidos. Acesso privado/banco/OAuth permanecem pendentes. Ver [Revisão de campos](REVISAO_CAMPOS.md).

## Ativação Streamlit

- [x] Preparar roteiro de Create app com repositório, branch, entrypoint e Python definidos.
- [x] Implementar verificador dos Secrets/callback e teste de PostgreSQL somente leitura sem exibir credenciais.
- [ ] Responsável criar aplicação na conta Streamlit e informar somente a URL pública.
- [ ] Configurar OAuth web, usuários e PostgreSQL nos Secrets privados da aplicação.
- [ ] Executar login, consulta, revisão, download e reinício na implantação real.
