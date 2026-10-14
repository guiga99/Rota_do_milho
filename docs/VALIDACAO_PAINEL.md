# Validação do painel de decisões

## Testes locais

Executado no Chromium em Linux, em 13/10/2026 no fuso America/Sao_Paulo. O script `tests/browser_decisoes.py` serve o painel localmente e intercepta os endpoints de respostas e do formulário. Nenhuma decisão de teste foi publicada no repositório.

Verificações aprovadas:

- Cinco perguntas renderizadas, sem opções aprovadas automaticamente.
- Escolha e orientação preservadas após recarregar a página.
- Formulário externo contém rótulo, marcador e JSON do registro.
- Abrir formulário não altera o status para confirmado.
- Histórico aceita somente registros estruturados da conta responsável `guiga99`.
- Respostas de terceiros são ignoradas.
- Rascunhos são reconciliados quando a resposta aparece no histórico.
- Texto é inserido sem interpretar HTML externo.
- Layout de 390 pixels sem rolagem horizontal.
- Respostas extensas têm fluxo de cópia sem truncamento.
- Download JSON contém respostas e referências confirmadas.
- Nenhuma exceção JavaScript durante o teste.

A suíte do MVP existente continua com 13 testes aprovados. Não foram realizadas consultas adicionais ao CNJ nesta entrega.

## Reproduzir

O painel estático não exige dependências para uso. Para o teste de navegador, instalar Playwright no ambiente de testes e disponibilizar Chromium (ou o navegador fornecido pelo Playwright); executar `python tests/browser_decisoes.py`. O script usa porta local temporária e encerra seu servidor ao terminar.

## Limites

O registro central usa autenticação e confirmação no GitHub. O painel não escreve diretamente na conta do usuário nem pede token. As opções em localStorage são rascunhos do navegador; somente issues estruturadas publicadas pelo responsável aparecem como registradas.

A publicação no GitHub Pages e a verificação HTTPS são etapas adicionais, documentadas em `DECISOES.md`. Uma verificação de leitura pública não equivale a testar a criação de uma decisão real; essa ação fica com o responsável. Nenhuma preferência foi aprovada pelo assistente.
