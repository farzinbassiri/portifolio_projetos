
# importanto módulos e funções criadas para limpeza e pré-tratamento dos dados
#from data_wrangling_modules import *
# carregando demais biliotecas
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

st.set_page_config(page_title= 'Regiões de atendimento', layout='wide')

#--------------------------------------------------------------
#                    Barra Lateral    
#--------------------------------------------------------------
st.markdown('# Mapa para apoio à tomada de decisões ')
st.markdown("""___""")

# definição global de tamanho dos gráficos
max_width = 1024
max_height = 700


# Arquivos de entrada
try: #caminho para Streamlit
    df = pd.read_excel('Testes_Geoespaciais/dataset_DW.xlsx', sheet_name='Dados_tratados')
except: #caminho para uso local
	df = pd.read_excel('dataset/dataset_DW.xlsx', sheet_name='Dados_tratados')


start_location = [df.loc[:, 'lat'].median(), df.loc[:,'lon'].median()]
mapa = folium.Map(location= start_location, min_zoom = 0, zoom_start= 13, control_scale=False)
marker_cluster = MarkerCluster().add_to(mapa)
#adiciona os pontos geográficos ao mapa
for index, location_info in df.iterrows():
    if (location_info['lon']!=0) & (location_info['lat']!=0):
        popup_text = 'Logradouro: ' + str(location_info['Endereco'])
        folium.Marker( [location_info['lat'], location_info['lon']],
                        popup=location_info['Endereco'], 
                        icon=folium.Icon(icon='')
                     ).add_to(marker_cluster)

		
#criando abas
#Abas com as diferentes métricas 

tab1, tab2, tab3 = st.tabs(['Ruas com atendimentos', 'Ruas com colaboradores residentes', '-'])

# separa os códigos para cada aba
# todo código que estiber em 'with tab1 vai aparecer naquela aba

with tab1: 
	with st.container():
		folium_static(mapa, width = max_width, height = max_height)
		
		
with tab2:
	st.markdown('# Em desenvolvimento')