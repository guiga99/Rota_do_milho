"""Revisões atribuídas à identidade do servidor, vinculadas ao valor de origem."""
import hashlib
import json
import uuid
import re
from .core import agora
from .fields import inventario, extrair
from .enrichment import CAMPOS

ESTADOS=('Confirmado','Corrigir','Informação insuficiente')


def hash_json(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True).encode()).hexdigest()


def alvos(result):
    items=[]
    def add(cnj,source,grau,field,value,ref):
        items.append({'alvo_id':hash_json(ref),'cnj':cnj,'fonte':source,'grau':grau,
                      'campo':field,'valor_original':value,'referencia':ref})
    for i,r in enumerate(result['registros']):
        digest=hash_json(r['original'])
        for x in inventario([r]):
            f=x['campo']
            add(r['cnj'],'DataJud',r['grau'],f,extrair(r['original'],f),['DataJud',i,digest,f])
        for f in CAMPOS:
            value=r.get('evidencia_transito') if f=='evidencia_transito' else None
            add(r['cnj'],'DataJud',r['grau'],'complementar.'+f,value,['DataJud',i,digest,'complementar.'+f])
    for c in result.get('complementos',[]):
        for i,o in enumerate(c['observacoes']):
            add(c['cnj'],c['fornecedor'],o['grau'],o['campo'],o['valor'],
                [c['fornecedor'],c['sha256_arquivo'],i,o['caminho']])
    return items


def ultimas(result):
    latest={}
    for r in result.get('revisoes',[]):latest[(r['alvo_id'],r['revisor'])]=r
    return list(latest.values())


def minha_revisao(result, alvo_id, email):
    return next((r for r in ultimas(result) if r['alvo_id']==alvo_id and r['revisor']==email),None)


def registrar(result, alvo_id, estado, comentario, proposta, evidencia, identity, anterior=None):
    if result.get('status')=='Em execução':raise ValueError('Aguarde a coleta terminar antes de revisar seus campos.')
    if identity.get('role') not in ('admin','operator') or identity.get('mode') not in ('google','local') or not identity.get('email'):
        raise ValueError('Usuário não autorizado a revisar.')
    if estado not in ESTADOS:raise ValueError('Escolha um estado de revisão.')
    for value in (comentario,proposta,evidencia):
        if not isinstance(value,str) or len(value)>4000:raise ValueError('Textos da revisão devem ter até 4.000 caracteres.')
        if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',value):raise ValueError('Texto contém caracteres de controle inválidos.')
    target=next((t for t in alvos(result) if t['alvo_id']==alvo_id),None)
    if not target:raise ValueError('Campo de origem mudou ou não existe. Atualize a consulta antes de revisar.')
    if estado=='Confirmado' and target['valor_original'] in (None,'',[],{}):
        raise ValueError('Campo ausente não pode ser confirmado. Marque Informação insuficiente ou registre uma correção.')
    if not comentario.strip():raise ValueError('Informe um comentário sobre a conferência realizada.')
    if estado=='Corrigir' and not proposta.strip():raise ValueError('Informe o valor proposto para a correção.')
    if estado in ('Confirmado','Corrigir') and not evidencia.strip():raise ValueError('Informe a fonte ou evidência usada na conferência.')
    if estado!='Corrigir' and proposta.strip():raise ValueError('Valor proposto é permitido somente em Corrigir.')
    current=minha_revisao(result,alvo_id,identity['email'])
    if (current['id'] if current else None)!=anterior:
        raise ValueError('Sua revisão foi atualizada em outra sessão. Atualize o histórico antes de salvar.')
    row={**target,'id':str(uuid.uuid4()),'estado':estado,'comentario':comentario.strip(),
         'valor_proposto':proposta.strip() or None,'evidencia':evidencia.strip() or None,
         'revisor':identity['email'],'revisada_utc':agora(),'modo_identidade':identity['mode'],
         'substitui':anterior,'escopo':'Conferência de campo; não constitui aceite jurídico do processo.'}
    return {**result,'revisoes':[*result.get('revisoes',[]),row]}


def linhas_revisoes(result):
    active={r['id'] for r in ultimas(result)}
    targets={t['alvo_id'] for t in alvos(result)}
    for r in result.get('revisoes',[]):
        yield {'CNJ':r['cnj'],'Fonte':r['fonte'],'Grau':r['grau'],'Campo':r['campo'],
               'Estado':r['estado'],'Comentário':r['comentario'],'Valor original':json.dumps(r['valor_original'],ensure_ascii=False),
               'Valor proposto':r['valor_proposto'],'Evidência':r['evidencia'],'Revisor':r['revisor'],
               'Data UTC':r['revisada_utc'],'Atual do revisor':r['id'] in active,
               'Origem vigente':r['alvo_id'] in targets,'ID revisão':r['id'],'Substitui':r['substitui'],
               'Identidade':r['modo_identidade'],'Escopo':r['escopo']}
