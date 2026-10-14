"""Inventário de todos os campos observados, sem inventar campos ausentes."""
import calendar
from datetime import datetime
from zoneinfo import ZoneInfo


def periodo_cinco_anos(today=None):
    today = today or datetime.now(ZoneInfo('America/Sao_Paulo')).date()
    year = today.year - 5
    return today.replace(year=year, day=min(today.day, calendar.monthrange(year, today.month)[1])), today


def tipo(value):
    if value is None: return 'null'
    if isinstance(value, bool): return 'boolean'
    if isinstance(value, dict): return 'object'
    if isinstance(value, list): return 'array'
    if isinstance(value, int): return 'integer'
    if isinstance(value, float): return 'number'
    return 'string'


def valores(value, path=''):
    """Caminhos com índices reais preservam todos os itens, incluindo vazios e nulos."""
    if isinstance(value, dict) and value:
        for key, item in value.items():
            yield from valores(item, f'{path}.{key}' if path else key)
    elif isinstance(value, list) and value:
        for index, item in enumerate(value):
            yield from valores(item, f'{path}[{index}]')
    else:
        yield path, tipo(value), value


def inventario(records):
    stats = {}
    for record in records:
        observed = set()
        def visit(value, path):
            if path:
                item = stats.setdefault(path, {'campo': path, 'tipos': set(), 'registros_presentes': 0, 'ocorrencias': 0, 'nulos': 0})
                item['tipos'].add(tipo(value)); item['ocorrencias'] += 1
                item['nulos'] += value is None
                if path not in observed:
                    item['registros_presentes'] += 1; observed.add(path)
            if isinstance(value, dict):
                for key, item in value.items(): visit(item, f'{path}.{key}' if path else key)
            elif isinstance(value, list):
                for item in value: visit(item, path + '[]')
        visit(record['original'], '')
    return [{**item, 'tipos': ', '.join(sorted(item['tipos'])), 'total_registros': len(records)} for _, item in sorted(stats.items())]


CAMPOS_PRINCIPAIS = ['numeroProcesso','classe.nome','assuntos[].nome','dataAjuizamento','grau']
ROTULOS = {'numeroProcesso':'Número CNJ','classe.nome':'Classe','assuntos[].nome':'Assuntos','dataAjuizamento':'Ajuizamento original','grau':'Grau'}


def extrair(source, path):
    def walk(value, parts):
        if not parts: return value
        part=parts[0];array=part.endswith('[]');key=part[:-2] if array else part
        if not isinstance(value,dict) or key not in value: return None
        child=value[key]
        if array:
            return [walk(item,parts[1:]) for item in child] if isinstance(child,list) else None
        return walk(child,parts[1:])
    return walk(source,path.split('.'))


def tabela_principal(records, fields):
    import json
    rows=[]
    for record in records:
        row={}
        for field in fields:
            value=extrair(record['original'],field)
            row[ROTULOS.get(field,field)]=json.dumps(value,ensure_ascii=False) if isinstance(value,(list,dict)) else value
        row['Qualidade técnica']=record['qualidade']
        rows.append(row)
    return rows
