# Avaliação do comentário extra: TJSC e eproc

Origem: orientação geral da issue #3, publicada pelo responsável em 14/10/2026. O comentário pede avaliar uma API a partir da consulta pública do tribunal de Santa Catarina.

## O que foi verificado

- [Link informado](https://eprocwebcon.tjsc.jus.br/consulta1g/externo_controlador.php?acao=processo_consulta_publica): HTTP 200, título “eproc - Consulta Processual - Busca de Processo”. O HTML contém um formulário POST, campos de número/chave e mecanismo de CAPTCHA/Cloudflare. Isso comprova uma interface humana; não documenta uma API para coleta em lote.
- [Portal oficial eproc](https://www.tjsc.jus.br/eproc): HTTP 200 e redirecionamento para a página oficial de processo eletrônico. [Perguntas frequentes](https://www.tjsc.jus.br/web/processo-eletronico-eproc/perguntas-frequentes) e [usuários externos](https://www.tjsc.jus.br/web/processo-eletronico-eproc/usuarios-externos) também responderam HTTP 200. Não foi identificada, nessas páginas consultadas, documentação pública de REST/SOAP para extração automática da consulta fornecida. Isso não prova inexistência de integrações institucionais.
- Endpoint CNJ `https://api-publica.datajud.cnj.jus.br/api_publica_tjsc/_search`: consulta autenticada real respondeu HTTP 200 e retornou `tribunal: TJSC`. Uma segunda consulta por número CNJ também funcionou e gerou Excel com a tabela principal e os valores originais.

A documentação wiki do DataJud continuou retornando HTTP 403 neste ambiente. O endpoint TJSC foi validado pela operação real, não pela página wiki nesta execução.

## Implicações para o projeto

1. Um site público e uma API são capacidades diferentes. Não usar chamadas internas, cookies ou URLs do formulário como contrato estável de integração, nem contornar CAPTCHA.
2. O DataJud já oferece uma rota para metadados TJSC. A versão nova permite consulta TJSC por CNJ e abertura manual do link eproc de primeiro grau, sem automação do portal.
3. TJSC é Justiça Estadual; TRF4 é Justiça Federal. Processos localizados em Santa Catarina podem pertencer à Justiça Federal vinculada ao TRF4. Trocar de tribunal muda o universo pesquisado; não reaplicar automaticamente filtros de contribuições federais ao TJSC. O TRF4 permanece a pesquisa tributária padrão.
4. A prova pequena no TJSC retornou o mesmo conjunto de raízes de metadados visto no TRF4. Partes, advogados, valor e decisão não vieram nesse registro. O teste não estabelece disponibilidade ou ausência desses campos em todo o acervo ou no portal eproc.
5. Enriquecimento no tribunal exige avaliar uma integração oficial, autorização e cobertura. Se ela não estiver documentada publicamente, obter esclarecimento pelo canal oficial; serviços como Jusbrasil, Escavador e JUDIT continuam alternativas a validar. Não foram enviados pedidos ou mensagens ao tribunal nesta etapa.

## Limites desta entrega

Não há coleta automática de partes/decisões do eproc, credencial institucional nem confirmação de API pública própria do portal. Não foi feita pesquisa nacional nem amostra tributária estadual. O suporte TJSC é uma consulta opcional por número, com proveniência própria; não substitui o objetivo inicial do TRF4.
