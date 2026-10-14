# Registro do piloto anterior

Este registro resume evidências locais de 13/10/2026. Não representa uma nova consulta nem testes da aplicação futura. As respostas individuais e a credencial não são publicadas aqui.

- Consulta mínima: HTTP 200; um registro e 14 movimentos retornados.
- Consulta filtrada: HTTP 200; 200 registros recebidos; primeiros 100 CNJs distintos exportados.
- Amostra exportada: 100 processos e 480 movimentações.
- Ordenação: data de ajuizamento decrescente. A amostra privilegiou processos recentes e não exigiu trânsito em julgado.
- Não houve movimento de trânsito identificado pelo detector inicial baseado em nome; esse resultado não prova inexistência de trânsito. O detector ainda precisa ser substituído por regras validadas.
- Campos observados: identificador, tribunal, grau, número, ajuizamento, sigilo, órgão, classe, sistema, formato, atualização, assuntos e movimentos.
- Partes, CNPJ, advogados, valor e teor da decisão não vieram na resposta.
- Os códigos foram observados em exploração do DataJud; seu mapeamento jurídico ainda é provisório.
- O arquivo gerado foi lido e verificado com OpenPyXL. O download pelo chat falhou para o usuário e a abertura no Excel do Windows não foi homologada.

## Requisição registrada (sem credencial)

```json
{
  "url": "https://api-publica.datajud.cnj.jus.br/api_publica_trf4/_search",
  "metodo": "POST",
  "consulta": {
    "size": 200,
    "query": {
      "terms": {
        "assuntos.codigo": [
          6060,
          6048,
          6045,
          6037,
          6041,
          6038,
          6062,
          6068,
          6065,
          6063,
          6059,
          6064,
          6058,
          6070
        ]
      }
    },
    "sort": [
      {
        "dataAjuizamento": {
          "order": "desc"
        }
      }
    ]
  },
  "data_utc": "2026-10-13T19:55:59.160945+00:00",
  "status": 200
}
```

SHA-256 do arquivo local `resposta_filtrada.json`: `a48c768dc0e8003337c47075b0cec585488547ff506193becf1ffd2cd3a92c54`.

O hash permite verificar correspondência com o arquivo original quando disponível; isoladamente não certifica origem nem substitui reprodução da consulta. A evidência original permanece fora do repositório.

A exploração inicial por texto retornou assuntos previdenciários e outros contextos, evidenciando a necessidade de refinar a seleção por códigos e validar a pertinência da amostra.
