"""MVP local para um operador. Não expor na Internet sem autenticação."""
import csv,json,os
from pathlib import Path
import streamlit as st
from rota.core import ASSUNTOS,ConsultaError,DataJud,Store,coletar
from rota.export import exportar
from rota.fields import inventario, periodo_cinco_anos

ROOT=Path(__file__).parent
st.set_page_config(page_title='Rota do Milho',page_icon='🌽',layout='wide')
st.title('Rota do Milho')
st.caption('Pesquisa tributária no TRF4 · metadados públicos do CNJ · revisão jurídica necessária')
store=Store(Path(os.getenv('ROTA_DATA_DIR',str(ROOT/'data/runtime')))/'consultas.sqlite3')
if 'api_key' not in st.session_state:st.session_state.api_key=os.getenv('DATAJUD_API_KEY','')
config,pesquisa,resultados,historico=st.tabs(['Configurações','Pesquisa','Resultados','Histórico'])
with config:
    st.subheader('Conexão DataJud')
    st.info('Uso local por um operador. A chave digitada fica somente nesta sessão e será perdida ao encerrá-la. Para inicialização automática, configure DATAJUD_API_KEY no servidor.')
    with st.form('config'):
        key=st.text_input('Chave API DataJud',type='password',value=st.session_state.api_key)
        salvar=st.form_submit_button('Usar chave nesta sessão')
        if salvar:st.session_state.api_key=key.strip();st.success('Configuração aplicada à sessão.')
    if st.button('Testar conexão'):
        api=None
        try:
            api=DataJud(st.session_state.api_key)
            with st.spinner('Consultando CNJ…'):test=api.teste()
            st.session_state.teste=test
            st.success(f"HTTP 200 · {test['registros']} registro(s) · {test['data']}")
            st.write('Campos disponíveis:',test['campos'])
        except ConsultaError as e:st.error(str(e))
        finally:
            if api:api.close()
with pesquisa:
    st.subheader('Consulta ao TRF4')
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
            st.session_state.result=res
            if res.get('erro'):st.warning(res['erro'])
            st.success(f"{res['status']} · {res['cnjs_unicos']} CNJs únicos. Abra Resultados.")
        except ConsultaError as e:st.error(str(e))
        finally:
            if api:api.close()
    with st.expander('103 termos originais — catálogo pendente de mapeamento'):
        with (ROOT/'data/catalogos/termos_originais.csv').open(encoding='utf-8-sig') as f:st.dataframe(list(csv.DictReader(f)),hide_index=True)
with historico:
    history=store.listar()
    st.caption('Histórico armazenado localmente no banco. Cada execução conserva sua resposta e seus registros de origem.')
    if history:
        id=st.selectbox('Consulta anterior',[r[0] for r in history],format_func=lambda x:next(f'{r[1]} · {r[2]} · {r[0][:8]}' for r in history if r[0]==x))
        if st.button('Abrir consulta'):st.session_state.result=store.obter(id);st.rerun()
    else:st.info('Nenhuma consulta registrada.')
with resultados:
    res=st.session_state.get('result')
    if not res:st.info('Execute uma pesquisa ou abra uma consulta do histórico.')
    else:
        st.write(f"**{res['status']}** · {res['cnjs_unicos']} CNJs · {res['recebidos']} registros recebidos")
        if res.get('erro'):st.warning(res['erro'])
        st.caption('Filtros abaixo atuam somente sobre a amostra coletada. Registros do mesmo processo em graus diferentes são preservados.')
        transito=st.checkbox('Somente indício textual de trânsito — exige revisão')
        qualidade=st.multiselect('Qualidade técnica',['Validado tecnicamente','Com ressalvas','Não exportável'],default=['Validado tecnicamente','Com ressalvas'])
        records=[r for r in res['registros'] if r['qualidade'] in qualidade and (not transito or r['indicio_transito'])]
        st.dataframe([{k:r[k] for k in ['cnj','grau','classe','assuntos','ajuizamento','qualidade','ressalvas','indicio_transito']} for r in records],hide_index=True,width='stretch')
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
                data=exportar(res,selection)
                st.download_button('Baixar XLSX verificado',data,file_name=f"TRF4_{res['id'][:8]}.xlsx",mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            except ValueError as e:st.error(str(e))
        st.download_button('Baixar evidências JSON',json.dumps(res,ensure_ascii=False,indent=2).encode(),file_name=f"evidencias_{res['id'][:8]}.json",mime='application/json')
        with st.expander('Filtros e rastreabilidade'):st.json({k:res.get(k) for k in ['id','criada','finalizada','query','status','total_api','erro']})
        if records:
            detalhe=st.selectbox('Processo para inspecionar',list(range(len(records))),format_func=lambda i:f"{records[i]['cnj']} · grau {records[i]['grau']}")
            with st.expander('Registro de origem e movimentações'):st.json(records[detalhe]['original'])
