
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

st.set_page_config(page_title= 'Localizacao', layout='wide')

#--------------------------------------------------------------
#                    Barra Lateral    
#--------------------------------------------------------------
st.markdown('# Aprendizado de Geolocalização')
st.markdown('## Marcadores com a localização de endereços')
st.markdown("""___""")


max_width = 1028
max_height = 702


# Arquivos de entrada
df = pd.read_excel('dataset_DW.xlsx', sheet_name='Dados_tratados')

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


folium_static(mapa, width = max_width, height = max_height)
