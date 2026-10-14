# Revisão dos campos pela equipe

Implementado após aprovação “De acordo” no chat, em 14/10/2026. A consulta às issues também reconheceu a #5: Escavador, PostgreSQL da equipe e piloto sem cobrança. A implantação real continua dependendo da configuração privada Google/Streamlit/banco; não há URL da aplicação de pesquisas ativa nesta entrega.

## Fluxo do colega

1. Entrar na aplicação com sua conta Google autorizada e abrir uma consulta do Histórico.
2. Em **Resultados → Validar campos com a equipe**, escolher processo e campo/fonte/grau.
3. Conferir o valor original e marcar **Confirmado**, **Corrigir** ou **Informação insuficiente**. Nenhuma opção é marcada automaticamente.
4. Escrever comentário. Para confirmar/corrigir, informar fonte ou evidência; para corrigir, também informar valor proposto. Campo ausente não pode ser confirmado.
5. Salvar. O servidor atribui revisor da sessão e data UTC, preserva a origem e registra uma nova versão. Operadores e administradores autorizados podem revisar.
6. Consultar o histórico da equipe e baixar XLSX/JSON: a aba **REVISOES_CAMPOS** contém os registros dos CNJs exportados, incluindo valores originais/propostos, comentário, evidência, revisor/data e IDs.

Metadados disponíveis no JSON CNJ e sete campos complementares são revisáveis. Complementos importados aparecem vinculados ao fornecedor e observação. Um campo do DataJud ausente pode coexistir com observação de outro fornecedor: a revisão é da fonte/valor escolhido, não de todo o processo.

## Histórico e divergências

Cada avaliação aponta para o snapshot/valor de origem. Nova avaliação da mesma pessoa preserva a anterior e referencia seu ID. Avaliações de pessoas diferentes coexistem; divergências não são resolvidas automaticamente pela avaliação mais recente de outro colega. **Atual do revisor** indica a última versão daquela pessoa; **Origem vigente** verifica se o alvo ainda pertence ao snapshot atual.

Gravação transacional no SQLite/PostgreSQL preserva revisões simultâneas. Versão antiga da mesma pessoa em outra sessão é rejeitada com orientação para atualizar o Histórico. Falha de persistência recebe diagnóstico; o formulário não considera a revisão salva sem confirmação do banco.

Correções são propostas, sem substituir valores da fonte ou preencher automaticamente as colunas jurídicas de PROCESSOS. Confirmado representa a conferência declarada pelo colega; **não constitui aceite jurídico do processo, decisão favorável ou crédito recuperável**. O responsável jurídico continua pendente. Na implantação local de desenvolvimento, o revisor é “operador local”; identidade Google real depende da homologação OAuth.

Comentários/evidências e identidade da equipe ficam no histórico privado e nos downloads dos usuários autorizados. Não enviar dados individuais ao painel GitHub Pages nem às issues. Textos externos são protegidos contra fórmulas no Excel; valores originais longos são fragmentados.

## Validação

Suite: regras de autorização/estado/evidência, campos ausentes, preservação da origem, versões e divergências entre revisores, snapshot alterado, gravação concorrente/reabertura SQLite e seleção/segurança XLSX. Integração PostgreSQL: revisões simultâneas e recuperação após reinício com TLS verificado. Navegador: salvar avaliação e conferir downloads. Dados dos testes são sintéticos; não comprovam login Google ou implantação real.
