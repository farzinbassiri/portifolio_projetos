
# importanto módulos e funções criadas para limpeza e pré-tratamento dos dados
from data_wrangling_modules import *
# carregando demais biliotecas
import pandas as pd
import plotly.express as px
import streamlit as st

# carregando a base de dados
# dados obtidos no site: https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv
df_raw = pd.read_csv('dataset\\zomato.csv')
df = data_wrangling(df_raw)
st.set_page_config(page_title= 'Visão Culinária', layout='wide')
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

tab1, tab2, tab3 = st.tabs(['-', '-', '-'])

# separa os códigos para cada aba
# todo código que estiber em 'with tab1 vai aparecer naquela aba

with tab1: # 'Visão Geral'
    st.markdown('## Melhores Restaurantes dos Principais tipos Culinários')
    with st.container():
        col1, col2, col3, col4 = st.columns(4, gap="large")
        with col1:
            # 1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?
            cols = ['Restaurant Name', 'Restaurant ID', 'Cuisines', 'AVG_cost_4_2', 'Aggregate rating', 'City','Country_Name']
            group_by_col = ['Restaurant Name', 'Aggregate rating', 'City','Country_Name', 'AVG_cost_4_2']
            sort_by_col = ['Aggregate rating', 'Restaurant ID']
            sort_by_col_order = [False, True] 
            col_calc = 'Aggregate rating'
            operacao = 'mean'
            filtro = df['Cuisines'] == 'Italian'

            resultado = classificacao(filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, col_calc)
            texto = str(resultado.iloc[0,1]) + '\n / 5.0'
            st.metric(label= '##### Culinária Italiana \n Melhor restaurante:  ', value= texto, delta=None, delta_color="normal", help=None, label_visibility="visible")
            with st.expander("Mais informações:"):
                st.write('-- Restaurante: ' + str(resultado.iloc[0,0]) + 
                         '\n\n -- Localização: ' + str(resultado.iloc[0,2] + '/' + str(resultado.iloc[0,3])) +
                         '\n\n -- Preço Médio: USD ' + str(np.round(resultado.iloc[0,4],2)) + 
                         '\n\n Quantidade de restaurantes deste tipo na base: ' + str(len(resultado)))
            
        with col2:
            # 2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?
            cols = ['Restaurant Name', 'Restaurant ID', 'Cuisines', 'AVG_cost_4_2', 'Aggregate rating', 'City','Country_Name']
            group_by_col = ['Restaurant Name', 'Aggregate rating', 'City','Country_Name', 'AVG_cost_4_2']
            sort_by_col = ['Aggregate rating', 'Restaurant ID']
            sort_by_col_order = [True, True] 
            col_calc = 'Aggregate rating'
            operacao = 'mean'
            filtro = df['Cuisines'] == 'Italian'

            resultado = classificacao(filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, col_calc)
            texto = str(resultado.iloc[0,1]) + '\n / 5.0'
            st.metric(label= '##### Culinária Italiana \n Pior restaurante:  ', value= texto, delta=None, delta_color="normal", help=None, label_visibility="visible")
            with st.expander("Mais informações:"):
                st.write('-- Restaurante: ' + str(resultado.iloc[0,0]) + 
                         '\n\n -- Localização: ' + str(resultado.iloc[0,2] + '/' + str(resultado.iloc[0,3])) +
                         '\n\n -- Preço Médio: USD ' + str(np.round(resultado.iloc[0,4],2)) +
                         '\n\n Quantidade de restaurantes deste tipo na base: ' + str(len(resultado)))
        
        with col3:
            # 1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?
            cols = ['Restaurant Name', 'Restaurant ID', 'Cuisines', 'AVG_cost_4_2', 'Aggregate rating', 'City','Country_Name']
            group_by_col = ['Restaurant Name', 'Aggregate rating', 'City','Country_Name', 'AVG_cost_4_2']
            sort_by_col = ['Aggregate rating', 'Restaurant ID']
            sort_by_col_order = [False, True] 
            col_calc = 'Aggregate rating'
            operacao = 'mean'
            filtro = df['Cuisines'] == 'American'

            resultado = classificacao(filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, col_calc)
            texto = str(resultado.iloc[0,1]) + '\n / 5.0'
            st.metric(label= '##### Culinária Americana \n Melhor restaurante:  ', value= texto, delta=None, delta_color="normal", help=None, label_visibility="visible")
            with st.expander("Mais informações:"):
                st.write('-- Restaurante: ' + str(resultado.iloc[0,0]) + 
                         '\n\n -- Localização: ' + str(resultado.iloc[0,2] + '/' + str(resultado.iloc[0,3])) +
                         '\n\n -- Preço Médio: USD ' + str(np.round(resultado.iloc[0,4],2)) + 
                         '\n\n Quantidade de restaurantes deste tipo na base: ' + str(len(resultado)))
            
        with col4:
            # 2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?
            cols = ['Restaurant Name', 'Restaurant ID', 'Cuisines', 'AVG_cost_4_2', 'Aggregate rating', 'City','Country_Name']
            group_by_col = ['Restaurant Name', 'Aggregate rating', 'City','Country_Name', 'AVG_cost_4_2']
            sort_by_col = ['Aggregate rating', 'Restaurant ID']
            sort_by_col_order = [True, True] 
            col_calc = 'Aggregate rating'
            operacao = 'mean'
            filtro = df['Cuisines'] == 'American'

            resultado = classificacao(filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, col_calc)
            texto = str(resultado.iloc[0,1]) + '\n / 5.0'
            st.metric(label= '##### Culinária Americana \n Pior restaurante:  ', value= texto, delta=None, delta_color="normal", help=None, label_visibility="visible")
            with st.expander("Mais informações:"):
                st.write('-- Restaurante: ' + str(resultado.iloc[0,0]) + 
                         '\n\n -- Localização: ' + str(resultado.iloc[0,2] + '/' + str(resultado.iloc[0,3])) +
                         '\n\n -- Preço Médio: USD ' + str(np.round(resultado.iloc[0,4],2)) + 
                         '\n\n Quantidade de restaurantes deste tipo na base: ' + str(len(resultado)))        

with st.container():
        col1, col2, col3, col4 = st.columns(4, gap="large")
        with col1:
            # 1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?
            cols = ['Restaurant Name', 'Restaurant ID', 'Cuisines', 'AVG_cost_4_2', 'Aggregate rating', 'City','Country_Name']
            group_by_col = ['Restaurant Name', 'Aggregate rating', 'City','Country_Name', 'AVG_cost_4_2']
            sort_by_col = ['Aggregate rating', 'Restaurant ID']
            sort_by_col_order = [False, True] 
            col_calc = 'Aggregate rating'
            operacao = 'mean'
            filtro = df['Cuisines'] == 'Arabian'

            resultado = classificacao(filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, col_calc)
            texto = str(resultado.iloc[0,1]) + '\n / 5.0'
            st.metric(label= '##### Culinária Árabe \n Melhor restaurante:  ', value= texto, delta=None, delta_color="normal", help=None, label_visibility="visible")
            with st.expander("Mais informações:"):
                st.write('-- Restaurante: ' + str(resultado.iloc[0,0]) + 
                         '\n\n -- Localização: ' + str(resultado.iloc[0,2] + '/' + str(resultado.iloc[0,3])) +
                         '\n\n -- Preço Médio: USD ' + str(np.round(resultado.iloc[0,4],2)) + 
                         '\n\n Quantidade de restaurantes deste tipo na base: ' + str(len(resultado)))
            
        with col2:
            # 2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?
            cols = ['Restaurant Name', 'Restaurant ID', 'Cuisines', 'AVG_cost_4_2', 'Aggregate rating', 'City','Country_Name']
            group_by_col = ['Restaurant Name', 'Aggregate rating', 'City','Country_Name', 'AVG_cost_4_2']
            sort_by_col = ['Aggregate rating', 'Restaurant ID']
            sort_by_col_order = [True, True] 
            col_calc = 'Aggregate rating'
            operacao = 'mean'
            filtro = df['Cuisines'] == 'Arabian'

            resultado = classificacao(filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, col_calc)
            texto = str(resultado.iloc[0,1]) + '\n / 5.0'
            st.metric(label= '##### Culinária Árabe \n Pior restaurante:  ', value= texto, delta=None, delta_color="normal", help=None, label_visibility="visible")
            with st.expander("Mais informações:"):
                st.write('-- Restaurante: ' + str(resultado.iloc[0,0]) + 
                         '\n\n -- Localização: ' + str(resultado.iloc[0,2] + '/' + str(resultado.iloc[0,3])) +
                         '\n\n -- Preço Médio: USD ' + str(np.round(resultado.iloc[0,4],2)) + 
                         '\n\n Quantidade de restaurantes deste tipo na base: ' + str(len(resultado)))
        
        with col3:
            # 1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?
            cols = ['Restaurant Name', 'Restaurant ID', 'Cuisines', 'AVG_cost_4_2', 'Aggregate rating', 'City','Country_Name']
            group_by_col = ['Restaurant Name', 'Aggregate rating', 'City','Country_Name', 'AVG_cost_4_2']
            sort_by_col = ['Aggregate rating', 'Restaurant ID']
            sort_by_col_order = [False, True] 
            col_calc = 'Aggregate rating'
            operacao = 'mean'
            filtro = df['Cuisines'] == 'Japanese'

            resultado = classificacao(filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, col_calc)
            texto = str(resultado.iloc[0,1]) + '\n / 5.0'
            st.metric(label= '##### Culinária Japonesa \n Melhor restaurante:  ', value= texto, delta=None, delta_color="normal", help=None, label_visibility="visible")
            with st.expander("Mais informações:"):
                st.write('-- Restaurante: ' + str(resultado.iloc[0,0]) + 
                         '\n\n -- Localização: ' + str(resultado.iloc[0,2] + '/' + str(resultado.iloc[0,3])) +
                         '\n\n -- Preço Médio: USD ' + str(np.round(resultado.iloc[0,4],2)) + 
                         '\n\n Quantidade de restaurantes deste tipo na base: ' + str(len(resultado)))
            
        with col4:
            # 2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?
            cols = ['Restaurant Name', 'Restaurant ID', 'Cuisines', 'AVG_cost_4_2', 'Aggregate rating', 'City','Country_Name']
            group_by_col = ['Restaurant Name', 'Aggregate rating', 'City','Country_Name', 'AVG_cost_4_2']
            sort_by_col = ['Aggregate rating', 'Restaurant ID']
            sort_by_col_order = [True, True] 
            col_calc = 'Aggregate rating'
            operacao = 'mean'
            filtro = df['Cuisines'] == 'Japanese'

            resultado = classificacao(filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, col_calc)
            texto = str(resultado.iloc[0,1]) + '\n / 5.0'
            st.metric(label= '##### Culinária Japonesa \n Pior restaurante:  ', value= texto, delta=None, delta_color="normal", help=None, label_visibility="visible")
            with st.expander("Mais informações:"):
                st.write('-- Restaurante: ' + str(resultado.iloc[0,0]) + 
                         '\n\n -- Localização: ' + str(resultado.iloc[0,2] + '/' + str(resultado.iloc[0,3])) +
                         '\n\n -- Preço Médio: USD ' + str(np.round(resultado.iloc[0,4],2)) + 
                         '\n\n Quantidade de restaurantes deste tipo na base: ' + str(len(resultado)))        
                
with st.container():
        col1, col2, col3, col4 = st.columns(4, gap="large")
        with col1:
            # 1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?
            cols = ['Restaurant Name', 'Restaurant ID', 'Cuisines', 'AVG_cost_4_2', 'Aggregate rating', 'City','Country_Name']
            group_by_col = ['Restaurant Name', 'Aggregate rating', 'City','Country_Name', 'AVG_cost_4_2']
            sort_by_col = ['Aggregate rating', 'Restaurant ID']
            sort_by_col_order = [False, True] 
            col_calc = 'Aggregate rating'
            operacao = 'mean'
            filtro = df['Cuisines'] == 'Home-made'

            resultado = classificacao(filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, col_calc)
            texto = str(resultado.iloc[0,1]) + '\n / 5.0'
            st.metric(label= '##### Culinária Caseira \n Melhor restaurante:  ', value= texto, delta=None, delta_color="normal", help=None, label_visibility="visible")
            with st.expander("Mais informações:"):
                st.write('-- Restaurante: ' + str(resultado.iloc[0,0]) + 
                         '\n\n -- Localização: ' + str(resultado.iloc[0,2] + '/' + str(resultado.iloc[0,3])) +
                         '\n\n -- Preço Médio: USD ' + str(np.round(resultado.iloc[0,4],2)) + 
                         '\n\n Quantidade de restaurantes deste tipo na base: ' + str(len(resultado)))
            
        with col2:
            # 2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?
            cols = ['Restaurant Name', 'Restaurant ID', 'Cuisines', 'AVG_cost_4_2', 'Aggregate rating', 'City','Country_Name']
            group_by_col = ['Restaurant Name', 'Aggregate rating', 'City','Country_Name', 'AVG_cost_4_2']
            sort_by_col = ['Aggregate rating', 'Restaurant ID']
            sort_by_col_order = [True, True] 
            col_calc = 'Aggregate rating'
            operacao = 'mean'
            filtro = df['Cuisines'] == 'Home-made'

            resultado = classificacao(filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, col_calc)
            texto = str(resultado.iloc[0,1]) + '\n / 5.0'
            st.metric(label= '##### Culinária Caseira \n Pior restaurante:  ', value= texto, delta=None, delta_color="normal", help=None, label_visibility="visible")
            with st.expander("Mais informações:"):
                st.write('-- Restaurante: ' + str(resultado.iloc[0,0]) + 
                         '\n\n -- Localização: ' + str(resultado.iloc[0,2] + '/' + str(resultado.iloc[0,3])) +
                         '\n\n -- Preço Médio: USD ' + str(np.round(resultado.iloc[0,4],2)) + 
                         '\n\n Quantidade de restaurantes deste tipo na base: ' + str(len(resultado)))
        
        
        
with st.container():
    st.markdown("""___""")
    st.markdown('## Dados sobre os tipos de culinária')
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        #11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas?
        cols = ['Restaurant Name', 'Restaurant ID', 'Cuisines', 'AVG_cost_4_2', 'City','Country_Name']
        group_by_col = ['Restaurant Name', 'AVG_cost_4_2', 'Cuisines', 'City','Country_Name']
        sort_by_col = ['AVG_cost_4_2', 'Restaurant ID']
        sort_by_col_order = [False, True] 
        col_calc = 'Aggregate rating'
        operacao = 'mean'
        filtro = df['Cuisines'] != ''

        resultado = classificacao(filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, col_calc)

        texto = str(resultado.iloc[0,2])
        st.metric(label= '##### Culinária com prato mais caro:  ', value= texto, delta=None, delta_color="normal", help=None, label_visibility="visible")
        with st.expander("Mais informações:"):
            st.write('-- Restaurante: ' + str(resultado.iloc[0,0]) + 
                     '\n\n -- Localização: ' + str(resultado.iloc[0,3] + '/' + str(resultado.iloc[0,4])) +
                     '\n\n -- Preço Médio: USD ' + str(np.round(resultado.iloc[0,1],2)))

            
    with col2:
        #12. Qual o tipo de culinária que possui a maior nota média?
        cols = ['Restaurant Name', 'Restaurant ID', 'Cuisines', 'Aggregate rating', 'City','Country_Name']
        group_by_col = ['Restaurant Name', 'Aggregate rating', 'Cuisines', 'City','Country_Name']
        sort_by_col = ['Aggregate rating', 'Restaurant ID']
        sort_by_col_order = [False, True] 
        col_calc = 'Aggregate rating'
        operacao = 'mean'
        filtro = df['Cuisines'] != ''

        resultado = classificacao(filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, col_calc)
        texto = str(resultado.iloc[0,2])
        st.metric(label= '##### Culinária com melhor avaliação:  ', value= texto, delta=None, delta_color="normal", help=None, label_visibility="visible")
        with st.expander("Mais informações:"):
            st.write('-- Restaurante: ' + str(resultado.iloc[0,0]) + 
                     '\n\n -- Localização: ' + str(resultado.iloc[0,3] + '/' + str(resultado.iloc[0,4])) +
                     '\n\n -- Preço Médio: USD ' + str(np.round(resultado.iloc[0,1],2)))

    with col3:
        #13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas?
        cols = ['Restaurant ID', 'Cuisines', 'Has Online delivery', 'Is delivering now', 'City','Country_Name']
        group_by_col = ['Cuisines']
        sort_by_col = ['Restaurant ID']
        sort_by_col_order = [False] 
        col_calc = 'Restaurant ID'
        operacao = 'count'
        filtro = (df['Has Online delivery'] == True) & (df['Is delivering now'] == True)

        resultado = classificacao(filtro, df, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, col_calc)
        texto = str(resultado.iloc[0,0])
        st.metric(label= '##### Culinária com mais restaurantes que \n ' +  
                  '##### aceitam pedidos online e fazem entregas:  ', value= texto, delta=None, delta_color="normal", help=None, label_visibility="visible")

        with st.expander("Mais informações:"):
            st.write('-- Quantidade de Restaurantes: ' + str(resultado.iloc[0,1]))        
            

