# Estratégia de negócio — issue #6

Referência vigente: [issue #6](https://github.com/guiga99/Rota_do_milho/issues/6), publicada por `guiga99` em 16/10/2026 UTC (15/10 no horário de São Paulo). Conferidos autoria, marcador, schema `rota-decisions/v1`, projeto e os dez IDs do registro; sem comentários na consulta de 16/10/2026. As notas detalham as alternativas escolhidas e prevalecem sobre seus rótulos genéricos. Este documento adapta o escopo; não declara as novas regras implementadas ou o negócio validado.

## Definições adotadas

| Tema / ID | Diretriz registrada | Consequência para o projeto |
|---|---|---|
| Cliente / `neg_cliente_pagante` | Empresa contribuinte; aferir leads primeiro com seu advogado; depois considerar contato direto; oferecer o modelo validado a escritório parceiro | Separar cliente pagante, interlocutor inicial e parceiro de distribuição |
| Entrega / `neg_proposta_valor` | Acompanhamento da recuperação | Pesquisa e cálculo alimentam uma prestação de serviço; não bastará vender uma lista de processos |
| Matérias / `neg_teses_piloto` | Trabalhar os 103 termos e demandas, sem redução às três teses sugeridas na pergunta | Manter catálogo completo e medir cobertura/mapeamento por termo; 103 termos não equivalem a 103 teses juridicamente validadas |
| Janela / nota de `neg_teses_piloto` | Trânsito em julgado nos últimos quatro anos, independentemente de protocolo/distribuição | Substituir o recorte de cinco anos de ajuizamento para a seleção de negócio; registrar data de referência e evidência do trânsito |
| Qualificação / `neg_gate_lead` | Dois níveis: investigação e aptidão para proposta; valorizar clientes com mais processos | Distinguir estágios, associar processos à empresa com evidência e evitar contar graus duplicados como novos processos |
| Resultado / `neg_transito_resultado` | Prioridade para favorável/trânsito, com monitoramento dos demais | Separar fila prioritária de acompanhamento; não promover caso sem evidência a oportunidade confirmada |
| Piso / `neg_piso_economico` | R$ 50 mil apenas no piloto; avaliar valores menores posteriormente | A nota restringe o rótulo “Comparar faixas no piloto”: comparação abaixo do piso fica para etapa posterior |
| Revisão / `revisao_juridica` | Responsável ainda pendente; ordenar pela data de trânsito para análise | Ordenação não substitui aceite jurídico; sentido da ordenação não foi escolhido |
| Abordagem / `neg_abordagem` | Sequência B, C, A | Pelas opções do painel: advogado/parceiro → relacionamento autorizado → decisor da empresa |
| Receita / `neg_receita` | Valor fixo pela elaboração do cálculo + percentual de êxito | Modelo híbrido; valores, percentual, base de cálculo, cobrança e divisão com parceiro continuam abertos |
| Sucesso / `neg_sucesso_piloto` | Propostas viáveis; avaliar leads interessantes e destinar os demais a parceiro | Medir viabilidade e motivos de destinação; critérios e metas não foram definidos |

O piso é tratado no contexto da pergunta como **valor da causa**, não estimativa de crédito nem honorários. A issue não definiu agregação de valores por empresa; não somar causas para atingir o piso sem nova definição. Confirmar o campo e a regra inclusiva (por exemplo, ≥ R$ 50.000) antes de automatizar o corte.

## Fluxo de negócio a desenvolver

1. **Encontrar candidatos:** TRF4, catálogo dos 103 termos, até 100 CNJs únicos por amostra. Preservar matérias sem mapeamento como lacunas de cobertura, sem afirmar busca completa.
2. **Completar evidências:** empresa/CNPJ e sua posição no processo, advogado, contraparte, valor da causa, resultado e data/documento do trânsito. Dados faltantes ou conflitantes ficam identificados.
3. **Organizar a investigação:** aplicar o recorte de trânsito dos últimos quatro anos à fila prioritária, independentemente do ajuizamento; usar o piso do piloto quando houver valor validado. Ordenar por trânsito, com direção a definir. Manter acompanhamento separado para casos ainda não confirmados.
4. **Consolidar a visão do cliente:** mostrar processos distintos associados à mesma empresa e priorizar multiplicidade conforme critério a definir. A escolha formal entre CNPJ, grupo ou processo como unidade comercial continua pendente; não presumir vínculo entre empresas só por nome semelhante.
5. **Aferir a qualidade e avançar:** primeiro advogado/parceiro, depois relacionamento autorizado e, se necessário, empresa. Registrar resultado, impedimento, próxima ação e responsável. A passagem de investigação para apto a proposta depende de critérios e aceite ainda a definir.
6. **Preparar proposta viável:** acompanhamento da recuperação, com parcela fixa pelo cálculo e parcela de êxito. Confirmar disponibilidade do crédito, escopo e economia da atuação; valor da causa sozinho não demonstra viabilidade.
7. **Destinar e aprender:** atuação própria ou encaminhamento a parceiro, com motivo registrado. Separar menor atratividade comercial de falta de direito, informação ou impedimento; encaminhamento não torna um caso juridicamente apto. Após validação do modelo, avaliar oferta a escritório parceiro.

Os passos detalham requisitos propostos para executar a estratégia. Não autorizam contatos automáticos, compartilhamento de dados com parceiros, contratação ou consumo pago de APIs.

## Pontos de atenção e decisões ainda abertas

- **Janela versus monitoramento:** a nota exige trânsito em quatro anos e a alternativa prevê monitorar os demais. Interpretação de trabalho: corte na fila prioritária e acompanhamento separado. Definir destino de casos com trânsito anterior à janela e dos sem data confirmada; ausência não significa trânsito inexistente.
- **Temporalidade:** definir bordas da janela, tratamento de múltiplos trânsitos/decisões parciais e ordenação crescente ou decrescente. Quatro anos é recorte comercial, não afirmação sobre prazo jurídico ou disponibilidade de crédito.
- **Qualificação:** nomear responsável jurídico, substituto e critérios de passagem para proposta; confirmar quando verificar crédito já aproveitado, execução/compensação e impedimentos. A issue mantém explicitamente esse responsável pendente.
- **Prioridade de empresas:** definir quais processos contam, peso da quantidade frente a valor/resultado e regra de desempate. Não há pontuação aprovada.
- **Abordagem:** a nota do cliente menciona advogado → contribuinte; a nota específica de abordagem intercala relacionamento autorizado. Usar B → C → A como sequência detalhada e definir prazo/condição para avançar, sem presumir que recusa autoriza outra abordagem.
- **Parcerias:** definir “interessante”, motivos de encaminhamento, aceite do parceiro, responsabilidades e divisão de receita. Casos inviáveis ou impedidos precisam ter motivo preservado, sem serem tratados como bons leads.
- **Economia:** definir valor fixo, percentual, base/momento do êxito, riscos e custo/horas máximos; o teste de fontes continua sem cobrança conforme issue #5.
- **Validação do negócio:** propostas viáveis são o resultado escolhido, mas faltam meta, prazo, responsável e denominador. Proposta não equivale a contratação ou recuperação realizada.

## Indicadores propostos para validar o piloto

Registrar separadamente: CNJs analisados; empresas identificadas; processos por empresa; candidatos em investigação; aptos a proposta; pendências por campo; conversas por interlocutor; propostas viáveis; encaminhamentos e motivos; contratos; recuperações efetivas; horas e custos por etapa. Fixar os denominadores das conversões e evitar contar vários processos da mesma empresa como várias empresas. Estes indicadores são proposta de medição; não há metas aprovadas nem resultados comerciais comprovados.

## Diferença entre direção aprovada e aplicação atual

O código ainda usa período de ajuizamento editável, com padrão de cinco anos, e não implementa o funil comercial, o novo corte por trânsito, ranking por empresa, piso monetário ou fluxo com parceiros. A revisão por campo existente também não constitui aceite jurídico de um lead. As amostras anteriores são evidência de coleta e precisam ser reavaliadas para este novo recorte.

Próximo incremento proposto: validar evidências de trânsito/valor/empresa numa amostra; resolver as regras abertas; então implementar seleção temporal, filas, visão por empresa e rastreio de qualificação/encaminhamento. Não reutilizar ajuizamento, baixa ou arquivamento como substitutos de trânsito. Consultas limitadas a uma amostra não comprovam cobertura de todo o tribunal.

Continuam vigentes TRF4 inicial, acesso da equipe, Google/Streamlit, banco existente e Escavador em teste sem cobrança. Implantação real e fontes autenticadas permanecem com suas pendências anteriores. Ver [plano](PLANO_MVP.md), [checklist](CHECKLIST.md) e [aceite previsto](TESTES.md).
