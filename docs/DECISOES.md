# Painel de decisões e orientações

Endereço publicado e verificado: https://guiga99.github.io/Rota_do_milho/ . GitHub Pages com status `built`, origem `gh-pages`, e HTML, JavaScript e CSS respondendo HTTP 200 com conteúdo igual aos arquivos do repositório.

## Fluxo do responsável

1. Abra o painel, escolha opções e acrescente suas orientações.
2. Clique **Registrar no GitHub**. As opções escolhidas ainda são um rascunho.
3. Entre na conta `guiga99` e confirme em **Submit new issue** no formulário aberto.
4. Volte à aba do painel: o histórico será atualizado automaticamente. O botão **Atualizar histórico** também permite forçar a leitura. O painel reconhecerá o registro e mostrará links para a evidência.

Uma pergunta pode receber uma orientação sem escolher uma das opções propostas. Não há escolha pré-aprovada. As sugestões são do assistente, não decisões do responsável.

Os rascunhos ficam no armazenamento local do navegador. Eles não são enviados ao GitHub ao clicar em uma opção. O registro confirmado é uma issue da conta responsável com marcador `<!-- rota-decisions:v1 -->` e bloco JSON com schema `rota-decisions/v1`. O botão de baixar escolhas oferece uma cópia, não substitui o registro central.

Para respostas extensas, o painel oferece copiar o registro completo e abrir o formulário; cole o conteúdo no corpo da issue antes de enviar. O rótulo `decisoes` é opcional. Não basta anexar o JSON: o painel lê o corpo da issue.

## Rastreabilidade

- Cada novo registro documenta suas escolhas, orientações, data e conta responsável.
- A resposta mais recente por pergunta substitui a anterior na visão atual. O histórico permanece disponível.
- Registros publicados por outras contas não aprovam decisões neste painel inicial.
- Se precisar mudar uma decisão, publique um novo registro pelo painel. Evite editar registros antigos, pois a precedência é pelo número da issue, não pela data da edição.
- Fechar uma issue significa encerrar seu acompanhamento; não apaga a decisão registrada.
- A leitura está limitada às 400 issues mais recentes do repositório. O painel informa se houver truncamento.
- Orientações gerais ficam no histórico. Não mudam automaticamente o código.
- A API pública do GitHub tem limite de requisições. Em caso de erro, os rascunhos continuam disponíveis e o histórico pode ser lido diretamente no GitHub.

## Uso pelo assistente

Antes de um próximo incremento, consultar o histórico público:

`GET https://api.github.com/repos/guiga99/Rota_do_milho/issues?state=all&sort=created&direction=desc&per_page=100`

O rótulo não é requisito: o GitHub pode não aplicar o parâmetro de rótulo do formulário. Validar conta autora, marcador, schema, projeto e IDs de perguntas. Consultar páginas seguintes quando necessário; a resposta mais recente de cada pergunta é a orientação vigente. Ler as orientações gerais, apontar conflitos com pedidos posteriores no chat e registrar no plano do incremento as decisões usadas. Nunca considerar escolhas de demonstração ou registros de terceiros como aprovação.

O assistente não recebe notificações automáticas nem trabalha continuamente depois de encerrar uma conversa. As respostas serão consultadas ao retomar o trabalho; o responsável pode avisar no chat que respondeu para iniciar a próxima etapa.

## Publicação e privacidade

HTML, CSS e JavaScript estáticos em `web/decisoes`, publicados no GitHub Pages pela branch `gh-pages`. O site não tem backend próprio, não pede token e não contém chaves API. O login e o registro são feitos diretamente no GitHub.

O repositório e as respostas são públicos. Não registrar credenciais, senhas, documentos individuais de processos ou informações reservadas nesse painel. Autenticação e confidencialidade para a futura aplicação de consultas continuam sendo uma etapa independente.

Para atualizar: publicar o commit em `main`, executar `python scripts/publicar_painel.py` e confirmar o site servido. O script usa `git commit-tree` para enviar somente a árvore estática para `gh-pages`, preservando a história de publicação, sem worktree ou alteração do checkout. Se o conteúdo já for igual, ele não publica novamente. O GitHub Pages já está configurado para essa branch.

## Amostra e novos campos

A seção Amostra oferece o Excel de 20 processos e ZIP com evidências. O inventário no site é agregado, sem dados individuais de processos. Marque os campos e clique **Usar esta seleção como rascunho**, depois **Registrar no GitHub**. A seleção fica no registro estruturado da pergunta `campos_prioritarios`, incluindo os caminhos originais. A pergunta `login_equipe` documenta o provedor preferido para a futura hospedagem. Nenhuma dessas duas decisões foi inferida a partir das respostas anteriores.

## Registro da issue #3

A escolha Google e a preferência por tabela enxuta foram implementadas no código. A orientação geral sobre TJSC/eproc foi avaliada e está em TJSC_EPROC.md. A nova pergunta `hospedagem` documenta o próximo requisito para o callback OAuth e a persistência; não enviar segredos ou lista de e-mails no registro público.

## Registro da issue #4

Streamlit Community Cloud escolhido, com persistência antes de uso operacional. Sete campos complementares e cinco fornecedores estudados: FONTES_COMPLEMENTARES.md. Entrada Cloud protegida, PostgreSQL e importação offline preparados; implantação e consulta comercial real permanecem pendentes. As novas perguntas `fornecedor_piloto`, `persistencia_cloud` e `orcamento_piloto` registram escolhas explícitas, sem contratação automática. Não inferir autorização de custo a partir de uma sugestão de fornecedor.

## Issue #5 e aprovação da revisão no chat

Issue #5 validada: Escavador, banco existente da equipe, teste sem cobrança. Não há autorização de compra/consumo pago. No chat, o responsável aprovou a revisão por colegas com Confirmado/Corrigir/Informação insuficiente; implementada conforme REVISAO_CAMPOS.md. Essa aprovação é documentada, sem criar uma issue em nome do usuário. Revisões privadas dos processos não são enviadas ao painel de decisões.

## Endereço Streamlit informado no chat

URL recebida: https://rotadomilho-dnvdghu9uyapphcp5gub6xj.streamlit.app/ . Callback ajustado no modelo público e no roteiro Google. Credenciais, lista privada e homologação online continuam pendentes. A URL é uma orientação do responsável; não foi criada issue em seu nome. Resposta HTTP da plataforma não equivale a validação do processo Python/login/banco.
