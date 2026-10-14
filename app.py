"""MVP DataJud com desenvolvimento local ou autenticação Google da equipe."""
import csv,json,os
from pathlib import Path
import streamlit as st
from rota.core import ASSUNTOS,TRIBUNAIS,ConsultaError,DataJud,coletar
from rota.export import exportar
from rota.fields import inventario, periodo_cinco_anos, CAMPOS_PRINCIPAIS, tabela_principal
from rota.access import proteger
from rota.storage import criar_store, StorageError
from rota.enrichment import FONTES, importar, linhas
from rota.reviews import ESTADOS, alvos, minha_revisao, linhas_revisoes

ROOT=Path(__file__).parent
st.set_page_config(page_title='Rota do Milho',page_icon='🌽',layout='wide')
st.title('Rota do Milho')
st.caption('Pesquisa tributária no TRF4 · TJSC por número CNJ · revisão jurídica necessária')
try: settings=st.secrets.to_dict()
except FileNotFoundError: settings={}
cloud=globals().get('ROTA_CLOUD',False)
identity=proteger(st,'google' if cloud else os.getenv('ROTA_AUTH_MODE',settings.get('access',{}).get('mode','local')),settings)
if identity['mode']=='google':
    st.sidebar.caption('Conta autorizada: '+identity['email'])
    if st.sidebar.button('Sair da conta'):st.session_state.clear();st.logout()
    st.sidebar.caption('Perfil: administrador' if identity['role']=='admin' else 'Perfil: operador')

@st.cache_resource
def conectar_historico(url, data_dir, online):
    return criar_store({'database':{'url':url}}, data_dir, cloud=online)
try:
    store=conectar_historico(settings.get('database',{}).get('url'),os.getenv('ROTA_DATA_DIR',str(ROOT/'data/runtime')),cloud)
except StorageError as e:
    st.error(str(e));st.stop()
if 'api_key' not in st.session_state:st.session_state.api_key=os.getenv('DATAJUD_API_KEY',settings.get('datajud',{}).get('api_key',''))
config,pesquisa,resultados,historico=st.tabs(['Configurações','Pesquisa','Resultados','Histórico'])
with config:
    if identity['role']!='admin':
        st.info('A configuração das integrações é restrita aos administradores da equipe.')
    else:
        st.subheader('Conexão DataJud')
        st.info('A chave digitada fica somente nesta sessão e será perdida ao encerrá-la. Para inicialização automática, configure DATAJUD_API_KEY no servidor.')
        with st.form('config'):
            key=st.text_input('Chave API DataJud',type='password',value=st.session_state.api_key)
            salvar=st.form_submit_button('Usar chave nesta sessão')
            if salvar:st.session_state.api_key=key.strip();st.success('Configuração aplicada à sessão.')
        tribunal_teste=st.selectbox('Tribunal para teste de conexão',list(TRIBUNAIS))
        if st.button('Testar conexão'):
            api=None
            try:
                api=DataJud(st.session_state.api_key,tribunal=tribunal_teste)
                with st.spinner('Consultando CNJ…'):test=api.teste()
                st.session_state.teste=test
                st.success(f"HTTP 200 · {test['registros']} registro(s) · {test['data']}")
                st.write('Campos disponíveis:',test['campos'])
            except (ConsultaError,StorageError) as e:st.error(str(e))
            finally:
                if api:api.close()
with pesquisa:
    tribunal=st.selectbox('Tribunal da consulta',list(TRIBUNAIS))
    if tribunal=='TJSC':
        st.info('TJSC é Justiça Estadual. Esta expansão consulta metadados por CNJ e não aplica automaticamente o recorte federal do TRF4. O portal eproc é uma consulta humana separada.')
        st.link_button('Abrir consulta pública eproc TJSC (1º grau)','https://eprocwebcon.tjsc.jus.br/consulta1g/externo_controlador.php?acao=processo_consulta_publica')
        with st.form('consulta_numero'):
            numero=st.text_input('Número CNJ (20 dígitos; pontuação opcional)')
            buscar_numero=st.form_submit_button('Consultar CNJ no TJSC')
        if buscar_numero:
            api=None
            try:
                api=DataJud(st.session_state.api_key,tribunal='TJSC')
                import re
                with st.spinner('Consultando metadados TJSC…'):res=coletar(api,store,[],limite=1,numero=re.sub(r'[.\-\s]','',numero))
                res['executada_por']=identity['email'];store.salvar(res);st.session_state.result=res
                if res.get('erro'):st.warning(res['erro'])
                else:st.success(f"{res['status']} · {res['cnjs_unicos']} CNJs únicos. Abra Resultados.")
            except (ConsultaError,StorageError) as e:st.error(str(e))
            finally:
                if api:api.close()
    else:
        st.subheader('Consulta tributária ao TRF4')
        st.warning('Os assuntos abaixo foram observados no piloto. O mapeamento jurídico dos 103 termos ainda está pendente. Não há busca em textos de decisões.')
        with st.form('pesquisar'):
            codes=st.multiselect('Assuntos enviados ao CNJ',list(ASSUNTOS),default=[6060,6048,6045],format_func=lambda x:f'{x} — {ASSUNTOS[x]}')
            usar_periodo=st.checkbox('Filtrar por período de ajuizamento', value=True)
            inicio_padrao,fim_padrao=periodo_cinco_anos()
            a,b=st.columns(2)
            inicio=a.date_input('De',value=inicio_padrao);fim=b.date_input('Até',value=fim_padrao)
            limite=st.number_input('Limite de processos únicos',min_value=1,max_value=100,value=100)
            buscar=st.form_submit_button('Consultar CNJ')
        if buscar:
            api=None
            try:
                api=DataJud(st.session_state.api_key)
                with st.spinner('Consultando e validando…'):res=coletar(api,store,codes,int(limite),inicio if usar_periodo else None,fim if usar_periodo else None)
                res['executada_por']=identity['email'];store.salvar(res);st.session_state.result=res
                if res.get('erro'):st.warning(res['erro'])
                else:st.success(f"{res['status']} · {res['cnjs_unicos']} CNJs únicos. Abra Resultados.")
            except (ConsultaError,StorageError) as e:st.error(str(e))
            finally:
                if api:api.close()
    with st.expander('103 termos originais — catálogo pendente de mapeamento'):
        with (ROOT/'data/catalogos/termos_originais.csv').open(encoding='utf-8-sig') as f:st.dataframe(list(csv.DictReader(f)),hide_index=True)
with historico:
    try:history=store.listar()
    except StorageError as e:st.error(str(e));history=[]
    st.caption('Histórico em PostgreSQL externo.' if settings.get('database',{}).get('url') else 'Histórico local em SQLite.')
    if history:
        id=st.selectbox('Consulta anterior',[r[0] for r in history],format_func=lambda x:next(f'{r[1]} · {r[2]} · {r[0][:8]}' for r in history if r[0]==x))
        if st.button('Abrir consulta'):
            try:st.session_state.result=store.obter(id);st.rerun()
            except StorageError as e:st.error(str(e))
    else:st.info('Nenhuma consulta registrada.')
with resultados:
    res=st.session_state.get('result')
    if not res:st.info('Execute uma pesquisa ou abra uma consulta do histórico.')
    else:
        st.write(f"**{res['status']}** · {res['cnjs_unicos']} CNJs · {res['recebidos']} registros recebidos")
        if res.get('erro'):st.warning(res['erro'])
        st.caption('Filtros abaixo atuam somente sobre a amostra coletada. Registros do mesmo processo em graus diferentes são preservados.')
        with st.expander('Validar campos com a equipe'):
            st.caption('Sua avaliação fica vinculada à conta e ao valor desta fonte. Comentário é obrigatório; confirmação e correção exigem evidência. Conferência de campo não constitui aceite jurídico do processo.')
            opcoes=alvos(res)
            numero_revisao=st.selectbox('Processo para revisar',list(dict.fromkeys(t['cnj'] for t in opcoes)),key='revisar_cnj_'+res['id'])
            do_processo=[t for t in opcoes if t['cnj']==numero_revisao]
            if do_processo:
                target=st.selectbox('Campo e fonte para revisar',do_processo,format_func=lambda t:f"{t['campo']} · {t['fonte']} · grau {t['grau']} · {t['alvo_id'][:8]}",key='revisar_alvo_'+res['id'])
                st.write('Valor da fonte:');st.json(target['valor_original'])
                current=minha_revisao(res,target['alvo_id'],identity['email'])
                if current:st.info(f"Sua última avaliação: {current['estado']} · {current['revisada_utc']}")
                with st.form('revisao_'+res['id']+'_'+target['alvo_id']+'_'+(current['id'] if current else 'nova')):
                    estado=st.radio('Resultado da conferência',ESTADOS,index=None)
                    comentario=st.text_area('Comentário da revisão',max_chars=4000)
                    proposta=st.text_area('Valor proposto (somente se Corrigir)',max_chars=4000)
                    evidencia=st.text_area('Fonte ou evidência da conferência',max_chars=4000,help='Informe referência, documento ou trecho que permita verificar a conclusão.')
                    gravar=st.form_submit_button('Salvar revisão do campo')
                if gravar:
                    try:
                        atualizado=store.revisar(res['id'],alvo_id=target['alvo_id'],estado=estado,comentario=comentario,proposta=proposta,evidencia=evidencia,identity=identity,anterior=current['id'] if current else None)
                        st.session_state.result=atualizado;st.session_state.revisao_salva=True;st.rerun()
                    except (ValueError,StorageError) as e:st.error(str(e))
                if st.session_state.pop('revisao_salva',False):st.success('Revisão registrada com revisor e data. O valor de origem foi preservado.')
            if res.get('revisoes'):
                st.dataframe(list(linhas_revisoes(res)),hide_index=True,width='stretch')
                st.caption('Atual do revisor indica a avaliação mais recente daquela pessoa; avaliações de colegas são preservadas. Origem vigente indica se o campo ainda corresponde ao mesmo snapshot.')
        with st.expander('Complementar informações com JSON de fornecedor'):
            st.caption('Importe somente respostas obtidas com acesso autorizado. O arquivo é preservado no histórico privado; sua autenticidade não é comprovada por este importador. Empresa, CNPJ, advogado, polo, valor e evidências são candidatos para revisão.')
            if identity['role']=='admin':
                with st.form('complementar_'+res['id']):
                    fornecedor=st.selectbox('Formato da resposta',list(FONTES))
                    arquivo=st.file_uploader('JSON de um processo desta consulta (até 5 MiB)',type=['json'])
                    enviar=st.form_submit_button('Importar JSON e registrar fonte')
                if enviar:
                    try:
                        if arquivo is None:raise ValueError('Selecione um arquivo JSON.')
                        complemento=importar(arquivo.getvalue(),fornecedor,{r['cnj'] for r in res['registros']},identity['email'])
                        atualizado,incluido=store.complementar(res['id'],complemento)
                        if not incluido:
                            st.info('Este arquivo já foi importado para esta consulta.')
                        else:
                            st.session_state.result=atualizado;st.rerun()
                    except (ValueError,StorageError) as e:st.error(str(e))
            else:st.info('A importação de fontes é restrita aos administradores.')
            if res.get('complementos'):
                st.dataframe(list(linhas(res['complementos'])),hide_index=True,width='stretch')
                st.warning('Observações não foram aprovadas juridicamente. Empresas podem incluir entes públicos; valores e resultados de diferentes graus podem divergir. Consulte a fonte antes de escolher o contribuinte ou concluir sobre trânsito e resultado favorável.')
        transito=st.checkbox('Somente indício textual de trânsito — exige revisão')
        qualidade=st.multiselect('Qualidade técnica',['Validado tecnicamente','Com ressalvas','Não exportável'],default=['Validado tecnicamente','Com ressalvas'])
        records=[r for r in res['registros'] if r['qualidade'] in qualidade and (not transito or r['indicio_transito'])]
        campos_disponiveis=[x['campo'] for x in inventario(res['registros'])]
        st.caption('Sugestão inicial de tabela enxuta; personalize as colunas. O JSON completo e as abas de dados originais são preservados.')
        campos=st.multiselect('Campos da tabela principal',campos_disponiveis,default=[f for f in CAMPOS_PRINCIPAIS if f in campos_disponiveis],key='campos_'+res['id'])
        st.dataframe(tabela_principal(records,campos),hide_index=True,width='stretch')
        with st.expander('Todos os campos disponíveis nesta amostra', expanded=False):
            st.caption('Inventário do JSON original, incluindo campos aninhados. Presença não comprova qualidade jurídica. O Excel inclui CAMPOS_DISPONIVEIS e DADOS_ORIGINAIS sem descartar campos novos.')
            st.dataframe(inventario(records),hide_index=True,width='stretch')
        cnjs=list(dict.fromkeys(r['cnj'] for r in records if r['qualidade']!='Não exportável'))
        selection_key='selecao_'+res['id']
        if selection_key in st.session_state:
            st.session_state[selection_key]=[n for n in st.session_state[selection_key] if n in cnjs]
        selection=st.multiselect('Selecionar CNJs para exportação',cnjs,default=cnjs,key=selection_key)
        if selection:
            try:
                data=exportar(res,selection,campos=campos)
                st.download_button('Baixar XLSX verificado',data,file_name=f"{res.get('tribunal','TRF4')}_{res['id'][:8]}.xlsx",mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            except ValueError as e:st.error(str(e))
        st.download_button('Baixar evidências JSON',json.dumps(res,ensure_ascii=False,indent=2).encode(),file_name=f"evidencias_{res['id'][:8]}.json",mime='application/json')
        with st.expander('Filtros e rastreabilidade'):st.json({k:res.get(k) for k in ['id','criada','finalizada','query','status','total_api','erro']})
        if records:
            detalhe=st.selectbox('Processo para inspecionar',list(range(len(records))),format_func=lambda i:f"{records[i]['cnj']} · grau {records[i]['grau']}")
            with st.expander('Registro de origem e movimentações'):st.json(records[detalhe]['original'])
