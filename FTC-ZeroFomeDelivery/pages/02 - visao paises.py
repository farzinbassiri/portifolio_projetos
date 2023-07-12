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
st.set_page_config(page_title= 'Visão Países', layout='wide')
#--------------------------------------------------------------
#                    Barra Lateral    
#--------------------------------------------------------------
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




# definição global de tamanho dos gráficos
max_width = 550
max_height = 400
#--------------------------------------------------------------
#           Layout do dashboard - usando streamlit    
#--------------------------------------------------------------

#Abas com as diferentes métricas 

tab1, tab2, tab3 = st.tabs(['Visão Países', '-', '-'])


# cada um dos grupos de gráficos usa a estrutura abaixo para o processamento dos dados
    # cols --> colunas do dataframe que serão utilizadas
    # group_by_col = coluna que será agrupada para a visualização dos dados
    # sort_by_col = coluna que será a referência de ordenação dos dados
    # sort_by_col_order = variável que indica se a ordenação é ascendente ou descendente
    # x_axis = coluna que será utilizada como eixo X no gráfico
    # y_axis =  coluna que será utilizada como eixo Y no gráfico
    # x_label = Nome do eixo X
    # y_label = Nome do eixo Y
    # graph_label = Nome do gráfico
    # #max_width = tamanho do gráfico, se comentado, usa o tamanho global
    # #max_height = tamanho do gráfico, se comentado, usa o tamanho global
    # operacao = 
        # 'nunique'
        # 'count'
        # 'mean'
        # 'sum'
        # 'none' -->  não faz operação nenhuma, também ignora o group_by_col.

    # filtro = especifica um fitro no df
    # grafico_percentual 
        # False: grafico com numeros absolutos
        # True: gráfico com numeros relativos, tudo é dividido pela quantidade de restaurantes no país.
            



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
            y_label = 'Quantidade de cidades'
            graph_label = 'Quantidade de Cidades Atendidas'
            #max_width = 700
            #max_height = 500
            operacao = 'nunique'
            #deixa o filtro vazio, assim irá buscar todos os dados
            filtro = pd.DataFrame({'A' : []})
            grafico_percentual = False

            fig, df_aux = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            df_aux.columns = [x_label, y_label]
            texto = 'Os 5 paises com mais cidades atendidas são:' 
            st.info(texto)
            st.dataframe(df_aux.head(5))
            #st.plotly_chart(fig, use_conteiner_width = False) 
        
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
            #max_width = 700
            #max_height = 500                        
            operacao = 'count'
            #deixa o filtro vazio, assim irá buscar todos os dados
            filtro = pd.DataFrame({'A' : []})
            
            grafico_percentual = False
            
            fig, df_aux = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            
            df_aux.columns = [x_label, y_label]
            texto = 'Os 5 paises com mais restaurantes cadastrados são:' 
            st.info(texto)
            st.dataframe(df_aux.head(5))
            #st.plotly_chart(fig, use_conteiner_width = False) 
    
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
            graph_label = "5 Paises com mais restaurantes 'Gourmet'"
            #max_width = 700
            #max_height = 500                        
            operacao = 'count'            

            restaurantes_selecionados = df['Price range'] == 'gourmet'
            
            grafico_percentual = False
            
            fig, df_aux = grafico_barras(grafico_percentual, restaurantes_selecionados, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 5)

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
            y_label = 'Tipos diferentes de culinária'
            graph_label = 'Variedade Gastronômica'
            #max_width = 700
            #max_height = 500                        
            operacao = 'nunique'
            #deixa o filtro vazio, assim irá buscar todos os dados
            filtro = pd.DataFrame({'A' : []})
            
            grafico_percentual = False
            
            fig, df_aux = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order, 
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            st.plotly_chart(fig, use_conteiner_width = False) 
            
    with st.container():
        col1, col2 = st.columns(2, gap="large")
        st.metric(label= '##### Cultura de Avaliação:  ', value= '', delta=None, delta_color="normal", help=None, label_visibility="visible")
        with st.expander("Insight:"):
            st.write('Apesar da índia ter maior base de restaurantes cadastrados, pode-se perceber que a Indonésia possui maior tentência à avaliação dos restaurantes. Os dois países com menor tendência a avaliar os restaurantes têm em comum a concentração em avaliação positiva. Isso pode indicar uma indisposição a reclamar da qualidade do serviço prestado ou, talvez, um constrangimento em fazê-lo. Talvez possa ser útil avaliar indicadores culturais que expliquem melhor essa tendência.')

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
            #max_width = 700
            #max_height = 500                        
            operacao = 'sum'

            #deixa o filtro vazio, assim irá buscar todos os dados
            filtro = pd.DataFrame({'A' : []})
            
            grafico_percentual = False
            
            fig, df_aux = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            st.plotly_chart(fig, use_conteiner_width = False)         
#####

        with col2:
            #8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?
            cols = ['Votes', 'Country_Name']
            group_by_col = 'Country_Name'
            sort_by_col = 'Votes'
            sort_by_col_order = [False] 
            x_axis = 'Country_Name'
            y_axis = 'Votes'
            x_label = 'País'
            y_label = 'Quantidade de avaliações por restaurante'
            graph_label = 'Paises maior cultura de avaliação'
            #max_width = 700
            #max_height = 500                        
            operacao = 'sum'

            #deixa o filtro vazio, assim irá buscar todos os dados
            filtro = pd.DataFrame({'A' : []})
            grafico_percentual = True
            
            fig, df_aux = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            
            st.plotly_chart(fig, use_conteiner_width = False)              


    with st.container():
        col1, col2 = st.columns(2, gap="large")
        
        with col1:  
        #Brasil: tipos de avaliações
            cols = ['Votes', 'Country_Name']
            group_by_col = 'Country_Name'
            sort_by_col = 'Votes'
            sort_by_col_order = [True] 
            x_axis = 'Country_Name'
            y_axis = 'Votes'
            x_label = 'País'
            y_label = 'Total de avaliações'
            #max_width = 700
            #max_height = 500                        
            operacao = 'sum'

            #deixa o filtro vazio, assim irá buscar todos os dados
            filtro = pd.DataFrame({'A' : []})
            grafico_percentual = False

            fig, df_votes = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')

            pais=df_votes.iloc[0,0]
            df_aux = df.loc[(df['Country_Name']==pais),:]
            graph_label = pais + ': Avaliações dos restaurantes'
            
            fig = avalia_pais(x_label, y_label, graph_label, max_width, max_height, df_aux)

            st.plotly_chart(fig, use_conteiner_width = False)  
            
        with col2:  
        #Brasil: tipos de avaliações
            cols = ['Votes', 'Country_Name']
            group_by_col = 'Country_Name'
            sort_by_col = 'Votes'
            sort_by_col_order = [True] 
            x_axis = 'Country_Name'
            y_axis = 'Votes'
            x_label = 'País'
            y_label = 'Total de avaliações'
            #max_width = 700
            #max_height = 500                        
            operacao = 'sum'

            #deixa o filtro vazio, assim irá buscar todos os dados
            filtro = pd.DataFrame({'A' : []})
            grafico_percentual = False

            fig, df_votes = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')

            pais=df_votes.iloc[1,0]
            df_aux = df.loc[(df['Country_Name']==pais),:]
            graph_label = pais + ': Avaliações dos restaurantes'
            
            fig = avalia_pais(x_label, y_label, graph_label, max_width, max_height, df_aux)

            st.plotly_chart(fig, use_conteiner_width = False)              
            

    with st.container():
        col1, col2 = st.columns(2, gap="large")
        
        with col1:  
            #9. Qual o nome do país que possui, na média, a maior nota média registrada?
            cols = ['Aggregate rating', 'Country_Name']
            group_by_col = 'Country_Name'
            sort_by_col = 'Aggregate rating'
            sort_by_col_order = [False] 
            x_axis = 'Country_Name'
            y_axis = 'Aggregate rating'
            x_label = 'País'
            y_label = 'Notas [0 a 5]'
            graph_label = 'País com melhor avaliação média'
            #max_width = 700
            #max_height = 500                        
            operacao = 'none'
            
            grafico_percentual = False
            df_mean = df.loc[:, cols].groupby(group_by_col).mean().round(decimals=2).sort_values(sort_by_col, ascending = sort_by_col_order).reset_index()
            df_mean.columns = ['País','Avaliação Média']
            
            #filtro dos paises selecionados
            filtro = ((df.loc[:,'Country_Name'] == df_mean.iloc[0,0]))
 
            #usa apenas os dados do dataframe filtado.. não gera o gráfico
            fig, df_aux = grafico_boxplot(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            
            texto = '### País com melhor nota média:'
            help_text = 'Nota pode ir de 0 a 5, sendo 5 a nota que melhor qualifica o restaurante. \n\ Nota 0 é data ao restaurante não avaliado.'
            st.info(texto)
            texto = str(df_mean.iloc[0,0]) + ': ' +  str(df_mean.iloc[0,1])
            st.metric(label= '', value= texto, delta=None, delta_color="normal", help=help_text, label_visibility="visible")               
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
            #max_width = 700
            #max_height = 500                        
            operacao = 'none'
            
            grafico_percentual = False
            df_mean = df.loc[:, cols].groupby(group_by_col).mean().round(decimals=2).sort_values(sort_by_col, ascending = sort_by_col_order).reset_index()
            df_mean.columns = ['País','Preço médio']
            
            #filtro dos paises selecionados
            filtro = ((df.loc[:,'Country_Name'] == df_mean.iloc[0,0]))
 
            #usa apenas os dados do dataframe filtado.. não gera o gráfico
            fig, df_aux = grafico_boxplot(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            
            texto = '### País valor médio de prato mais caro:'
            st.info(texto)
            texto = str(df_mean.iloc[0,0]) + ': $' +  str(df_mean.iloc[0,1])
            st.metric(label= '', value= texto, delta=None, delta_color="normal", help=None, label_visibility="visible")               
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
            #max_width = 700
            #max_height = 500                        
            operacao = 'count'

            filtro = df.loc[:, sort_by_col] == True
            grafico_percentual = False
            
            fig, df_aux = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order,
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
            #max_width = 700
            #max_height = 500                        
            operacao = 'count'

            filtro = df.loc[:,'Has Online delivery'] == True
            grafico_percentual = False
            
            fig, df_aux = grafico_barras(grafico_percentual, filtro, df, operacao, cols, group_by_col,sort_by_col, sort_by_col_order, 
                                 x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, False, 'all')
            
            st.plotly_chart(fig, use_conteiner_width = False)   

            
