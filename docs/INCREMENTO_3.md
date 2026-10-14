# Incremento orientado pela issue #3

## Decisões aplicadas

- Login Google: suporte OIDC e autorização de equipe implementados, com operador/administrador. Configuração protegida e homologação real continuam requisitos externos.
- Tabela enxuta: colunas personalizáveis com sugestão inicial explícita, sem tratar a sugestão como campos já aprovados. A issue contém orientação textual, não uma lista de caminhos de campos.
- JSON completo preservado: tabela/exportação enxuta não altera o registro original. O Excel ganha TABELA_PRINCIPAL e mantém PROCESSOS, inventário e DADOS_ORIGINAIS.
- Comentário TJSC/eproc: pesquisa oficial e prova real DataJud documentadas em TJSC_EPROC.md. Consulta opcional por número CNJ, com fonte dinâmica. TRF4 permanece padrão.

## Validação

23 testes automatizados aprovados: regressões do MVP, tabela compacta com dados originais, autorização, ocultação de chaves, TJSC e rejeição de tribunal/número divergente. Duas operações reais DataJud/TJSC responderam HTTP 200 (conectividade e consulta por número). O Excel dessa consulta foi reaberto pelo exportador. Respostas individuais estão fora do Git.

## Pendências

- Escolher hospedagem com HTTPS e persistência; nova pergunta no painel.
- Criar cliente OAuth Google e informar configuração/usuários em área protegida.
- Homologar login/logout e callbacks reais no ambiente hospedado.
- Confirmar campos específicos após usar o inventário do painel ou o seletor do aplicativo.
- Para eproc, confirmar integração oficialmente autorizada antes de enriquecimento automático.

Nenhum cadastro OAuth, integração comercial ou implantação pública da aplicação Python foi inventado. Nenhum CAPTCHA foi contornado. A publicação do painel e sua leitura não equivalem à hospedagem do backend.

O download da tabela enxuta foi conferido no Chromium: 20 processos, seis colunas de sugestão inicial e 907 valores originais preservados no mesmo XLSX. A primeira consulta TJSC ordenada excedeu o timeout; a consulta exata por CNJ foi simplificada para não ordenar desnecessariamente e passou na validação real.

A [versão 2 do Excel](https://github.com/guiga99/Rota_do_milho/releases/download/amostra-trf4-20-v2/TRF4_amostra20.xlsx) reaproveita a amostra real anterior, acrescentando TABELA_PRINCIPAL. Não é uma nova coleta de 20 processos nem uma seleção de campos já aprovada pelo responsável. A versão anterior permanece disponível.

Publicação da versão 2 concluída pelo [workflow](https://github.com/guiga99/Rota_do_milho/actions/runs/38559155977). Excel e ZIP responderam HTTP 200; TABELA_PRINCIPAL possui 20 linhas de dados e seis colunas, DADOS_ORIGINAIS conserva 907 valores, e o JSON é idêntico à amostra original. [Suíte no GitHub](https://github.com/guiga99/Rota_do_milho/actions/runs/38559155448) também concluída com success.

Metadados de descoberta OIDC do Google acessíveis com HTTP 200 e emissor esperado; isso não valida o login sem cliente OAuth. O campo de hospedagem no painel está pendente de resposta e a aplicação Python permanece sem implantação pública.
