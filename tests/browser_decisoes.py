"""Verifica o painel no Chromium sem publicar respostas de demonstração."""
import json
import re
import shutil
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).parents[1]
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(ROOT/'web/decisoes')))
thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
url=f'http://127.0.0.1:{server.server_port}'
results=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path=shutil.which('chromium'),headless=True,args=['--no-sandbox'])
  context=browser.new_context(viewport={'width':1440,'height':1000})
  remote=[];requests=[]
  def history(route):
   query=parse_qs(urlparse(route.request.url).query);requests.append(query)
   # Reproduz o filtro do GitHub: uma issue sem rótulo não aparece com labels.
   data=[i for i in remote if query['labels'][0] in i.get('labels',[])] if 'labels' in query else remote
   route.fulfill(json=data)
  context.route('https://api.github.com/repos/guiga99/Rota_do_milho/issues?**',history)
  context.route('https://github.com/**',lambda r:r.fulfill(body='<p>Formulário externo interceptado no teste</p>',content_type='text/html'))
  page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(url);page.get_by_text('Nenhum registro confirmado ainda.',exact=False).wait_for()
  assert page.locator('#questions .card').count()==20
  assert page.locator('#questions .card:visible').count()==10
  assert page.locator('#previous-questions .card').count()==10
  assert not page.locator('#materiais-anteriores').get_attribute('open')
  assert page.locator('#count-total').inner_text()=='20'
  assert page.locator('#questions a[href*=PAUTA_NEGOCIO]').count()>0
  assert page.locator('.option[aria-pressed="true"]').count()==0
  assert page.locator('#save').is_disabled()
  page.locator('#q-neg_cliente_pagante .option').first.click()
  page.locator('#note-neg_cliente_pagante').fill('Revisar primeiro o Sistema S.')
  page.locator('#general-note').fill('Orientação de teste; nunca publicar.')
  assert page.locator('#count-draft').inner_text()=='2'
  page.reload();page.get_by_text('Nenhum registro confirmado ainda.',exact=False).wait_for()
  assert page.locator('#note-neg_cliente_pagante').input_value()=='Revisar primeiro o Sistema S.'
  results.append('Escolhas sem aprovação automática e rascunho preservado após recarga')
  with page.expect_popup() as popup:page.locator('#save').click()
  opened=popup.value;opened.wait_for_load_state()
  query=parse_qs(urlparse(opened.url).query)
  assert query['labels']==['decisoes']
  body=query['body'][0];payload=json.loads(re.search(r'```json\s*([\s\S]*?)```',body)[1])
  assert payload['decisions'][0]['option']=='empresa'
  assert payload['decisions'][0]['id']=='neg_cliente_pagante'
  assert payload['context']=='reuniao-negocio-2026-10-15'
  assert page.locator('#count-saved').inner_text()=='0'
  results.append('Formulário GitHub com registro estruturado; abrir formulário não confirma resposta')
  issue={'number':10,'labels':[],'user':{'login':'guiga99'},'body':body,'created_at':'2026-10-14T00:00:00Z','html_url':'https://github.com/guiga99/Rota_do_milho/issues/10'}
  forged={**issue,'number':11,'user':{'login':'terceiro'}}
  remote.extend([forged,issue])
  page.wait_for_function('Date.now()-lastReturnRefresh>2500')
  page.evaluate("window.dispatchEvent(new Event('focus'))")
  page.get_by_text('1 registro(s) confirmado(s)',exact=False).wait_for()
  assert page.locator('#count-saved').inner_text()=='1'
  assert page.locator('#count-draft').inner_text()=='0'
  assert page.locator('.history-item').count()==1
  assert all('labels' not in q for q in requests)
  assert all('_' in q for q in requests)
  results.append('Ao voltar à aba, reconhece issue sem rótulo, ignora terceiros e reconcilia rascunhos')
  page.locator('#note-neg_cliente_pagante').fill('<img src=x onerror=alert(1)>')
  page.locator('#refresh').click();page.get_by_text('1 registro(s) confirmado(s)',exact=False).wait_for()
  assert page.locator('article.card img').count()==0
  results.append('Conteúdo externo é apresentado como texto, sem HTML executável')
  cloud_payload={'schema':'rota-decisions/v1','project':'guiga99/Rota_do_milho','decisions':[
      {'id':'hospedagem','option':'streamlit_cloud','note':'Piloto gerenciado sintético'}],'guidance':''}
  remote.append({**issue,'number':12,'body':'<!-- rota-decisions:v1 -->\n```json\n'+json.dumps(cloud_payload)+'\n```'})
  page.locator('#refresh').click();page.get_by_text('2 registro(s) confirmado(s)',exact=False).wait_for()
  assert page.locator('#q-hospedagem .status').text_content()=='Registrada no GitHub',page.locator('#q-hospedagem .status').text_content()
  for q in ['fornecedor_piloto','persistencia_cloud','orcamento_piloto']:
   assert page.locator('#q-'+q+' .option[aria-pressed="true"]').count()==0
  results.append('Hospedagem registrada é preservada; fornecedor, banco e teto continuam sem decisão automática')
  legal={'schema':'rota-decisions/v1','project':'guiga99/Rota_do_milho','decisions':[
      {'id':'revisao_juridica','option':'pendente','note':''}],'guidance':''}
  remote.append({**issue,'number':13,'body':'<!-- rota-decisions:v1 -->\n```json\n'+json.dumps(legal)+'\n```'})
  page.locator('#refresh').click();page.get_by_text('3 registro(s) confirmado(s)',exact=False).wait_for()
  assert page.locator('#q-revisao_juridica .status').inner_text()=='Pendência registrada'
  assert page.locator('#count-total').inner_text()=='19'
  assert page.locator('#count-saved').inner_text()=='1'
  legal['decisions'][0]['option']='especialista'
  remote.append({**issue,'number':14,'body':'<!-- rota-decisions:v1 -->\n```json\n'+json.dumps(legal)+'\n```'})
  page.locator('#refresh').click();page.get_by_text('4 registro(s) confirmado(s)',exact=False).wait_for()
  assert page.locator('#count-total').inner_text()=='18'
  assert page.locator('#count-saved').inner_text()=='2'
  results.append('Responsável jurídico adiado continua aberto; decisão posterior do responsável encerra a pendência')
  page.locator('#essential-only').uncheck()
  assert page.locator('#questions .card:visible').count()==20
  page.locator('#note-neg_ausencias').fill('Critério de teste escrito antes da escolha.')
  page.locator('#q-neg_ausencias .option').first.click()
  assert page.evaluate('payload().decisions.some(d=>d.id==="neg_ausencias")')
  assert page.locator('#note-neg_ausencias').input_value()=='Critério de teste escrito antes da escolha.'
  page.locator('#essential-only').check()
  assert page.locator('#q-neg_ausencias').is_hidden()
  results.append('20 perguntas de negócio, 10 essenciais, fontes e opção fora da pauta essencial preservada')
  page.locator('#materiais-anteriores > summary').click()
  page.get_by_text('Selecionar campos prioritários no inventário',exact=True).click()
  page.locator('#field-list input').first.wait_for()
  assert page.locator('#field-list input').count()==39
  page.locator('#field-list input[value="numeroProcesso"]').check()
  page.locator('#field-list input[value="movimentos[].nome"]').check()
  page.locator('#apply-fields').click()
  data=page.evaluate('payload()')
  chosen=next(d for d in data['decisions'] if d['id']=='campos_prioritarios')
  assert json.loads(chosen['note'])['campos_prioritarios']==['movimentos[].nome','numeroProcesso']
  assert chosen['option']=='personalizado'
  assert 'releases/download/amostra-trf4-20-v1' in page.get_by_role('link',name='Baixar Excel dos 20 processos').get_attribute('href')
  results.append('Inventário de 39 campos, escolha rastreável e links da amostra de 20 processos')
  page.locator('#materiais-anteriores > summary').click()
  page.set_viewport_size({'width':390,'height':844})
  assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
  results.append('Layout mobile sem rolagem horizontal')
  page.locator('#general-note').fill('á'*2000)
  for q in ['neg_cliente_pagante','neg_proposta_valor','neg_teses_piloto','neg_gate_lead','revisao_juridica']:
   page.locator('#note-'+q).fill('á'*1000)
  page.locator('#save').click();assert page.locator('dialog[open]').count()==1
  page.get_by_role('button',name='Voltar',exact=True).click()
  results.append('Respostas extensas têm fluxo de cópia, sem perder conteúdo')
  with page.expect_download() as download:page.locator('#export').click()
  dest=ROOT/'output/painel-escolhas-teste.json';dest.parent.mkdir(exist_ok=True);download.value.save_as(dest)
  assert json.loads(dest.read_text())['schema']=='rota-decisions/v1'
  results.append('Exportação JSON conserva escolhas e referências registradas')
  assert not errors,errors
  results.append('Nenhuma exceção JavaScript')
  browser.close()
finally:server.shutdown();server.server_close()
print('\n'.join('OK: '+r for r in results))
