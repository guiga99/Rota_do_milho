# Plano do MVP

## Objetivo e escopo

Permitir a um operador consultar o TRF4, filtrar candidatos tributários relacionados a contribuições sobre folha, inspecionar movimentações e baixar Excel com proveniência. A amostra padrão terá até 100 CNJs únicos; o limite não representa o universo inteiro nem 100 oportunidades confirmadas.

O catálogo inicial contém 103 termos fornecidos pelo usuário. Seu mapeamento para a tabela oficial de assuntos precisa ser validado antes de ser considerado definitivo.

## Telas

| Tela | Comportamento esperado |
|---|---|
| Pesquisa | Tribunal TRF4, período de ajuizamento, classes, assuntos, termos mapeados e limite de CNJs |
| Resultados | Seleção, filtros locais, motivo da inclusão, qualidade, detalhes e registros por grau |
| Histórico | Filtros originais, contagens, status, respostas armazenadas e reexportação |
| Configurações | Integração DataJud, chave mascarada, teste de conexão e diagnóstico sanitizado |

Filtros enviados à API e filtros locais terão rótulos distintos. A quantidade exibida deve indicar se corresponde ao retorno remoto, à amostra ou ao resultado filtrado localmente. Totais com relação `gte` serão apresentados como limites inferiores, nunca como totais exatos.

## Pesquisa e revisão

1. Mapear termos para códigos e contexto tributário, com justificativa, fonte e status de revisão.
2. Testar a busca em uma amostra pequena e registrar falsos positivos na revisão jurídica.
3. Oferecer busca por candidatos recentes e, após validação dos códigos de movimentos, busca por evidência de trânsito em julgado.
4. Explicar que um filtro local de trânsito não varre o acervo inteiro do tribunal.
5. Preservar evidências conflitantes e movimentos posteriores à indicação de trânsito.

Campos ausentes permanecem nulos. Não habilitar filtro de valor mínimo de R$ 50.000 nem de Fazenda Nacional sem fonte que forneça e permita validar esses campos. Ausência de retorno para um termo não comprova ausência de processos sobre a matéria.

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
