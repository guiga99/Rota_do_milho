# Checklist inicial

Marcado significa concluído com evidência; os demais itens permanecem pendentes. Ver [validação do incremento](VALIDACAO_INCREMENTO_1.md). Paginação multi-página está coberta com respostas controladas; a consulta real validou uma página, sem garantia de snapshot do acervo. Windows documentado, mas execução ainda não homologada. Resultados do piloto não substituem os testes da aplicação futura.

## Preparação

- [x] Definir TRF4 e até 100 candidatos como escopo inicial.
- [x] Extrair e preservar 103 termos do documento enviado.
- [x] Demonstrar consulta autenticada real ao DataJud no piloto (HTTP 200).
- [x] Registrar limitações observadas e tecnologias propostas.
- [ ] Confirmar documentação oficial vigente, autenticação, paginação e limites.
- [ ] Validar hierarquia e códigos oficiais de assuntos; aprovar mapeamentos.
- [ ] Revisar pertinência jurídica de uma amostra com o responsável jurídico.

## Incremento 1 — conexão

- [x] Fixar dependências e documentar execução no Windows e Linux.
- [x] Implementar leitura segura da chave e teste pela interface.
- [x] Distinguir erro de rede/TLS, 401/403, 429, timeout, 5xx e resposta inválida.
- [x] Validar tribunal e estrutura em consulta real de um registro.
- [x] Registrar diagnóstico sem credenciais e sem corpo sensível em logs.

## Incremento 2 — coleta e validação

- [x] Implementar paginação estável conforme API, com limite por CNJs únicos.
- [x] Registrar páginas recebidas, duplicidades e interrupções.
- [x] Preservar diferentes registros/graus do mesmo CNJ.
- [x] Armazenar JSON original, hash, consulta, horário e versão do coletor.
- [x] Validar CNJ, datas, estruturas e aderência aos filtros.
- [ ] Implementar regras de movimentos com códigos validados e evidências.
- [ ] Classificar qualidade técnica e revisão jurídica separadamente.
- [ ] Confirmar repetição sem perda de histórico ou duplicação indevida.

## Incremento 3 — interface e exportação

- [x] Construir Pesquisa, Resultados, Histórico e Configurações.
- [x] Diferenciar filtro remoto de filtro na amostra local.
- [x] Exibir campos indisponíveis e consultas parciais.
- [x] Exportar seleção ou consulta completa, com proveniência.
- [x] Reabrir XLSX e comparar dados, abas, contagens e tipos.
- [x] Preservar CNJ como texto e neutralizar fórmulas em conteúdo externo.
- [x] Testar download real no navegador.
- [ ] Confirmar abertura no Excel do Windows.

## Incremento 4 — publicação

- [ ] Definir hospedagem, persistência e provedor de autenticação.
- [ ] Restringir configurações ao administrador.
- [ ] Implementar armazenamento seguro e substituição de credenciais.
- [ ] Verificar ausência de segredos em logs, exportações e Git.
- [ ] Testar backup e restauração do banco e referências a respostas originais.
- [ ] Executar testes automatizados e teste real na hospedagem.
- [ ] Registrar pendências e obter aceite operacional e jurídico da amostra.

## Rotina de cada consulta

- [ ] Conectividade válida ou diagnóstico explícito.
- [ ] Filtros e horário registrados.
- [ ] Resultado: concluída, limite atingido, parcial ou falha.
- [ ] Contagens reconciliadas entre API, registros, CNJs e exportação.
- [ ] Ressalvas e fontes acessíveis ao operador.
- [ ] Arquivo gerado e verificado quando solicitado.
