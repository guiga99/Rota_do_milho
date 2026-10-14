"""Consulta DataJud, evidências locais e validação técnica."""
import hashlib
import json
import re
import sqlite3
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import httpx

TRIBUNAIS = {'TRF4':'https://api-publica.datajud.cnj.jus.br/api_publica_trf4/_search','TJSC':'https://api-publica.datajud.cnj.jus.br/api_publica_tjsc/_search'}
ENDPOINT = TRIBUNAIS['TRF4']
ASSUNTOS = {6060:'Contribuição sobre a folha de salários',6048:'Contribuições Previdenciárias',6045:'SEBRAE, SESC, SENAC, SENAI e outros',6037:'Salário-Educação',6041:'Contribuição INCRA',6038:'Seguro Acidentes do Trabalho',6062:'1/3 de férias',6068:'Salário-Maternidade',6065:'Hora Extra',6063:'Auxílio-Alimentação',6059:'Reembolso auxílio-creche',6064:'Custeio de Assistência Médica',6058:'Indenização Trabalhista',6070:'Autônomos, Empresários (Pró-labore) e Facultativos'}

class ConsultaError(Exception):
    pass

def agora():
    return datetime.now(timezone.utc).isoformat()

def cnj_valido(n):
    if not isinstance(n,str) or not re.fullmatch(r'\d{20}', n):
        return False
    return int(n[7:9]) == 98 - int(n[:7] + n[9:] + '00') % 97

def data_valida(v):
    if not isinstance(v,str):
        return False
    try:
        if re.fullmatch(r'\d{14}',v):
            datetime.strptime(v,'%Y%m%d%H%M%S')
        else:
            datetime.fromisoformat(v.replace('Z','+00:00'))
        return True
    except ValueError:
        return False

def criar_query(codigos, inicio=None, fim=None, size=100):
    if not codigos:
        raise ConsultaError('Selecione ao menos um assunto.')
    filters=[{'terms':{'assuntos.codigo':list(codigos)}}]
    intervalo={}
    if inicio: intervalo['gte']=inicio.strftime('%Y%m%d')+'000000'
    if fim: intervalo['lte']=fim.strftime('%Y%m%d')+'235959'
    if inicio and fim and inicio>fim:
        raise ConsultaError('A data inicial deve anteceder a final.')
    if intervalo: filters.append({'range':{'dataAjuizamento':intervalo}})
    return {'size':size,'query':{'bool':{'filter':filters}},'sort':[{'dataAjuizamento':'desc'},{'id.keyword':'asc'}]}

class DataJud:
    def __init__(self,key,transport=None,tribunal="TRF4"):
        if tribunal not in TRIBUNAIS: raise ConsultaError("Tribunal não suportado.")
        self.tribunal=tribunal;self.endpoint=TRIBUNAIS[tribunal]
        if not key.strip(): raise ConsultaError('Configure a chave DataJud.')
        self.client=httpx.Client(timeout=40,transport=transport,follow_redirects=False,headers={'Authorization':'APIKey '+key.strip(),'Content-Type':'application/json'})
    def close(self): self.client.close()
    def request(self,q):
        for tentativa in range(3):
            try: r=self.client.post(self.endpoint,json=q)
            except httpx.TimeoutException: raise ConsultaError('Tempo limite excedido ao consultar o CNJ.') from None
            except httpx.RequestError: raise ConsultaError('Falha de conexão, proxy ou certificado HTTPS. Verifique a rede.') from None
            if r.status_code in (429,500,502,503,504) and tentativa<2:
                try: wait=min(10,max(0,float(r.headers.get('Retry-After',2**tentativa))))
                except ValueError: wait=2**tentativa
                time.sleep(wait);continue
            if r.status_code!=200:
                mensagem={401:'Chave recusada pelo CNJ.',403:'Acesso recusado: verifique permissão ou rede.',429:'Limite de requisições atingido.'}.get(r.status_code,'Serviço retornou erro.')
                raise ConsultaError(f'{mensagem} HTTP {r.status_code}.')
            try: d=r.json()
            except ValueError: raise ConsultaError('Resposta HTTP 200 não contém JSON válido.') from None
            hits=d.get('hits') if isinstance(d,dict) else None
            if not isinstance(hits,dict) or not isinstance(hits.get('hits'),list):
                raise ConsultaError('Resposta não contém a estrutura esperada do DataJud.')
            if d.get('timed_out') or d.get('_shards',{}).get('failed',0):
                raise ConsultaError('A API informou timeout ou falha parcial de processamento.')
            for h in hits['hits']:
                if not isinstance(h,dict) or not isinstance(h.get('_source'),dict): raise ConsultaError('Registro com estrutura inválida.')
                if h['_source'].get('tribunal')!=self.tribunal: raise ConsultaError('Resposta contém tribunal diferente do selecionado.')
                for field in ('classe','orgaoJulgador'):
                    if h['_source'].get(field) is not None and not isinstance(h['_source'][field],dict):
                        raise ConsultaError('Registro contém metadados com estrutura inválida.')
            return d
        raise ConsultaError('Serviço indisponível.')
    def teste(self):
        d=self.request({'size':1,'query':{'match_all':{}}})
        return {'data':agora(),'http':200,'registros':len(d['hits']['hits']),'campos':list(d['hits']['hits'][0]['_source']) if d['hits']['hits'] else []}

def normalizar(s,codigos,inicio=None,fim=None):
    n=s.get('numeroProcesso');problemas=[]
    if not cnj_valido(n): problemas.append('Número CNJ com formato ou dígito inválido')
    if not data_valida(s.get('dataAjuizamento')): problemas.append('Data de ajuizamento ausente ou inválida')
    assuntos=s.get('assuntos',[])
    if not isinstance(assuntos,list): assuntos=[];problemas.append('Estrutura de assuntos inválida')
    if codigos and not set(codigos)&{a.get('codigo') for a in assuntos if isinstance(a,dict)}: problemas.append('Assunto incompatível com filtro')
    date=s.get('dataAjuizamento','')
    if data_valida(date):
        day=datetime.strptime(date,'%Y%m%d%H%M%S').date() if re.fullmatch(r'\d{14}',date) else datetime.fromisoformat(date.replace('Z','+00:00')).date()
        if (inicio and day<inicio) or (fim and day>fim): problemas.append('Data fora do período solicitado')
        if day>datetime.now(timezone.utc).date(): problemas.append('Data de ajuizamento futura: revisar')
    moves=s.get('movimentos',[])
    if not isinstance(moves,list): moves=[];problemas.append('Estrutura de movimentos inválida')
    moves=[m for m in moves if isinstance(m,dict)]
    for m in moves:
        if not data_valida(m.get('dataHora')): problemas.append('Movimento com data ausente ou inválida');break
    # Indício textual explícito, ainda sem regra jurídica validada por código.
    tj=[m for m in moves if re.search(r'tr[aâ]nsit(?:o|ad[oa]).*julgad',str(m.get('nome') or ''),re.I)]
    return {'cnj':n,'origem_id':s.get('id'),'tribunal':s.get('tribunal'),'grau':s.get('grau'),'classe':(s.get('classe') or {}).get('nome'),'orgao':(s.get('orgaoJulgador') or {}).get('nome'),'assuntos':'; '.join(str(a.get('codigo'))+' — '+str(a.get('nome') or '') for a in assuntos if isinstance(a,dict)),'ajuizamento':s.get('dataAjuizamento'),'qualidade':'Não exportável' if not cnj_valido(n) else ('Com ressalvas' if problemas else 'Validado tecnicamente'),'ressalvas':'; '.join(dict.fromkeys(problemas)),'indicio_transito':bool(tj),'evidencia_transito':json.dumps(tj,ensure_ascii=False) if tj else None,'movimentos':moves,'original':s}

def conservar_anotacoes(result,previous):
    merged=dict(result)
    for field in ('revisoes','complementos'):
        items=list(previous.get(field,[]))
        def key(x):return x['id'] if field=='revisoes' else (x['fornecedor'],x['sha256_arquivo'])
        seen={key(x) for x in items}
        for x in result.get(field,[]):
            if key(x) not in seen:items.append(x);seen.add(key(x))
        if items:merged[field]=items
    return merged

class Store:
    def __init__(self,path):
        self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True)
        with self.connect() as c:c.execute('CREATE TABLE IF NOT EXISTS consultas (id TEXT PRIMARY KEY, criada TEXT, status TEXT, payload TEXT)')
    def connect(self): return sqlite3.connect(self.path)
    def salvar(self,result):
        with self.connect() as c:
            c.execute('BEGIN IMMEDIATE')
            row=c.execute('SELECT payload FROM consultas WHERE id=?',(result['id'],)).fetchone()
            payload=conservar_anotacoes(result,json.loads(row[0]) if row else {})
            c.execute('INSERT OR REPLACE INTO consultas VALUES (?,?,?,?)',(result['id'],result['criada'],result['status'],json.dumps(payload,ensure_ascii=False)))
    def listar(self):
        with self.connect() as c:return c.execute('SELECT id,criada,status FROM consultas ORDER BY criada DESC').fetchall()
    def obter(self,id):
        with self.connect() as c:row=c.execute('SELECT payload FROM consultas WHERE id=?',(id,)).fetchone()
        return json.loads(row[0]) if row else None
    def complementar(self,id,complemento):
        with self.connect() as c:
            c.execute('BEGIN IMMEDIATE')
            row=c.execute('SELECT payload FROM consultas WHERE id=?',(id,)).fetchone()
            if not row:raise ValueError('Consulta não encontrada no histórico.')
            result=json.loads(row[0]);existing=result.get('complementos',[])
            if any(x['sha256_arquivo']==complemento['sha256_arquivo'] and x['fornecedor']==complemento['fornecedor'] for x in existing):return result,False
            result['complementos']=[*existing,complemento]
            c.execute('UPDATE consultas SET payload=? WHERE id=?',(json.dumps(result,ensure_ascii=False),id))
            return result,True
    def revisar(self,id,**kwargs):
        from .reviews import registrar
        with self.connect() as c:
            c.execute('BEGIN IMMEDIATE')
            row=c.execute('SELECT payload FROM consultas WHERE id=?',(id,)).fetchone()
            if not row:raise ValueError('Consulta não encontrada no histórico.')
            result=registrar(json.loads(row[0]),**kwargs)
            c.execute('UPDATE consultas SET payload=? WHERE id=?',(json.dumps(result,ensure_ascii=False),id))
            return result

def coletar(api,store,codigos,limite=100,inicio=None,fim=None,numero=None):
    if not 1<=limite<=100: raise ConsultaError('O limite deve estar entre 1 e 100.')
    if numero is not None:
        if not cnj_valido(numero): raise ConsultaError('Número CNJ inválido. Informe 20 dígitos com dígito verificador válido.')
        query={'size':100,'query':{'term':{'numeroProcesso':numero}}}
    else: query=criar_query(codigos,inicio,fim,size=min(limite,100))
    result={'id':str(uuid.uuid4()),'criada':agora(),'status':'Em execução','endpoint':api.endpoint,'tribunal':api.tribunal,'query':query,'codigos':codigos,'paginas':[],'registros':[],'recebidos':0,'duplicados':0,'erro':None,'versao':'0.1.0'}
    cnjs=set();identidades=set();cursor=None
    try:
        for _ in range(30):
            q=json.loads(json.dumps(query))
            if cursor:q['search_after']=cursor
            d=api.request(q);raw=json.dumps(d,ensure_ascii=False,sort_keys=True)
            result['paginas'].append({'consulta':q,'resposta':d,'sha256':hashlib.sha256(raw.encode()).hexdigest(),'coletada':agora()})
            hits=d['hits']['hits'];result['total_api']=d['hits'].get('total');result['recebidos']+=len(hits)
            for h in hits:
                s=h['_source']
                if numero is not None and s.get('numeroProcesso')!=numero: raise ConsultaError('API retornou número CNJ diferente do solicitado.')
                identity=(s.get('id') or h.get('_id'),s.get('grau'),s.get('numeroProcesso'))
                if identity in identidades:result['duplicados']+=1;continue
                identidades.add(identity)
                normalized=normalizar(s,codigos,inicio,fim)
                n=normalized['cnj']
                if cnj_valido(n) and n not in cnjs and len(cnjs)>=limite: continue
                result['registros'].append(normalized)
                if cnj_valido(n):cnjs.add(n)
            result['cnjs_unicos']=len(cnjs)
            if numero is not None and len(hits)<query['size']:result['status']='Concluída';break
            if len(cnjs)>=limite:result['status']='Limite de amostra atingido';break
            if len(hits)<query['size']:result['status']='Concluída';break
            next_cursor=hits[-1].get('sort')
            if not next_cursor or next_cursor==cursor:raise ConsultaError('Paginação sem cursor válido; coleta parcial.')
            cursor=next_cursor
            store.salvar(result)
        else:raise ConsultaError('Limite operacional de páginas atingido; coleta parcial.')
    except ConsultaError as exc:
        result['erro']=str(exc);result['status']='Parcial' if result['paginas'] else 'Falha'
    result['cnjs_unicos']=len(cnjs);result['finalizada']=agora();store.salvar(result)
    return result
