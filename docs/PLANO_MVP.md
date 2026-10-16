# Plano do MVP

Direção vigente: [estratégia da issue #6](ESTRATEGIA_NEGOCIO.md). Este plano descreve o comportamento a desenvolver; regras novas de negócio ainda não estão implementadas.

## Objetivo e escopo

Apoiar a identificação e qualificação de empresas contribuintes para acompanhamento da recuperação tributária, começando pela interlocução com seus advogados. Consultar o TRF4, trabalhar os 103 termos, inspecionar evidências e exportar Excel com proveniência. O modelo comercial combina parcela fixa pelo cálculo e percentual de êxito; após validação, poderá ser oferecido a escritório parceiro. A amostra padrão terá até 100 CNJs únicos; o limite não representa o universo inteiro nem 100 oportunidades confirmadas.

O catálogo inicial contém 103 termos fornecidos pelo usuário. Seu mapeamento para a tabela oficial de assuntos precisa ser validado antes de ser considerado definitivo.

## Telas

| Tela | Comportamento esperado |
|---|---|
| Pesquisa | Tribunal TRF4, janela de trânsito de quatro anos com evidência, classes, assuntos, 103 termos mapeados e limite de CNJs; sem excluir ajuizamentos antigos |
| Resultados | Investigação e aptidão para proposta, acompanhamento separado, trânsito e valor com evidência, visão da empresa e seus processos, motivo da inclusão e registros por grau |
| Histórico | Filtros originais, contagens, status, respostas armazenadas e reexportação |
| Configurações | Integração DataJud, chave mascarada, teste de conexão e diagnóstico sanitizado |

Filtros enviados à API e filtros locais terão rótulos distintos. A quantidade exibida deve indicar se corresponde ao retorno remoto, à amostra ou ao resultado filtrado localmente. Totais com relação `gte` serão apresentados como limites inferiores, nunca como totais exatos.

## Pesquisa e revisão

1. Mapear termos para códigos e contexto tributário, com justificativa, fonte e status de revisão.
2. Testar a busca em uma amostra pequena e registrar falsos positivos na revisão jurídica.
3. Selecionar pela evidência de trânsito nos últimos quatro anos, sem usar ajuizamento como substituto. Validar códigos, documentos e datas; casos sem evidência ficam pendentes/em acompanhamento. Definir bordas da janela e sentido da ordenação antes de automatizar.
4. Explicar que um filtro local de trânsito não varre o acervo inteiro do tribunal.
5. Preservar evidências conflitantes e movimentos posteriores à indicação de trânsito.

Campos ausentes permanecem nulos. A issue #6 adota piso de R$ 50.000 apenas para o piloto, no contexto do valor da causa, e deixa a avaliação abaixo desse piso para depois. Confirmar campo/regra de corte e não habilitar filtro monetário nem de Fazenda Nacional sem fonte que forneça e permita validar esses campos. Valor da causa não é crédito recuperável. Priorizar empresas com mais processos, com associação comprovada e critérios de ranking ainda a definir. Ausência de retorno para um termo não comprova ausência de processos sobre a matéria.

## Entregas

| Etapa | Produto | Critério de conclusão |
|---|---|---|
| 1 | Configuração e consulta mínima | Teste autenticado real, JSON conferido e execução registrada |
| 2 | Coleta, validação e XLSX | Amostra de até 100 CNJs, contagens conciliadas, Excel reaberto automaticamente |
| 3 | Interface e histórico | Pesquisa, filtros, reexportação e download testados no navegador |
| 4 | Hospedagem protegida | Login, segredos, persistência, backup restaurado e consulta real na hospedagem |

A entrega 3 inclui confirmação de abertura no Excel do Windows. Se esse ambiente não estiver disponível ao desenvolvedor, registrar o teste como pendente e realizar homologação com o usuário.

## Fora da primeira versão

Coleta nacional, monitoramento agendado, integrações comerciais, raspagem de sites, leitura de decisões não disponibilizadas pelo DataJud e cálculo automático de crédito tributário. Fontes complementares serão avaliadas após medir as lacunas reais; serviços pagos dependem de autorização.

## Incremento de qualificação — issue #6

Acrescentar às entregas técnicas a validação do funil: investigação → apto a proposta; abordagem advogado/parceiro → relacionamento autorizado → empresa; atuação própria ou encaminhamento com motivo. Não confundir quantidade de processos com empresas únicas. Aprovação de campo não aprova oportunidade.

Aceite previsto: caso antigo com trânsito recente elegível; caso recente sem trânsito confirmado separado; valor e origem conferidos; processos/graus deduplicados para priorização; proposta com evidência, escopo e economia de atuação. Responsável jurídico, critérios de passagem, metas, prazo, regras de parceria e remuneração detalhada ainda precisam de definição. Ver [testes previstos](TESTES.md).

Acompanhamento comercial/manual dos demais casos faz parte da estratégia. Monitoramento automático agendado e cálculo automático continuam fora da versão atual. A entrega comercial de acompanhamento da recuperação não significa que o sistema já calcule ou recupere créditos.
