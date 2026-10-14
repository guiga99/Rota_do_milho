# Configurações e credenciais

## DataJud

Configurar a chave por variável `DATAJUD_API_KEY` ou mecanismo de segredos do servidor. O valor não integra este repositório. Cabeçalho Authorization montado no servidor e removido de qualquer registro de diagnóstico.

A interface administrativa terá campo mascarado, salvar/substituir credencial e testar conexão. Após salvar, retornar apenas o estado configurado e o resultado do teste, nunca devolver o valor armazenado. Não exigir senha de tribunal para uma integração que usa somente API key.

Para cadastro persistente pela interface, usar cofre de segredos da hospedagem ou criptografia autenticada com chave mestra externa ao banco. Esta decisão deve ser implementada e testada antes da versão hospedada. Não guardar senha ou chave em texto simples no SQLite.

## Login da aplicação

Na hospedagem, usar provedor de identidade mantido e separar autenticação do usuário das credenciais das fontes. Configurações restritas ao administrador. Outros métodos (OAuth, tokens ou login do fornecedor) serão definidos somente quando uma integração complementar for aprovada.

## Dados e operação

- HTTPS com validação de certificado habilitada.
- Endpoints de integração previamente definidos; evitar envio de credencial a destino arbitrário.
- Logs estruturados sem cabeçalhos de autenticação, segredos ou dumps de ambiente.
- Backup protegido do banco e das evidências; política de retenção a definir antes da hospedagem.
- Banco, respostas individuais e XLSX fora do Git por padrão.
- Exportar apenas dados necessários; não acrescentar identificadores pessoais por inferência.
- Testar isolamento entre sessões antes de habilitar mais de um usuário.

O `.gitignore` é uma barreira auxiliar: revisar o conteúdo preparado para cada commit e executar verificação de segredos. Não incluir credenciais em exemplos, capturas ou fixtures.
