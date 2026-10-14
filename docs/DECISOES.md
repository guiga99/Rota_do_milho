# Painel de decisões e orientações

Endereço planejado: https://guiga99.github.io/Rota_do_milho/ . A publicação e a verificação de acesso devem ser confirmadas no relatório da entrega.

## Fluxo do responsável

1. Abra o painel, escolha opções e acrescente suas orientações.
2. Clique **Registrar no GitHub**. As opções escolhidas ainda são um rascunho.
3. Entre na conta `guiga99` e confirme em **Submit new issue** no formulário aberto.
4. Volte ao painel e use **Atualizar histórico**. O painel reconhecerá o registro e mostrará links para a evidência.

Uma pergunta pode receber uma orientação sem escolher uma das opções propostas. Não há escolha pré-aprovada. As sugestões são do assistente, não decisões do responsável.

Os rascunhos ficam no armazenamento local do navegador. Eles não são enviados ao GitHub ao clicar em uma opção. O registro confirmado é uma issue com o rótulo `decisoes`, marcador `<!-- rota-decisions:v1 -->` e bloco JSON com schema `rota-decisions/v1`. O botão de baixar escolhas oferece uma cópia, não substitui o registro central.

Para respostas extensas, o painel oferece copiar o registro completo e abrir o formulário; cole o conteúdo no corpo da issue e mantenha o rótulo `decisoes` antes de enviar. Não basta anexar o JSON: o painel lê o corpo da issue.

## Rastreabilidade

- Cada novo registro documenta suas escolhas, orientações, data e conta responsável.
- A resposta mais recente por pergunta substitui a anterior na visão atual. O histórico permanece disponível.
- Registros publicados por outras contas não aprovam decisões neste painel inicial.
- Se precisar mudar uma decisão, publique um novo registro pelo painel. Evite editar registros antigos, pois a precedência é pelo número da issue, não pela data da edição.
- Fechar uma issue significa encerrar seu acompanhamento; não apaga a decisão registrada.
- A leitura está limitada às 400 issues mais recentes com esse rótulo. O painel informa se houver truncamento.
- Orientações gerais ficam no histórico. Não mudam automaticamente o código.
- A API pública do GitHub tem limite de requisições. Em caso de erro, os rascunhos continuam disponíveis e o histórico pode ser lido diretamente no GitHub.

## Uso pelo assistente

Antes de um próximo incremento, consultar o histórico público:

`GET https://api.github.com/repos/guiga99/Rota_do_milho/issues?labels=decisoes&state=all&sort=created&direction=desc&per_page=100`

Validar conta autora, marcador, schema, projeto e IDs de perguntas. Consultar páginas seguintes quando necessário; a resposta mais recente de cada pergunta é a orientação vigente. Ler as orientações gerais, apontar conflitos com pedidos posteriores no chat e registrar no plano do incremento as decisões usadas. Nunca considerar escolhas de demonstração ou registros de terceiros como aprovação.

O assistente não recebe notificações automáticas nem trabalha continuamente depois de encerrar uma conversa. As respostas serão consultadas ao retomar o trabalho; o responsável pode avisar no chat que respondeu para iniciar a próxima etapa.

## Publicação e privacidade

HTML, CSS e JavaScript estáticos em `web/decisoes`, publicados no GitHub Pages pela branch `gh-pages`. O site não tem backend próprio, não pede token e não contém chaves API. O login e o registro são feitos diretamente no GitHub.

O repositório e as respostas são públicos. Não registrar credenciais, senhas, documentos individuais de processos ou informações reservadas nesse painel. Autenticação e confidencialidade para a futura aplicação de consultas continuam sendo uma etapa independente.

Para atualizar: publicar o commit em `main`, gerar o histórico da subpasta com `git subtree split --prefix=web/decisoes`, enviar a referência resultante para `gh-pages` e confirmar o site servido. Não criar worktrees; utilizar o checkout existente.
