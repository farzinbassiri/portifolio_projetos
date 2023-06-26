
# importanto módulos e funções criadas para limpeza e pré-tratamento dos dados
from data_wrangling_modules import *
# carregando demais biliotecas
import pandas as pd
import plotly.express as px
import streamlit as st
import folium
from streamlit_folium import folium_static


# carregando a base de dados
# dados obtidos no site: https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv
df_raw = pd.read_csv('FTC-ZeroFomeDelivery/dataset/zomato.csv') 
df = data_wrangling(df_raw)
st.set_page_config(page_title= 'Visão Geral', layout='wide')
#--------------------------------------------------------------
#                    Barra Lateral    
#--------------------------------------------------------------
#filtro de TOP x países:
top_mode = st.sidebar.selectbox('Deseja limitar automaticamente a quantidade de países?', ('não', 'sim'))
if top_mode == 'sim':
    cols = ['City', 'Country_Name']
    group_by_col = 'Country_Name'
    sort_by_col = 'City'
    sort_by_col_order = [False] 
    operacao = 'nunique'
    df_mapa = df.loc[:,cols].groupby(group_by_col).nunique().sort_values(sort_by_col, ascending = sort_by_col_order).reset_index()
    top_mode = st.sidebar.slider(label = 'Defina quantidade de países', min_value= 1, max_value= len(df_mapa), value=2)
    df_mapa = df_mapa.loc[0:(top_mode-1), :]  
else: 
    df_mapa = df.loc[:,['Country_Name']].groupby('Country_Name').count().reset_index()
# seleção dos paises de interesse
paises = df.loc[:,['Country_Name']].groupby('Country_Name').count().reset_index()
country_options = st.sidebar.multiselect(
                        'Selecione os paises para indicação no mapa:',
                        paises['Country_Name'],
                        default = df_mapa['Country_Name'])

 

#--------------------------------------------------------------
#           Layout do dashboard - usando streamlit    
#--------------------------------------------------------------

#Abas com as diferentes métricas 
tab1, tab2, tab3 = st.tabs(['Visão Geral', '-', '-'])

# separa os códigos para cada aba
# todo código que estiber em 'with tab1 vai aparecer naquela aba

#Fome Zero!
#O Melhor lugar para encontrar seu mais novo restaurante favorito!
#Temos as seguintes marcas dentro da nossa plataforma:


with tab1: # 'Visão Geral'
    with st.container():
        st.header('Fome Zero! - Delivery')
    
    with st.container():
        st.markdown('### O Melhor lugar para encontrar seu mais novo restaurante favorito!')

    with st.container():
        st.markdown('#### Temos as seguintes marcas dentro da nossa plataforma:')
    
    with st.container():
        col1, col2, col3 = st.columns(3, gap="large")
        
        with col1:
            #2. Quantos países únicos estão registrados?
            
            count = len(df.loc[:, 'Restaurant ID'].unique())
            texto = '#### ' + str(count) + " restaurantes cadastrados"
            st.info(texto)
            #st.metric(value = count, label = '')
            #st.dataframe(df.head().style.format(thousands="."), use_container_width=True)
            
        with col2:
            #2. Quantos países únicos estão registrados?
            count = len(df.loc[:, 'Country_Name'].unique())
            texto = "#### Presente em " + str(count) + " países"
            st.info(texto)
            
        with col3:
            #3. Quantas cidades únicas estão registradas?
            count = len(df.loc[:, 'City'].unique())
            texto = '#### ' + str(count) + " cidades atendidas"
            st.info(texto)
            
    with st.container():
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            #4. Qual o total de avaliações feitas?
            votes_sum = df.loc[:, 'Votes'].sum()
            votes_milhao = int(votes_sum/1000000)
            votes_milhar = int((votes_sum - votes_milhao*1000000)/1000)
            votes_centena = (votes_sum - votes_milhao*1000000)-votes_milhar*1000
            texto = '#### ' + str(votes_milhao) + '.' + str(votes_milhar) + '.' + str(votes_centena) + ' avaliações realizadas'
            st.info(texto)
            #st.metric(value = votes_sum, label = '')
            
        with col2:
            #5. Qual o total de tipos de culinária registrados?¶
            count = len(df.loc[:, 'Cuisines'].unique())
            texto = '#### ' + str(count) + " tipos de culinária disponíveis"
            st.info(texto)

    with st.container():
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            #deixa o filtro vazio, assim irá buscar todos os dados
            filtro = pd.DataFrame({'A' : []})
        with col2:
            #deixa o filtro vazio, assim irá buscar todos os dados
            dummy = pd.DataFrame({'A' : []})
            
    with st.container():
        col1, col2 = st.columns(2, gap="large")
        
        with col1:        
            #deixa o filtro vazio, assim irá buscar todos os dados
            dummy = pd.DataFrame({'A' : []})
            
        with col2:
            #deixa o filtro vazio, assim irá buscar todos os dados
            dummy = pd.DataFrame({'A' : []})
            
    with st.container():
        cols = ['City', 'Country_Name', 'Latitude', 'Longitude']
        group_by_col = ['City','Country_Name']
        latitude = 'Latitude'
        longitude = 'Longitude'
        st.markdown('# Restaurantes Cadastrados')
        #filtro dos paises selecionados
        filtro_pais = df['Country_Name'].isin(country_options)
        
        mapa = grafico_country_map(df.loc[filtro_pais,:], cols, group_by_col, latitude, longitude)
        max_width = 1024
        max_height = 500    
        folium_static(mapa, width = max_width, height = max_height)
        
