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
