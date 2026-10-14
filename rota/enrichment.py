"""Leitura de arquivos oficiais: candidatos com proveniência, sem conclusões jurídicas."""
import hashlib
import json
import re
from .core import agora, cnj_valido

FONTES = {
    'Escavador': 'https://api.escavador.com/v2/docs/consulta-de-processos',
    'JUDIT': 'https://lawsuits.production.judit.io/docs/spec',
}
CAMPOS = ('empresa','cnpj','advogado','polo_passivo','valor_causa','evidencia_transito','resultado_decisao')


def numero(value):
    return re.sub(r'[.\-\s]', '', str(value or ''))


def importar(raw, fornecedor, esperados, actor):
    if fornecedor not in FONTES:
        raise ValueError('Fornecedor não suportado por este importador.')
    if len(raw)>5*1024*1024:
        raise ValueError('Arquivo excede 5 MiB.')
    try:
        arquivo_original=raw.decode('utf-8')
        original=json.loads(arquivo_original.lstrip('\ufeff'))
    except (ValueError, UnicodeDecodeError, RecursionError):
        raise ValueError('Arquivo JSON UTF-8 inválido ou profundamente aninhado.') from None
    if not isinstance(original,dict):
        raise ValueError('Informe a resposta JSON de um único processo.')
    # Evita importar uma configuração de API no lugar da resposta processual.
    def sem_segredos(value):
        if isinstance(value,dict):
            for k,v in value.items():
                if str(k).casefold() in ('authorization','api_key','api-key','client_secret','access_token','cookie_secret'):
                    raise ValueError('Arquivo contém campos de credenciais; importe somente a resposta processual.')
                sem_segredos(v)
        elif isinstance(value,list):
            for v in value:sem_segredos(v)
    try:sem_segredos(original)
    except RecursionError:raise ValueError('Arquivo profundamente aninhado.') from None
    data=original
    prefix=''
    if fornecedor=='JUDIT' and isinstance(original.get('response_data'),dict):
        data=original['response_data'];prefix='response_data.'
    cnj=numero(data.get('numero_cnj') if fornecedor=='Escavador' else data.get('code'))
    if not cnj_valido(cnj) or cnj not in esperados:
        raise ValueError('O CNJ é inválido ou não pertence à consulta aberta.')
    obs=[]
    def add(field,value,path,grau=None,source=None,inferred=False):
        if value is None or value=='' or value==[] or value=={}:return
        obs.append({'campo':field,'valor':value,'caminho':prefix+path,'grau':grau,'origem_id':source,
                    'status':'inferido_fornecedor' if inferred else 'pendente_revisao'})
    if fornecedor=='Escavador':
        sources=data.get('fontes',[])
        if not isinstance(sources,list):raise ValueError('Estrutura fontes inválida.')
        for i,source in enumerate(sources):
            if not isinstance(source,dict):raise ValueError('Fonte processual inválida.')
            base=f'fontes[{i}]';grau=source.get('grau');sid=source.get('processo_fonte_id',source.get('id'))
            capa=source.get('capa') or {}
            if not isinstance(capa,dict):raise ValueError('Capa processual inválida.')
            add('valor_causa',capa.get('valor_causa'),base+'.capa.valor_causa',grau,sid)
            parties=source.get('envolvidos',[])
            if not isinstance(parties,list):raise ValueError('Envolvidos inválidos.')
            for j,p in enumerate(parties):
                if not isinstance(p,dict):raise ValueError('Parte processual inválida.')
                path=base+f'.envolvidos[{j}]'
                if p.get('tipo_pessoa')=='JURIDICA':add('empresa',{'nome':p.get('nome'),'polo':p.get('polo')},path,grau,sid)
                add('cnpj',p.get('cnpj'),path+'.cnpj',grau,sid)
                if p.get('polo')=='PASSIVO':add('polo_passivo',p.get('nome'),path+'.nome',grau,sid)
                if p.get('polo')=='ADVOGADO':add('advogado',{'nome':p.get('nome'),'oabs':p.get('oabs')},path,grau,sid)
                for k,lawyer in enumerate(p.get('advogados') or []):
                    if not isinstance(lawyer,dict):raise ValueError('Advogado inválido.')
                    add('advogado',{'nome':lawyer.get('nome'),'oabs':lawyer.get('oabs'),'parte':p.get('nome')},path+f'.advogados[{k}]',grau,sid)
        # Status predito e arquivamento não são evidência de trânsito/resultado.
    else:
        grau=data.get('instance');sid=data.get('id');add('valor_causa',data.get('amount'),'amount',grau,sid)
        parties=data.get('parties',[])
        if not isinstance(parties,list):raise ValueError('Partes inválidas.')
        for i,p in enumerate(parties):
            if not isinstance(p,dict):raise ValueError('Parte processual inválida.')
            path=f'parties[{i}]';inferred=p.get('was_inferred') is True
            if p.get('entity_type')=='company':add('empresa',{'nome':p.get('name'),'polo':p.get('side')},path,grau,sid,inferred)
            docs=p.get('documents') or []
            if not isinstance(docs,list):raise ValueError('Documentos inválidos.')
            for j,d in enumerate(docs):
                if not isinstance(d,dict):raise ValueError('Documento inválido.')
                if d.get('document_type')=='cnpj':add('cnpj',d.get('document'),path+f'.documents[{j}].document',grau,sid,inferred)
            # main_document pode ser CPF: só aproveita se a parte é empresa e tem 14 dígitos.
            main=p.get('main_document')
            if p.get('entity_type')=='company' and len(re.sub(r'\D','',str(main or '')))==14:
                add('cnpj',main,path+'.main_document',grau,sid,inferred)
            if str(p.get('side')).casefold()=='passive':add('polo_passivo',p.get('name'),path+'.name',grau,sid,inferred)
            for j,l in enumerate(p.get('lawyers') or []):
                if not isinstance(l,dict):raise ValueError('Advogado inválido.')
                add('advogado',{'nome':l.get('name'),'oab':l.get('oab'),'documentos':l.get('documents'),'parte':p.get('name')},path+f'.lawyers[{j}]',grau,sid,inferred or l.get('was_inferred') is True)
        steps=data.get('steps') or []
        if not isinstance(steps,list):raise ValueError('Movimentos inválidos.')
        for i,s in enumerate(steps):
            if not isinstance(s,dict):raise ValueError('Movimento inválido.')
            if re.search(r'tr[aâ]nsit(?:o|ad[oa]).*julgad',str(s.get('content') or ''),re.I):
                add('evidencia_transito',s,f'steps[{i}]',s.get('lawsuit_instance',grau),s.get('step_id'))
        for field in ('sentence','appeal_judgement'):
            add('resultado_decisao',data.get(field),field,grau,sid)
    for field in CAMPOS:
        if not any(o['campo']==field for o in obs):
            obs.append({'campo':field,'valor':None,'caminho':None,'grau':None,'origem_id':None,'status':'nao_fornecido'})
    return {'schema':'rota-enrichment/v1','cnj':cnj,'fornecedor':fornecedor,'documentacao':FONTES[fornecedor],
            'importada_utc':agora(),'importada_por':actor,'sha256_arquivo':hashlib.sha256(raw).hexdigest(),
            'autenticidade':'Arquivo importado pelo administrador; consulta autenticada não comprovada pelo importador.',
            'observacoes':obs,'original':original,'arquivo_original_utf8':arquivo_original}


def linhas(complementos):
    for c in complementos:
        for o in c['observacoes']:
            yield {'CNJ':c['cnj'],'Fornecedor':c['fornecedor'],'Campo':o['campo'],
                   'Valor informado':json.dumps(o['valor'],ensure_ascii=False) if o['valor'] is not None else None,
                   'Estado':o['status'],'Grau':o['grau'],'ID fonte':o['origem_id'],'Caminho JSON':o['caminho'],
                   'Importação UTC':c['importada_utc'],'SHA256 arquivo':c['sha256_arquivo']}
