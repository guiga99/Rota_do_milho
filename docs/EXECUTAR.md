# Executar o MVP local

## Windows

1. Instale Python 3.12 com o launcher `py`.
2. Baixe o repositório pelo botão **Code → Download ZIP** do GitHub e extraia, ou clone com Git.
3. Execute `iniciar_windows.bat` na pasta extraída. O script prepara o ambiente, instala as dependências e inicia a interface na conexão local.
4. Abra o endereço local exibido pelo Streamlit no navegador do computador.
5. Em **Configurações**, informe a chave DataJud e clique **Usar chave nesta sessão**, depois **Testar conexão**.
6. Em **Pesquisa**, selecione assuntos e limite (período padrão: últimos cinco anos, editável); clique **Consultar CNJ**.
7. Em **Resultados**, revise a qualidade, selecione CNJs e clique **Baixar XLSX verificado**. O arquivo vai para a pasta de downloads do navegador.

O script Windows foi escrito para esse fluxo, mas sua execução e a abertura no Excel do Windows ainda precisam de homologação. O aplicativo foi executado e testado em Linux/Python 3.12.

## Linux

Na raiz do repositório:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-lock.txt
.venv/bin/python -m streamlit run app.py --server.address 127.0.0.1 --browser.gatherUsageStats false
```

## Configuração e dados

- A chave digitada fica na sessão, sem gravação no SQLite. Também é possível definir `DATAJUD_API_KEY` no processo do servidor. Não incluir valores em arquivos versionados.
- Não há leitura automática de `.env` nesta versão.
- O banco fica em `data/runtime/consultas.sqlite3`. `ROTA_DATA_DIR` permite escolher outro diretório de armazenamento.
- Cada consulta tem seu próprio histórico; registros de origem diferentes são preservados. Não existe ainda um catálogo global de processos normalizado em tabelas separadas.
- O XLSX também contém inventário e todos os valores originais em abas próprias. O JSON completo sem credencial pode ser baixado em Resultados. Ele pode conter dados públicos de processos; mantenha o arquivo no local apropriado.
- Copie o banco somente com o aplicativo parado para um backup simples consistente. A restauração automatizada ainda não foi implementada.

## Testes

```bash
.venv/bin/python -m unittest discover -s tests -v
```

No Windows, use `.venv\Scripts\python.exe` em lugar de `.venv/bin/python`. Os testes automatizados usam respostas controladas e não exigem chave. O teste real do CNJ é uma etapa separada pela interface.

## Limitações

Aplicação local para um operador. Ainda sem login, cofre para cadastro persistente de credenciais ou implantação pública. Não expor o servidor na Internet até implementar e validar esses recursos. As regras de trânsito são indícios textuais explicitamente rotulados; a validação jurídica por códigos e o mapeamento dos 103 termos permanecem pendentes.
