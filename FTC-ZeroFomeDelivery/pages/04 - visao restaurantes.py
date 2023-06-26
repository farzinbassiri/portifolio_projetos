
# importanto módulos e funções criadas para limpeza e pré-tratamento dos dados
from data_wrangling_modules import *
# carregando demais biliotecas
import pandas as pd
import plotly.express as px
import streamlit as st

# carregando a base de dados
# dados obtidos no site: https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv
#Correção do caminho da base de dados para ser compativel com o streamlit:
df_raw = pd.read_csv('FTC-ZeroFomeDelivery/dataset/zomato.csv') 
df = data_wrangling(df_raw)
st.set_page_config(page_title= 'Visão Cidades', layout='wide')
#--------------------------------------------------------------
#                    Barra Lateral    
#--------------------------------------------------------------

#filtro de TOP x restaurantes:
top_mode = st.sidebar.selectbox('Colocar todos os restaurantes?', ('não', 'sim'))
if top_mode == 'não':
    top_mode = st.sidebar.slider(label = 'Defina quantidade de restaurantes', min_value= 5, max_value= 100, value=15)
else: 
    top_mode = 'all'
    
color_mode = st.sidebar.selectbox('Indicar país onde o restaurente fica?', ('não', 'sim'))
if color_mode == 'não':
    color_mode = False
else: 
    color_mode = 'Country_Name'

# seleção dos paises de interesse
paises = df.loc[:,['Country_Name']].groupby('Country_Name').count().reset_index()
country_options = st.sidebar.multiselect(
                        'Selecione os paises de interesse:',
                        paises['Country_Name'],
                        default = paises['Country_Name'])


    
#filtro dos paises selecionados
filtro_pais = df['Country_Name'].isin(country_options)
df = df.loc[filtro_pais,:]



#--------------------------------------------------------------
#           Layout do dashboard - usando streamlit    
#--------------------------------------------------------------

#Abas com as diferentes métricas 

tab1, tab2, tab3 = st.tabs(['Indicadores Absolutos', '-', '-'])

# separa os códigos para cada aba
# todo código que estiber em 'with tab1 vai aparecer naquela aba

with tab1: # 'Visão Geral'
    with st.container():
        # 1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
        cols = ['Restaurant Name', 'Votes', 'Country_Name']
        group_by_col = ['Restaurant Name', 'Country_Name']
        sort_by_col = 'Votes'
        sort_by_col_order = [False] 
        x_axis = 'Restaurant Name'
        y_axis = 'Votes'
        x_label = 'Restaurantes'
        y_label = 'Quantidade de votos'
        if top_mode != 'all':
            graph_label = 'TOP ' + str(top_mode) + ' Restaurantes mais avaliados'
        else:
            graph_label = 'Restaurantes mais avaliados'
        max_width = 1280
        max_height = 700
        operacao = 'sum'
        #deixa o filtro vazio, assim irá buscar todos os dados
        filtro = pd.DataFrame({'A' : []})
        grafico_percentual = False
        
        fig = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order, 
                              x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, color_mode, top_mode)
        st.plotly_chart(fig, use_conteiner_width = False) 

    with st.container():
        #2. Qual o nome do restaurante com a maior nota média?
        cols = ['Restaurant Name', 'Restaurant ID', 'Aggregate rating', 'Country_Name']
        group_by_col = ['Restaurant Name', 'Country_Name']
        sort_by_col = ['Aggregate rating', 'Restaurant ID']
        sort_by_col_order = [False, True] 
        x_axis = 'Restaurant Name'
        y_axis = 'Aggregate rating'
        x_label = 'Restaurantes'
        y_label = 'Nota média'
        if top_mode != 'all':
            graph_label = 'TOP ' + str(top_mode) + ' Restaurantes com maior nota média'
        else:
            graph_label = 'Restaurantes com maior nota média'
        max_width = 1280
        max_height = 700
        operacao = 'mean'
        #deixa o filtro vazio, assim irá buscar todos os dados
        filtro = pd.DataFrame({'A' : []})
        grafico_percentual = False
        fig = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order, 
                              x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, color_mode, top_mode)
        st.plotly_chart(fig, use_conteiner_width = False) 

    with st.container():
        #3. Qual o nome do restaurante que possui o maior valor de uma prato para duas pessoas?
        cols = ['Restaurant Name', 'Restaurant ID', 'AVG_cost_4_2', 'Country_Name']
        group_by_col = ['Restaurant Name', 'Country_Name']
        sort_by_col = ['AVG_cost_4_2', 'Restaurant ID']
        sort_by_col_order = [False, True] 
        x_axis = 'Restaurant Name'
        y_axis = 'AVG_cost_4_2'
        x_label = 'Restaurantes'
        y_label = 'Custo [USD]'
        if top_mode != 'all':
            graph_label = 'TOP ' + str(top_mode) + ' Restaurantes mais caros'
        else:
            graph_label = 'Restaurantes mais caros'
        max_width = 1280
        max_height = 700
        operacao = 'mean'
        #deixa o filtro vazio, assim irá buscar todos os dados
        filtro = pd.DataFrame({'A' : []})
        grafico_percentual = False
        fig = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order, 
                              x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, color_mode, top_mode)
        st.plotly_chart(fig, use_conteiner_width = False) 
        

    with st.container():
        st.markdown('### Melhor e pior restaurante de culinária brasileira:')
        col1, col2, col3 = st.columns(3, gap="large")
        
        with col1:        
            #4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação?
            cols = ['Restaurant Name', 'Restaurant ID', 'Aggregate rating', 'AVG_cost_4_2', 'City', 'Country_Name']
            group_by_col = ['Restaurant Name', 'Aggregate rating', 'AVG_cost_4_2', 'City', 'Country_Name']
            sort_by_col = ['Aggregate rating', 'Restaurant ID']
            sort_by_col_order = [True, True] 
            col_calc = 'Aggregate rating'
            operacao = 'nunique'
            filtro = (df['Cuisines'] == 'Brazilian') 
            piores_restaurantes = classificacao(filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, col_calc)
            texto = str(piores_restaurantes.iloc[0,1]) + '\n / 5.0'
            st.metric(label= '##### Pior restaurante:  ', value= texto, delta=None, delta_color="normal", help=None, label_visibility="visible")
            with st.expander("Mais informações:"):
                st.write('-- Restaurante: ' + str(piores_restaurantes.iloc[0,0]) + 
                         '\n\n -- Localização: ' + str(piores_restaurantes.iloc[0,3] + '/' + str(piores_restaurantes.iloc[0,4])) +
                         '\n\n -- Preço Médio do Prato: ' + str(piores_restaurantes.iloc[0,2]))

        
        with col2:
            #5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação?
            cols = ['Restaurant Name', 'Restaurant ID', 'Aggregate rating', 'AVG_cost_4_2', 'City', 'Country_Name']
            group_by_col = ['Restaurant Name', 'Aggregate rating', 'AVG_cost_4_2', 'City', 'Country_Name']
            sort_by_col = ['Aggregate rating', 'Restaurant ID']
            sort_by_col_order = [False, True] 
            col_calc = 'Aggregate rating'
            operacao = 'nunique'
            filtro = (df['Cuisines'] == 'Brazilian') 

            melhores_restaurantes = classificacao(filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, col_calc)
            texto = str(melhores_restaurantes.iloc[0,1]) + '\n / 5.0'
            st.metric(label= '##### Melhor restaurante:  ', value= texto, delta=None, delta_color="normal", help=None, label_visibility="visible")
            with st.expander("Mais informações:"):
                st.write('-- Restaurante: ' + str(melhores_restaurantes.iloc[0,0]) + 
                         '\n\n -- Localização: ' + str(melhores_restaurantes.iloc[0,3] + '/' + str(melhores_restaurantes.iloc[0,4])) +
                         '\n\n -- Preço Médio do Prato: ' + str(melhores_restaurantes.iloc[0,2]))

    with st.container():
        st.markdown('### Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas?')
        col1, col2, col3 = st.columns(3, gap="large")
        with col1:
            st.markdown('')
            with st.expander("Avaliação:", expanded=True):
                st.write('Os restaurantes que fazem entregas tem uma tendência a possuir maior quantidade de avaliações dos clientes')        
        
        with col2:
            #6. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas?
            cols = ['Has Online delivery', 'Votes']
            col_calc = 'Votes'
            group_by_col = ['Has Online delivery']
            sort_by_col = ['Votes']
            sort_by_col_order = [True] 
            x_axis = 'Votes'
            y_axis = 'Has Online delivery'
            x_label = 'Faz entrega'
            y_label = 'Não faz entrega'
            graph_label = 'Restaurantes que fazem entrega x Quantidade média de avaliações'
            max_width = 500
            max_height = 400
            grafico_percentual = False
            color_mode = False  
            operacao = 'mean'
            top_mode = 'all'
            col_calc = 'Votes'
            pie_hole = 0.5
            #deixa o filtro vazio, assim irá buscar todos os dados
            del filtro
            filtro = (df['Votes'] != '')

            fig = pie_chart(filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, col_calc, 
                            x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, top_mode, pie_hole)
            st.plotly_chart(fig, use_conteiner_width = False)
        
        


    with st.container():
        #7. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?
        st.markdown('### Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?')
        col1, col2, col3 = st.columns(3, gap="large")
        with col1:
            st.markdown('')
            with st.expander("Avaliação:", expanded=True):
                st.write('Os restaurantes que fazem reserva de mesas tem uma tendência a possuir pratos mais caros.')        
        
        with col2:
            cols = ['Has Table booking', 'AVG_cost_4_2']
            col_calc = 'AVG_cost_4_2'
            group_by_col = ['Has Table booking']
            sort_by_col = ['AVG_cost_4_2']
            sort_by_col_order = [True] 
            x_axis = 'AVG_cost_4_2'
            y_axis = 'Has Table booking'
            x_label = 'Faz reserva'
            y_label = 'Não faz reserva'
            graph_label = 'Restaurantes que fazem reserva x Custo do prato'
            max_width = 500
            max_height = 400
            grafico_percentual = False
            color_mode = False  
            operacao = 'mean'
            top_mode = 'all'
            col_calc = 'AVG_cost_4_2'
            pie_hole = 0.5
            #deixa o filtro vazio, assim irá buscar todos os dados
            filtro = (df['AVG_cost_4_2'] != '')

            fig = pie_chart(filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, col_calc, x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, top_mode, pie_hole)
            st.plotly_chart(fig, use_conteiner_width = False)
        

    with st.container():
        #8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)?
        st.markdown('### Os restaurantes de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas?')
        col1, col2, col3 = st.columns(3, gap="large")
        with col1:
            st.markdown('')
            with st.expander("Avaliação:", expanded=True):
                st.write('Os restaurantes com culinária japonesa são em geral mais caros que os de churrasco quando olhamos o mercado Americano.')        
        
        with col2:
            cols = ['Cuisines', 'AVG_cost_4_2', 'Country_Name']
            col_calc = 'AVG_cost_4_2'
            group_by_col = ['Cuisines']
            sort_by_col = ['AVG_cost_4_2']
            sort_by_col_order = [True] 
            x_axis = 'AVG_cost_4_2'
            y_axis = 'Cuisines'
            x_label = ''
            y_label = ''
            graph_label = 'Custo médio dos pratos em restaurantes nos USA'
            max_width = 500
            max_height = 400
            grafico_percentual = False
            color_mode = False  
            operacao = 'mean'
            top_mode = 'all'
            col_calc = 'AVG_cost_4_2'
            pie_hole = 0.5

            filtro = (df['Country_Name'] == 'United States of America') & ((df['Cuisines'] == 'BBQ') | (df['Cuisines'] == 'Japanese'))

            fig = pie_chart(filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, col_calc, 
                            x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, top_mode, pie_hole)
            st.plotly_chart(fig, use_conteiner_width = False)
        
