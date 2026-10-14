# Catálogo inicial de termos

`data/catalogos/termos_originais.csv` contém os 103 parágrafos de verbas do arquivo **verbas gui.docx**, na ordem recebida. As instruções e perguntas após a lista não foram tratadas como termos. IDs são posições atribuídas na extração; não são códigos oficiais CNJ.

A origem é o documento fornecido pelo usuário nesta sessão. O CSV preserva o texto original extraído; normalização, sinônimos e associações devem ficar em uma camada separada.

## Mapeamento futuro

Campos previstos: ID do termo, categoria, forma normalizada, sinônimos, código e nome oficiais, hierarquia/contexto tributário, URL da fonte, data de verificação, justificativa, prioridade e status (pendente, validado, rejeitado).

O código usado na consulta inicial foi observado no retorno real do DataJud. Isso não substitui validação da tabela oficial e de sua hierarquia. Um termo pode corresponder a vários assuntos ou não ter equivalente pesquisável nos metadados.

Não classificar toda verba como indenizatória. Não interpretar ausência de correspondência como ausência de processos. Não pesquisar descrição ou decisão se a fonte não expuser esse campo. No piloto, o nome do assunto veio em `assuntos.nome`.
