'use strict';
const REPO = 'guiga99/Rota_do_milho';
const OWNER = 'guiga99';
const STORAGE = 'rota.decisoes.v1';
const MARKER = '<!-- rota-decisions:v1 -->';
const questions = [
 {id:'proxima_entrega',title:'Qual deve ser a próxima entrega?',description:'O MVP local já consulta o CNJ e exporta Excel. Há três caminhos possíveis para o próximo incremento.',suggestion:'Refinar a seleção jurídica primeiro reduz falsos positivos antes de ampliar o uso.',options:[['selecao_juridica','Refinar seleção jurídica','Validar assuntos, termos e evidências de trânsito.'],['consulta_online','Consulta pela Internet','Priorizar hospedagem protegida com login.'],['homologacao_windows','Validar no Windows','Conferir instalação, download e abertura no Excel.']]},
 {id:'periodo_padrao',title:'Qual período sugerir nas pesquisas?',description:'Processos antigos podem ser relevantes para trânsito em julgado. Um período restrito pode excluí-los.',suggestion:'Manter sem restrição de período como padrão, permitindo informar datas em cada pesquisa.',options:[['sem_restricao','Sem restrição de período','A consulta continua limitada a até 100 candidatos.'],['dez_anos','Últimos 10 anos','Sugestão inicial editável a cada consulta.'],['cinco_anos','Últimos 5 anos','Uma janela menor, também editável.']]},
 {id:'dados_complementares',title:'Como tratar os dados que o DataJud não fornece?',description:'Empresa, advogado, valor e teor da decisão não vieram na amostra do piloto.',suggestion:'Começar com revisão manual e fonte registrada, sem contratação automática de serviços.',options:[['manual','Revisão manual','Permitir complementar os dados com fonte e data.'],['avaliar_fontes','Avaliar outras fontes','Pesquisar alternativas; serviços pagos exigem nova decisão.'],['metadados','Só metadados por enquanto','Manter esses campos pendentes no primeiro ciclo.']]},
 {id:'acesso_aplicacao',title:'Quem deverá acessar a aplicação hospedada?',description:'Esta escolha orienta login, permissões e separação dos dados quando o MVP for hospedado.',suggestion:'Começar apenas com sua conta simplifica a primeira implantação protegida.',options:[['individual','Somente minha conta','Um operador e administração das integrações.'],['equipe','Minha equipe','Planejar convites e permissões; informar detalhes abaixo.'],['definir_depois','Definir depois','Prosseguir com o uso local enquanto decidimos.']]},
 {id:'revisao_juridica',title:'Quem revisará a pertinência dos resultados?',description:'A validação técnica não confirma decisão favorável nem crédito recuperável. Uma amostra precisa de revisão jurídica.',suggestion:'Definir o responsável pela revisão antes de aprovar as regras de seleção.',options:[['usuario','Eu farei a revisão','Você recebe uma amostra com evidências e ressalvas.'],['especialista','Um advogado da equipe','Identificar o papel ou a pessoa nas orientações, se desejar.'],['pendente','Ainda preciso definir','Manter resultados como candidatos sem aprovação jurídica.']]}
];
let draft = {decisions:{},note:''};
let records = [], latest = {}, availableStorage = true;
const $ = id => document.getElementById(id);
function node(tag,cls,text){const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=text;return e;}
function status(message){$('action-status').textContent=message;}
try {const d=JSON.parse(localStorage.getItem(STORAGE)||'null');if(d&&d.decisions&&typeof d.decisions==='object'){draft.decisions=d.decisions;draft.note=typeof d.note==='string'?d.note:'';}}catch{availableStorage=false;}
function saveLocal(){try{localStorage.setItem(STORAGE,JSON.stringify(draft));}catch{availableStorage=false;status('O navegador não permite guardar rascunhos. Baixe suas escolhas antes de sair.');}}
function selected(q){return draft.decisions[q.id]||latest[q.id]||{option:null,note:''};}
function differences(){return questions.filter(q=>{const d=draft.decisions[q.id],r=latest[q.id];return d&&(!r||d.option!==r.option||d.note!==r.note);});}
function render(){
 const root=$('questions');root.replaceChildren();
 for(const [index,q] of questions.entries()){
  const current=selected(q),remote=latest[q.id];
  const changed=differences().some(x=>x.id===q.id);
  const card=node('article','card');card.id='q-'+q.id;
  const top=node('div','card-top');top.append(node('span','card-number',String(index+1).padStart(2,'0')+' / DECISÃO'));
  top.append(node('span','status'+(changed?' draft':''),changed?'Rascunho local':remote?'Registrada no GitHub':'Aguardando sua escolha'));card.append(top);
  card.append(node('h3','',q.title),node('p','description',q.description),node('p','suggestion','Sugestão: '+q.suggestion));
  const options=node('div','options');options.setAttribute('role','group');options.setAttribute('aria-label',q.title);
  for(const [id,label,desc] of q.options){const b=node('button','option');b.type='button';b.setAttribute('aria-pressed',String(current.option===id));b.append(node('strong','',label),node('span','',desc));b.addEventListener('click',()=>{draft.decisions[q.id]={option:id,note:current.note||''};saveLocal();render();status('Escolha guardada como rascunho. Registre no GitHub para confirmar.');});options.append(b);}
  card.append(options);
  const label=node('label','', 'Sua orientação para esta decisão');label.htmlFor='note-'+q.id;card.append(label);
  const note=node('textarea');note.id=label.htmlFor;note.rows=2;note.maxLength=1000;note.value=current.note||'';note.placeholder='Opcional: ajuste, condição ou alternativa…';
  note.addEventListener('input',()=>{draft.decisions[q.id]={option:selected(q).option||null,note:note.value};saveLocal();updateCounts();});card.append(note);
  if(remote){const p=node('p','saved-detail','Registro: '+new Date(remote.date).toLocaleString('pt-BR')+' · ');const link=node('a','', '#'+remote.issue);link.href=remote.url;link.target='_blank';link.rel='noopener';p.append(link);card.append(p);}
  root.append(card);
 }
 updateCounts();
}
function updateCounts(){const changes=differences();for(const q of questions){const s=document.querySelector('#q-'+q.id+' .status');if(s){const changed=changes.some(x=>x.id===q.id);s.className='status'+(changed?' draft':'');s.textContent=changed?'Rascunho local':latest[q.id]?'Registrada no GitHub':'Aguardando sua escolha';}}$('count-total').textContent=questions.filter(q=>!latest[q.id]).length;$('count-draft').textContent=changes.length+(draft.note.trim()?1:0);$('count-saved').textContent=Object.keys(latest).length;$('save').disabled=!changes.length&&!draft.note.trim();}
function payload(){return {schema:'rota-decisions/v1',project:REPO,created_at:new Date().toISOString(),decisions:differences().map(q=>({id:q.id,question:q.title,option:draft.decisions[q.id].option||null,label:q.options.find(x=>x[0]===draft.decisions[q.id].option)?.[1]||'Orientação sem opção',note:(draft.decisions[q.id].note||'').trim()})),guidance:draft.note.trim()};}
function issueBody(p){const lines=[MARKER,'## Orientações do responsável pelo projeto','',...p.decisions.map(d=>`- **${d.question}**\n  - Escolha: ${d.label}\n  - Orientação: ${d.note||'—'}`),'',p.guidance?'### Orientação geral\n'+p.guidance:'','### Registro estruturado','```json',JSON.stringify(p,null,2),'```','','Registro enviado pelo painel de decisões. Não contém credenciais.'];return lines.join('\n');}
$('save').addEventListener('click',()=>{
 const p=payload();if(!p.decisions.length&&!p.guidance)return;
 const url=`https://github.com/${REPO}/issues/new?labels=decisoes&title=${encodeURIComponent('[Decisões] Orientações do MVP — '+new Date().toLocaleDateString('pt-BR'))}&body=${encodeURIComponent(issueBody(p))}`;
 if(url.length>8000){
  const dialog=node('dialog','long-record');const h=node('h2','','Seu registro tem um texto longo');
  const explain=node('p','','Copie o registro completo e cole no corpo da issue do GitHub. Depois confirme em Submit new issue.');
  const text=node('textarea');text.value=issueBody(p);text.readOnly=true;text.rows=10;text.setAttribute('aria-label','Registro completo para copiar');
  const copy=node('button','primary','Copiar registro e abrir GitHub ↗');
  copy.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(text.value);window.open(`https://github.com/${REPO}/issues/new?labels=decisoes&title=${encodeURIComponent('[Decisões] Orientações do MVP')}`,'_blank','noopener');status('Registro copiado. Cole no corpo da issue e confirme no GitHub.');dialog.close();dialog.remove();}catch{text.select();status('Selecione e copie o registro exibido. Abra uma nova issue com o rótulo decisoes.');}});
  const close=node('button','secondary','Voltar');close.addEventListener('click',()=>{dialog.close();dialog.remove();});dialog.append(h,explain,text,copy,close);document.body.append(dialog);dialog.showModal();return;
 }
 window.open(url,'_blank','noopener');status('Formulário aberto. Confirme em “Submit new issue” no GitHub. Suas escolhas ainda são rascunho até o registro aparecer no histórico.');
});
$('general-note').value=draft.note;
$('general-note').addEventListener('input',e=>{draft.note=e.target.value;saveLocal();updateCounts();});
$('export').addEventListener('click',()=>{const p={...payload(),confirmed:latest};const b=new Blob([JSON.stringify(p,null,2)],{type:'application/json'});const u=URL.createObjectURL(b);const a=node('a');a.href=u;a.download='rota-do-milho-decisoes.json';a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);status('Arquivo de escolhas baixado; isso não registra as respostas no GitHub.');});
$('discard').addEventListener('click',()=>{if(!confirm('Descartar somente os rascunhos deste navegador? Os registros no GitHub serão preservados.'))return;draft={decisions:{},note:''};$('general-note').value='';saveLocal();render();status('Rascunhos descartados.');});
function parseRecord(issue){
 if(issue.pull_request||issue.user?.login!==OWNER||!issue.body?.includes(MARKER))return null;
 const matches=[...issue.body.matchAll(/^```json[ \t]*\r?\n([\s\S]*?)^```[ \t]*$/gm)];const match=matches.at(-1);if(!match)return null;
 try{const p=JSON.parse(match[1]);if(p.schema!=='rota-decisions/v1'||p.project!==REPO||!Array.isArray(p.decisions))return null;
 const decisions=p.decisions.filter(d=>{const q=questions.find(q=>q.id===d.id);return q&&(d.option===null||q.options.some(o=>o[0]===d.option))&&typeof d.note==='string';});
 return {...p,decisions,issue:issue.number,date:issue.created_at,url:issue.html_url,guidance:typeof p.guidance==='string'?p.guidance:''};}catch{return null;}
}
function renderHistory(){const el=$('history');el.replaceChildren();for(const r of records){const box=node('article','history-item');const a=node('a','','Registro #'+r.issue+' · '+new Date(r.date).toLocaleString('pt-BR'));a.href=r.url;a.target='_blank';a.rel='noopener';box.append(a);for(const d of r.decisions){const q=questions.find(q=>q.id===d.id);box.append(node('p','',q.title+' '+(q.options.find(o=>o[0]===d.option)?.[1]||'Orientação sem opção')+(d.note?' — '+d.note:'')));}if(r.guidance)box.append(node('p','','Orientação geral: '+r.guidance));el.append(box);}}
async function sync(){
 $('refresh').disabled=true;$('sync-status').textContent='Consultando o histórico público no GitHub…';
 try{
  let issues=[],truncated=false;
  for(let page=1;page<=4;page++){
   const res=await fetch(`https://api.github.com/repos/${REPO}/issues?labels=decisoes&state=all&sort=created&direction=desc&per_page=100&page=${page}`,{headers:{Accept:'application/vnd.github+json'}});
   if(!res.ok)throw new Error(res.status===403||res.status===429?'Limite de consultas ao GitHub. Tente novamente mais tarde.':'Histórico temporariamente indisponível. HTTP '+res.status+'.');
   const part=await res.json();if(!Array.isArray(part))throw new Error('Resposta inesperada do histórico.');issues.push(...part);if(part.length<100)break;if(page===4)truncated=true;
  }
  records=issues.map(parseRecord).filter(Boolean).sort((a,b)=>b.issue-a.issue);latest={};
  for(const r of records)for(const d of r.decisions)if(!(d.id in latest))latest[d.id]={...d,date:r.date,issue:r.issue,url:r.url};
  // Apenas o responsável proprietário pode confirmar decisões; terceiros não alteram o painel.
  for(const q of questions){const d=draft.decisions[q.id],r=latest[q.id];if(d&&r&&d.option===r.option&&d.note.trim()===r.note.trim())delete draft.decisions[q.id];}
  if(draft.note.trim()&&records.some(r=>r.guidance.trim()===draft.note.trim())){draft.note='';$('general-note').value='';}
  saveLocal();render();renderHistory();
  $('sync-status').textContent=(records.length?records.length+' registro(s) confirmado(s) pela conta '+OWNER+'.':'Nenhum registro confirmado ainda. Faça suas escolhas acima.')+' Última atualização: '+new Date().toLocaleTimeString('pt-BR')+(truncated?' · Limite de leitura atingido; registros anteriores podem não estar exibidos.':'');
 }catch(e){$('sync-status').textContent=e.message+' Seus rascunhos foram preservados. Use o link do GitHub para consultar os registros.';}
 finally{$('refresh').disabled=false;}
}
$('refresh').addEventListener('click',sync);
render();sync();
