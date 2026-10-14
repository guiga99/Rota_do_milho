# Incremento 4 — issue #4

Data: 14/10/2026 UTC. [Registro do responsável](https://github.com/guiga99/Rota_do_milho/issues/4) validado pela conta, marcador e schema. Escolha: Streamlit Community Cloud, com persistência antes de dados operacionais. Orientação: estudar cinco fornecedores para sete campos que faltam no DataJud.

## Entrega

- Avaliação de Escavador, JUDIT, Vigilant/TrackJud, Codilo e Jusbrasil em [FONTES_COMPLEMENTARES](FONTES_COMPLEMENTARES.md). Recomendação: piloto Escavador e comparação JUDIT, condicionado a acesso/custo. Não há ranking de desempenho comprovado.
- `cloud_app.py` exige Google e PostgreSQL, sem permitir que modo local ou ausência de DSN libere consultas online. Modelo de Secrets e [roteiro de implantação](STREAMLIT_CLOUD.md).
- Adaptador PostgreSQL com TLS completo, pool limitado e erros sem credenciais. SQLite preservado para desenvolvimento local. Nenhuma migração/banco de produção criado.
- Importação administrativa de JSON Escavador/JUDIT para CNJ da consulta, com bytes UTF-8 recuperáveis, hash, data/autor, caminhos, fonte/grau. Inferências e ausências explícitas, importação idempotente/transacional. Arquivo importado não comprova consulta real.
- Excel inclui observações e fontes complementares, fragmenta textos longos, filtra a seleção e preserva os originais CNJ. Não promove candidatos a resultado jurídico.
- Painel registra hospedagem da issue #4 e apresenta decisões novas de fornecedor, persistência e teto, sem preencher respostas em nome do responsável.

## Validação e limites

Testes usam dados sintéticos, sem consulta comercial. Suite, navegador e integração PostgreSQL são executados nesta entrega; comandos e resultado consolidado em TESTES.md. CI inclui o PostgreSQL descartável com TLS e reinício. Nenhum XLSX/JSON individual, senha ou DSN real entra no Git.

Não houve deploy Streamlit, OAuth real, provisionamento de banco gerenciado, teste de backup/restauração ou requisição autenticada a fornecedor. Conta Streamlit/configuração privada, banco, fonte/teto e responsável jurídico continuam pendentes. O painel público foi atualizado; a aplicação de consultas continua disponível localmente enquanto a configuração online é concluída.
