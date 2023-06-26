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
st.set_page_config(page_title= 'Visão Países', layout='wide')
#--------------------------------------------------------------
#                    Barra Lateral    
#--------------------------------------------------------------
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

tab1, tab2, tab3 = st.tabs(['Indicadores Absolutos', 'Indicadores Relativos [%]', '-'])

# separa os códigos para cada aba
# todo código que estiber em 'with tab1 vai aparecer naquela aba

with tab1: # 'Visão Geral'
    with st.container():
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            # 1. Qual o nome do país que possui mais cidades registradas?  
            cols = ['City', 'Country_Name']
            group_by_col = 'Country_Name'
            sort_by_col = 'City'
            sort_by_col_order = [False] 
            x_axis = 'Country_Name'
            y_axis = 'City'
            x_label = 'País'
            y_label = 'Cidades assistidas'
            graph_label = 'Total de Países com Restaurantes Cadastrados'
            max_width = 700
            max_height = 500
            operacao = 'nunique'
            #deixa o filtro vazio, assim irá buscar todos os dados
            filtro = pd.DataFrame({'A' : []})
            grafico_percentual = False
            
            fig = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
                    
            st.plotly_chart(fig, use_conteiner_width = False) 
        
        with col2:
            #2. Qual o nome do país que possui mais restaurantes registrados?
            cols = ['Restaurant ID', 'Country_Name']
            group_by_col = 'Country_Name'
            sort_by_col = 'Restaurant ID'
            sort_by_col_order = [False] 
            x_axis = 'Country_Name'
            y_axis = 'Restaurant ID'
            x_label = 'País'
            y_label = 'Quantidade de Restaurantes'
            graph_label = 'Total de Restaurantes Cadastrados'
            max_width = 700
            max_height = 500                        
            operacao = 'count'
            #deixa o filtro vazio, assim irá buscar todos os dados
            filtro = pd.DataFrame({'A' : []})
            
            grafico_percentual = False
            
            fig = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            st.plotly_chart(fig, use_conteiner_width = False) 
    
    with st.container():
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            #3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados (estilo gourmet)?
            
            cols = ['Restaurant ID', 'Country_Name']
            group_by_col = 'Country_Name'
            sort_by_col = 'Restaurant ID'
            sort_by_col_order = [False] 
            x_axis = 'Country_Name'
            y_axis = 'Restaurant ID'
            x_label = 'País'
            y_label = 'Quantidade de Restaurantes'
            graph_label = 'Restaurantes Estilo "Gourmet"'
            max_width = 700
            max_height = 500                        
            operacao = 'count'            

            restaurantes_selecionados = df['Price range'] == 'gourmet'
            
            grafico_percentual = False
            
            fig = grafico_barras(grafico_percentual, restaurantes_selecionados, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            st.plotly_chart(fig, use_conteiner_width = False) 
    
        with col2:
            # 4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?
           
            cols = ['Cuisines', 'Country_Name']
            group_by_col = 'Country_Name'
            sort_by_col = 'Cuisines'
            sort_by_col_order = [False] 
            x_axis = 'Country_Name'
            y_axis = 'Cuisines'
            x_label = 'País'
            y_label = 'Quantidade'
            graph_label = 'Tipos de culinária disponíveis'
            max_width = 700
            max_height = 500                        
            operacao = 'nunique'
            #deixa o filtro vazio, assim irá buscar todos os dados
            filtro = pd.DataFrame({'A' : []})
            
            grafico_percentual = False
            
            fig = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order, 
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            st.plotly_chart(fig, use_conteiner_width = False) 
            
    with st.container():
        col1, col2 = st.columns(2, gap="large")
        
        with col1:        
            # 5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
            cols = ['Votes', 'Country_Name']
            group_by_col = 'Country_Name'
            sort_by_col = 'Votes'
            sort_by_col_order = [False] 
            x_axis = 'Country_Name'
            y_axis = 'Votes'
            x_label = 'País'
            y_label = 'Quantidade'
            graph_label = 'Total de Avaliações Realizadas'
            max_width = 700
            max_height = 500                        
            operacao = 'sum'

            #deixa o filtro vazio, assim irá buscar todos os dados
            filtro = pd.DataFrame({'A' : []})
            
            grafico_percentual = False
            
            fig = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            st.plotly_chart(fig, use_conteiner_width = False)         
            
        with col2:
            # 6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?
            cols = ['Has Online delivery', 'Country_Name']
            group_by_col = 'Country_Name'
            sort_by_col = 'Has Online delivery'
            sort_by_col_order = False 
            x_axis = 'Country_Name'
            y_axis = 'Has Online delivery'
            x_label = 'País'
            y_label = 'Quantidade'
            graph_label = 'Restaurantes que fazem entrega'
            max_width = 700
            max_height = 500                        
            operacao = 'count'

            filtro = df.loc[:,'Has Online delivery'] == True
            grafico_percentual = False
            
            fig = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order, 
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            
            st.plotly_chart(fig, use_conteiner_width = False)    
    
    with st.container():
        col1, col2 = st.columns(2, gap="large")
        
        with col1:  
            #7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?
            cols = ['Has Table booking', 'Country_Name']
            group_by_col = 'Country_Name'
            sort_by_col = 'Has Table booking'
            sort_by_col_order = [False] 
            x_axis = 'Country_Name'
            y_axis = 'Has Table booking'
            x_label = 'País'
            y_label = 'Quantidade'
            graph_label = 'Restaurantes que aceitam reserva'
            max_width = 700
            max_height = 500                        
            operacao = 'count'

            filtro = df.loc[:, sort_by_col] == True
            grafico_percentual = False
            
            fig = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            
            st.plotly_chart(fig, use_conteiner_width = False)                

        with col2:  
            #8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?
            cols = ['Votes', 'Country_Name']
            group_by_col = 'Country_Name'
            sort_by_col = 'Votes'
            sort_by_col_order = [False] 
            x_axis = 'Country_Name'
            y_axis = 'Votes'
            x_label = 'País'
            y_label = 'Votos por restaurante cadastrado'
            graph_label = 'Paises com mais cultura de votos'
            max_width = 700
            max_height = 500                        
            operacao = 'sum'

            #deixa o filtro vazio, assim irá buscar todos os dados
            filtro = pd.DataFrame({'A' : []})
            grafico_percentual = True
            
            fig = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            
            st.plotly_chart(fig, use_conteiner_width = False)              



    with st.container():
        col1, col2 = st.columns(2, gap="large")
        
        with col1:  
            #9. Qual o nome do país que possui, na média, a maior nota média registrada?
            cols = ['Rating_note', 'Country_Name']
            group_by_col = 'Country_Name'
            sort_by_col = 'Rating_note'
            sort_by_col_order = [False] 
            x_axis = 'Country_Name'
            y_axis = 'Rating_note'
            x_label = 'País'
            y_label = 'Notas [0 a 5]'
            graph_label = 'Paises com melhores avaliações'
            max_width = 700
            max_height = 500                        
            operacao = 'mean'

            filtro = pd.DataFrame({'A' : []})
            grafico_percentual = False
            
            fig = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            
            st.plotly_chart(fig, use_conteiner_width = False)                


   
        with col2:  
            #11. Qual a média de preço de um prato para dois por país?
            cols = ['AVG_cost_4_2', 'Country_Name']
            group_by_col = 'Country_Name'  
            sort_by_col = 'AVG_cost_4_2'
            sort_by_col_order = [False] 
            x_axis = 'Country_Name'
            y_axis = 'AVG_cost_4_2'
            x_label = 'País'
            y_label = 'Valor em USD'
            graph_label = 'Custo médio para 2 pessoas'
            max_width = 700
            max_height = 500                        
            operacao = 'mean'

            #deixa o filtro vazio, assim irá buscar todos os dados
            filtro = pd.DataFrame({'A' : []})
            grafico_percentual = False
            
            fig = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            
            st.plotly_chart(fig, use_conteiner_width = False)  
            
with tab2: # 'Visão Geral %'
    with st.container():
        #2. Qual o nome do país que possui mais restaurantes registrados?
        cols = ['Restaurant ID', 'Country_Name']
        group_by_col = 'Country_Name'
        sort_by_col = 'Restaurant ID'
        sort_by_col_order = [False] 
        x_axis = 'Country_Name'
        y_axis = 'Restaurant ID'
        x_label = 'País'
        y_label = 'Quantidade de Restaurantes'
        graph_label = 'Total de Restaurantes Cadastrados'
        max_width = 700
        max_height = 500                        
        operacao = 'count'
        #deixa o filtro vazio, assim irá buscar todos os dados
        filtro = pd.DataFrame({'A' : []})
        grafico_percentual = False    
        fig = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                             x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
        st.plotly_chart(fig, use_conteiner_width = True) 
    
    with st.container():
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            #3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados (estilo gourmet)?
            
            cols = ['Restaurant ID', 'Country_Name']
            group_by_col = 'Country_Name'
            sort_by_col = 'Restaurant ID'
            sort_by_col_order = [False] 
            x_axis = 'Country_Name'
            y_axis = 'Restaurant ID'
            x_label = 'País'
            y_label = '% Restaurantes'
            graph_label = 'Restaurantes Estilo "Gourmet"'
            max_width = 700
            max_height = 500                        
            operacao = 'count'            
            grafico_percentual = True

            restaurantes_selecionados = df['Price range'] == 'gourmet'
            
            fig = grafico_barras(grafico_percentual, restaurantes_selecionados, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            st.plotly_chart(fig, use_conteiner_width = False) 
    
        with col2:
            # 4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?
           
            cols = ['Cuisines', 'Country_Name']
            group_by_col = 'Country_Name'
            sort_by_col = 'Cuisines'
            sort_by_col_order = [False] 
            x_axis = 'Country_Name'
            y_axis = 'Cuisines'
            x_label = 'País'
            y_label = '% de restaurantes'
            graph_label = 'Tipos de culinária disponíveis'
            max_width = 700
            max_height = 500                        
            operacao = 'nunique'
            grafico_percentual = True
            #indica que não vai haver filtro criando um df vazio
            filtro = pd.DataFrame({'A' : []})
            
            fig = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            st.plotly_chart(fig, use_conteiner_width = False) 
            
    with st.container():
        col1, col2 = st.columns(2, gap="large")
        
        with col1:        
            # 5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
            cols = ['Votes', 'Country_Name']
            group_by_col = 'Country_Name'
            sort_by_col = 'Votes'
            sort_by_col_order = [False] 
            x_axis = 'Country_Name'
            y_axis = 'Votes'
            x_label = 'País'
            y_label = 'Quantidade de votos por restaurante'
            graph_label = 'Cultura de Avaliação dos Restaurantes'
            max_width = 700
            max_height = 500                        
            operacao = 'sum'
            grafico_percentual = True

            #indica que não vai haver filtro criando um df vazio
            filtro = pd.DataFrame({'A' : []})
            
            fig = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            st.plotly_chart(fig, use_conteiner_width = False)         
            
        with col2:
            # 6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?
            cols = ['Has Online delivery', 'Country_Name']
            group_by_col = 'Country_Name'
            sort_by_col = 'Has Online delivery'
            sort_by_col_order = [False] 
            x_axis = 'Country_Name'
            y_axis = 'Has Online delivery'
            x_label = 'País'
            y_label = '% restaurantes'
            graph_label = 'Has Online delivery'
            max_width = 700
            max_height = 500                        
            operacao = 'count'
            grafico_percentual = True

            restaurantes_selecionados = df.loc[:,'Has Online delivery'] == True
            
            fig2 = grafico_barras(grafico_percentual, restaurantes_selecionados, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order,
                                  x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            st.plotly_chart(fig2, use_conteiner_width = False)    

    with st.container():
        col1, col2 = st.columns(2, gap="large")
        
        with col1:  
            #7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?
            cols = ['Has Table booking', 'Country_Name']
            group_by_col = 'Country_Name'
            sort_by_col = 'Has Table booking'
            sort_by_col_order = [False] 
            x_axis = 'Country_Name'
            y_axis = 'Has Table booking'
            x_label = 'País'
            y_label = '% de Restaurantes'
            graph_label = 'Restaurantes que aceitam reserva'
            max_width = 700
            max_height = 500                        
            operacao = 'count'

            restaurantes_selecionados = df.loc[:, sort_by_col] == True
            grafico_percentual = True
            
            fig = grafico_barras(grafico_percentual, restaurantes_selecionados, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            
            st.plotly_chart(fig, use_conteiner_width = False)                

        with col2:  
            #9. Qual o nome do país que possui, na média, a maior nota média registrada?
            cols = ['Rating_note', 'Country_Name']
            group_by_col = 'Country_Name'
            sort_by_col = 'Rating_note'
            sort_by_col_order = [False] 
            x_axis = 'Country_Name'
            y_axis = 'Rating_note'
            x_label = 'País'
            y_label = 'Notas [0 a 5]'
            graph_label = 'Paises com melhores avaliações'
            max_width = 700
            max_height = 500                        
            operacao = 'mean'

            filtro = pd.DataFrame({'A' : []})
            grafico_percentual = True
            
            fig = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            
            st.plotly_chart(fig, use_conteiner_width = False)                

