
# importanto módulos e funções criadas para limpeza e pré-tratamento dos dados
from data_wrangling_modules import *
# carregando demais biliotecas
import pandas as pd
import plotly.express as px
import streamlit as st



# carregando a base de dados
# dados obtidos no site: https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv
df_raw = pd.read_csv('FTC-ZeroFomeDelivery/dataset/zomato.csv') 
#df_raw = pd.read_csv('dataset\\zomato.csv')
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
    
color_mode = st.sidebar.selectbox('Indicar país onde o restaurante fica?', ('não', 'sim'))
if color_mode == 'não':
    color_mode = False
else: 
    color_mode = 'Country_Name'

#filtro de avaliações realizadas
filtro_votes = st.sidebar.selectbox('Incluir restaurantes sem avaliação?', ('não', 'sim'))
if filtro_votes == 'não':
    filtro_votes = df['Votes'] != 0
    df = df.loc[filtro_votes,:]

#filtro de valor de prato
filtro_AVG_cost_4_2 = st.sidebar.selectbox('Incluir restaurantes sem registro de custo de prato?', ('não', 'sim'))
if filtro_AVG_cost_4_2 == 'não':
    filtro_AVG_cost_4_2 = df['Aggregate rating'] != 0
    df = df.loc[filtro_AVG_cost_4_2,:]

    
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

tab1, tab2, tab3 = st.tabs(['Visão Cidades', '-', '-'])

# separa os códigos para cada aba
# todo código que estiber em 'with tab1 vai aparecer naquela aba

with tab1: # 'Visão Geral'
    with st.container():
        # 1. Qual o nome da cidade que possui mais restaurantes registrados?
        cols = ['Restaurant ID', 'City', 'Country_Name']
        group_by_col = ['City', 'Country_Name']
        sort_by_col = 'Restaurant ID'
        sort_by_col_order = [False] 
        x_axis = 'City'
        y_axis = 'Restaurant ID'
        x_label = 'Cidades atendidas'
        y_label = 'Quantidade de Restaurantes'
        if top_mode != 'all':
            graph_label = 'TOP ' + str(top_mode) + ' Cidades com mais Restaurantes Cadastrados'
        else:
            graph_label = 'Restaurantes mais votados'        
        max_width = 1280
        max_height = 700
        operacao = 'nunique'
        #deixa o filtro vazio, assim irá buscar todos os dados
        filtro = pd.DataFrame({'A' : []})
        grafico_percentual = False

        fig, df_aux = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                             x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, color_mode, top_mode)
        st.plotly_chart(fig, use_conteiner_width = False) 

    with st.container():
        #2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?
        cols = ['Aggregate rating', 'City', 'Country_Name']
        group_by_col = ['City', 'Country_Name']
        sort_by_col = ['Aggregate rating']
        sort_by_col_order = [False] 
        x_axis = 'City'
        y_axis = 'Aggregate rating'
        x_label = 'Cidade'
        y_label = 'Quantidade de Restaurantes'
        if top_mode != 'all':
            graph_label = 'TOP ' + str(top_mode) + ' Restaurantes melhor avaliados (nota > 4)'
        else:
            graph_label = 'Restaurantes melhor avaliados (nota > 4)'        
        max_width = 1280
        max_height = 600                        
        operacao = 'mean'
        filtro = df['Aggregate rating'] > 4


        grafico_percentual = False

        fig, df_aux = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                             x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, color_mode, top_mode)
        st.plotly_chart(fig, use_conteiner_width = False) 
        
    with st.container():
        #3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?
        cols = ['Aggregate rating', 'City', 'Country_Name']
        group_by_col = ['City', 'Country_Name']
        sort_by_col = 'Aggregate rating'
        sort_by_col_order = [True] 
        x_axis = 'City'
        y_axis = 'Aggregate rating'
        x_label = 'Cidade'
        y_label = 'Quantidade de Restaurantes'
        if top_mode != 'all':
            graph_label = 'TOP ' + str(top_mode) + ' Restaurantes pior avaliados (nota < 2.5)'
        else:
            graph_label = 'Restaurantes pior avaliados (nota < 2.5)'
        max_width = 1280
        max_height = 600                        
        operacao = 'mean'
        filtro = df['Aggregate rating'] <2.5


        grafico_percentual = False

        fig, df_aux = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                             x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, color_mode, top_mode)
        st.plotly_chart(fig, use_conteiner_width = False) 
        
    with st.container():
        #4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
        cols = ['AVG_cost_4_2', 'City', 'Country_Name']
        group_by_col = ['City', 'Country_Name'] 
        sort_by_col = 'AVG_cost_4_2'
        sort_by_col_order = [False] 
        x_axis = 'City'
        y_axis = 'AVG_cost_4_2'
        x_label = 'Cidade'
        y_label = 'Valor do prato para 2'
        if top_mode != 'all':
            graph_label = 'TOP ' + str(top_mode) + ' Cidades com pratos mais caros'
        else:
            graph_label = 'Cidades com pratos mais caros'
        max_width = 1280
        max_height = 600                        
        operacao = 'mean'
        #deixa o filtro vazio, assim irá buscar todos os dados
        filtro = pd.DataFrame({'A' : []})


        grafico_percentual = False

        fig, df_aux = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                             x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, color_mode, top_mode)
        st.plotly_chart(fig, use_conteiner_width = False) 
    
    with st.container():
        #5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?
        cols = ['Cuisines', 'City', 'Country_Name']
        group_by_col = ['City', 'Country_Name'] 
        sort_by_col = 'Cuisines'
        sort_by_col_order = [False] 
        x_axis = 'City'
        y_axis = 'Cuisines'
        x_label = 'Cidade'
        y_label = 'Variedade de culinária'
        if top_mode != 'all':
            graph_label = 'TOP ' + str(top_mode) + ' Cidades com maior diversidade culinária'
        else:
            graph_label = 'Cidades com maior diversidade de culinária'
        max_width = 1280
        max_height = 600                        
        operacao = 'nunique'
        #deixa o filtro vazio, assim irá buscar todos os dados
        filtro = pd.DataFrame({'A' : []})


        grafico_percentual = False

        fig, df_aux = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                             x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, color_mode, top_mode)
        st.plotly_chart(fig, use_conteiner_width = False) 
        
        
    with st.container():
        #6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?
        cols = ['Has Table booking', 'City', 'Country_Name']
        group_by_col = ['City', 'Country_Name']
        sort_by_col = 'Has Table booking'
        sort_by_col_order = [False] 
        x_axis = 'City'
        y_axis = 'Has Table booking'
        x_label = 'Cidade'
        y_label = 'Quantidade de Restaurantes'
        if top_mode != 'all':
            graph_label = 'TOP ' + str(top_mode) + ' Cidades com mais Restaurantes que fazem Reserva'
        else:
            graph_label = 'Cidades com mais restaurantes que fazem reserva'
        max_width = 1280
        max_height = 600                        
        operacao = 'count'
        filtro = df.loc[:, sort_by_col] == True

        grafico_percentual = False

        fig, df_aux = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                             x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, color_mode, top_mode)
        st.plotly_chart(fig, use_conteiner_width = False)         
                    
    with st.container():
        #7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?
        cols = ['Is delivering now', 'City', 'Country_Name']
        group_by_col = ['City', 'Country_Name']
        sort_by_col = 'Is delivering now'
        sort_by_col_order = [False] 
        x_axis = 'City'
        y_axis = 'Is delivering now'
        x_label = 'Cidade'
        y_label = 'Quantidade de Restaurantes'
        if top_mode != 'all':
            graph_label = 'TOP ' + str(top_mode) + ' Cidades com mais restaurantes que fazem entrega'
        else:
            graph_label = 'Cidades que fazem entrega'
        max_width = 1280
        max_height = 600                        
        operacao = 'count'
        filtro = df.loc[:, sort_by_col] == True

        grafico_percentual = False

        fig, df_aux = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                             x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, color_mode, top_mode)
        st.plotly_chart(fig, use_conteiner_width = False)         
                

    with st.container():
        #8. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?
        cols = ['Has Online delivery', 'City', 'Country_Name']
        group_by_col = ['City', 'Country_Name']
        sort_by_col = 'Has Online delivery'
        sort_by_col_order = [False] 
        x_axis = 'City'
        y_axis = 'Has Online delivery'
        x_label = 'Cidade'
        y_label = 'Pedidos Online'
        if top_mode != 'all':
            graph_label = 'TOP ' + str(top_mode) + ' Cidades com restaurantes que aceitam pedidos online'
        else:
            graph_label = 'Cidades com restaurantes que aceitam pedidos online'
        max_width = 1280
        max_height = 600                        
        operacao = 'count'
        filtro = df.loc[:, sort_by_col] == True

        grafico_percentual = False

        fig, df_aux = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                             x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, color_mode, top_mode)
        st.plotly_chart(fig, use_conteiner_width = False)         
                
