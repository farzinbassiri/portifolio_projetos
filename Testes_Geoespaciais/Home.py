
# importanto módulos e funções criadas para limpeza e pré-tratamento dos dados
#from data_wrangling_modules import *
# carregando demais biliotecas
import pandas as pd
import math
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

import os.path


st.set_page_config(page_title= 'Regiões de atendimento', layout='wide')

#--------------------------------------------------------------
#                    Barra Lateral    
#--------------------------------------------------------------
st.markdown('# Mapa para apoio à tomada de decisões ')
st.markdown("""___""")

st.sidebar.markdown('#### Escolha a largura desejada para o mapa')
max_width = st.sidebar.slider('', min_value=200, value=768, max_value=2048)

st.sidebar.markdown('#### Escolha a altura desejada para o mapa')
max_height = st.sidebar.slider('', min_value=201, value=500, max_value=768)

# definição global de tamanho dos gráficos
# max_width = 1024
# max_height = 700


# Arquivos de entrada
try: #caminho para Streamlit
    df = pd.read_excel('Testes_Geoespaciais/dataset_DW.xlsx', sheet_name='Dados_tratados')
except: #caminho para uso local
	df = pd.read_excel('dataset/dataset_DW.xlsx', sheet_name='Dados_tratados')






# funções
def angle(p1, p2):
    """Calcula o ângulo entre dois pontos em relação ao eixo x."""
    x_diff = p2[0] - p1[0]
    y_diff = p2[1] - p1[1]
    return math.atan2(y_diff, x_diff)

def organize_points(points):
    """Organiza os pontos para formar um polígono sem cruzamentos."""
    # Encontrar o ponto mais à esquerda
    start_point = min(points, key=lambda p: p[1])

    # Ordenar os pontos por ângulo em relação ao ponto inicial
    sorted_points = sorted(points, key=lambda p: angle(start_point, p))
    sorted_points.insert(0, start_point)

    return sorted_points


# busca dados de mapas especiais
try:
    df_mapa_1 = pd.read_excel('Testes_Geoespaciais/coordenadas_v1.xlsx', sheet_name='mapa_1')
except:
    df_mapa_1 = pd.read_excel(os.path.abspath(os.getcwd()) +'/dataset/coordenadas_v1.xlsx', sheet_name='mapa_1')

try: 
    df_mapa_2 = pd.read_excel('Testes_Geoespaciais/coordenadas_v1.xlsx', sheet_name='mapa_2')       

except:
    df_mapa_2 = pd.read_excel(os.path.abspath(os.getcwd()) + '/dataset/coordenadas_v1.xlsx', sheet_name='mapa_2') 
# acerta o formato
df_mapa_1.lat = df_mapa_1.lat.astype('float64')
df_mapa_1.lon = df_mapa_1.lon.astype('float64')
df_mapa_2.lat = df_mapa_2.lat.astype('float64')
df_mapa_2.lon = df_mapa_2.lon.astype('float64')

# Lista de coordenadas (latitude, longitude)
coordinates_m1 = df_mapa_1.loc[:,['lat','lon']].values
coordinates_m2 = df_mapa_2.loc[:,['lat','lon']].values
coordinates_m3 = df.loc[df.Tipo!=4,['lat','lon']].values

# Organizar os pontos
org_coordinates_m1 = organize_points(coordinates_m1)
org_coordinates_m2 = organize_points(coordinates_m2)
org_coordinates_m3 = organize_points(coordinates_m3)



#criando abas
#Abas com as diferentes métricas 

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(['Roteiro de Visitação',
                                                    'Famílias', 
                                                    'Equipe', 
                                                    'Escolas',
                                                    'Projetos & Instituições Públicas', 
                                                    'Zona de influência', 'Zona de influência com polígono'])

# separa os códigos para cada aba
# todo código que estiber em 'with tab1 vai aparecer naquela aba


	
with tab1:
    start_location = [df_mapa_1.loc[:, 'lat'].median(), df_mapa_1.loc[:,'lon'].median()]
    m1 = folium.Map(location= start_location, min_zoom = 0, zoom_start= 15, control_scale=True, max_bounds=True)
    marker_cluster = MarkerCluster().add_to(m1)
    
    folium.Polygon(locations=org_coordinates_m1,
                   color="blue",
                   weight=2,
                   fill_color="blue",
                   fill_opacity=0.2,
                   fill=True).add_to(m1)
    
    #adiciona os pontos geográficos ao mapa
    for index, location_info in df_mapa_1.iterrows():
        if (location_info['lon']!=0) & (location_info['lat']!=0):
            popup_text = 'Descrição: ' + str(location_info['Descricao'])
            folium.Marker( [location_info['lat'], location_info['lon']],
                            popup=location_info['Descricao'], 
                            icon=folium.Icon(icon='')
                         ).add_to(marker_cluster)


    start_location = [df_mapa_2.loc[:, 'lat'].median(), df_mapa_2.loc[:,'lon'].median()]
    m2 = folium.Map(location= start_location, min_zoom = 0, zoom_start= 14, control_scale=True, max_bounds=True)
    marker_cluster = MarkerCluster().add_to(m2)
    
    folium.Polygon(locations=org_coordinates_m2,
                   color="blue",
                   weight=2,
                   fill_color="blue",
                   fill_opacity=0.2,
                   fill=True).add_to(m2)
    
    #adiciona os pontos geográficos ao mapa
    for index, location_info in df_mapa_2.iterrows():
        if (location_info['lon']!=0) & (location_info['lat']!=0):
            popup_text = 'Descrição: ' + str(location_info['Descricao'])
            folium.Marker( [location_info['lat'], location_info['lon']],
                            popup=location_info['Descricao'], 
                            icon=folium.Icon(icon='')
                         ).add_to(marker_cluster)
    
    with st.container(border=False):
    	folium_static(m1, width = max_width, height = max_height)
    with st.container(border=False):
        folium_static(m2, width = max_width, height = max_height)

with tab2: 
    with st.container():
        filtro = df.Tipo == 1
        start_location = [df.loc[filtro, 'lat'].median(), df.loc[filtro,'lon'].median()]
        mapa = folium.Map(location= start_location, min_zoom = 0, zoom_start= 13, control_scale=False)
        
        marker_cluster = MarkerCluster().add_to(mapa)
        #adiciona os pontos geográficos ao mapa
        for index, location_info in df.loc[filtro,:].iterrows():
            if (location_info['lon']!=0) & (location_info['lat']!=0):
                popup_text = 'Descrição: ' + str(location_info['Descricao'])
                folium.Marker( [location_info['lat'], location_info['lon']],
                                popup=location_info['Descricao'], 
                                icon=folium.Icon(icon='')
                             ).add_to(marker_cluster)
        st.markdown("""___""")
        
        folium_static(mapa, width = max_width, height = max_height)
        # folium_static(mapa)	


with tab3:
    with st.container():
        filtro = df.Tipo == 2
        start_location = [df.loc[filtro, 'lat'].median(), df.loc[filtro,'lon'].median()]
        mapa = folium.Map(location= start_location, min_zoom = 0, zoom_start= 13, control_scale=False)
        
        marker_cluster = MarkerCluster().add_to(mapa)
        #adiciona os pontos geográficos ao mapa
        for index, location_info in df.loc[filtro,:].iterrows():
            if (location_info['lon']!=0) & (location_info['lat']!=0):
                popup_text = 'Descrição: ' + str(location_info['Descricao'])
                folium.Marker( [location_info['lat'], location_info['lon']],
                                popup=location_info['Descricao'], 
                                icon=folium.Icon(icon='')
                             ).add_to(marker_cluster)
        st.markdown("""___""")
        
        folium_static(mapa, width = max_width, height = max_height)
        # folium_static(mapa)
       

with tab4:
    with st.container():
        filtro = df.Tipo == 3
        st.markdown('#### Escolas, etc')
        start_location = [df.loc[filtro, 'lat'].median(), df.loc[filtro,'lon'].median()]
        mapa = folium.Map(location= start_location, min_zoom = 0, zoom_start= 13, control_scale=False)
        
        marker_cluster = MarkerCluster().add_to(mapa)
        #adiciona os pontos geográficos ao mapa
        for index, location_info in df.loc[filtro,:].iterrows():
            if (location_info['lon']!=0) & (location_info['lat']!=0):
                popup_text = 'Descrição: ' + str(location_info['Descricao'])
                folium.Marker( [location_info['lat'], location_info['lon']],
                                popup=location_info['Descricao'], 
                                icon=folium.Icon(icon='')
                             ).add_to(marker_cluster)
        st.markdown("""___""")
        
        folium_static(mapa, width = max_width, height = max_height)
        # folium_static(mapa)

with tab5:
    with st.container():
        filtro = df.Tipo == 4
        st.markdown('#### Escolas, etc')
        start_location = [df.loc[filtro, 'lat'].median(), df.loc[filtro,'lon'].median()]
        mapa = folium.Map(location= start_location, min_zoom = 0, zoom_start= 13, control_scale=False)
        
        marker_cluster = MarkerCluster().add_to(mapa)
        #adiciona os pontos geográficos ao mapa
        for index, location_info in df.loc[filtro,:].iterrows():
            if (location_info['lon']!=0) & (location_info['lat']!=0):
                popup_text = 'Descrição: ' + str(location_info['Descricao'])
                folium.Marker( [location_info['lat'], location_info['lon']],
                                popup=location_info['Descricao'], 
                                icon=folium.Icon(icon='')
                             ).add_to(marker_cluster)
        st.markdown("""___""")
        
        folium_static(mapa, width = max_width, height = max_height)
        # folium_static(mapa)


with tab6:
    with st.container():
        filtro = df.Tipo != 4
        st.markdown('##### A *zona de influência* é compreendida pela soma das regiões familias e as regiões com colaboradores residentes, formando a zona de influência positiva')
        start_location = [df.loc[filtro, 'lat'].median(), df.loc[filtro,'lon'].median()]
        mapa = folium.Map(location= start_location, min_zoom = 0, zoom_start= 12, control_scale=False)
        
        marker_cluster = MarkerCluster().add_to(mapa)
        #adiciona os pontos geográficos ao mapa
        for index, location_info in df.loc[filtro,:].iterrows():
            if (location_info['lon']!=0) & (location_info['lat']!=0):
                popup_text = 'Descrição: ' + str(location_info['Descricao'])
                folium.Marker( [location_info['lat'], location_info['lon']],
                                popup=location_info['Descricao'], 
                                icon=folium.Icon(icon='')
                             ).add_to(marker_cluster)
        st.markdown("""___""")
        
        folium_static(mapa, width = max_width, height = max_height)
        # folium_static(mapa)

with tab7:
    filtro = df.Tipo != 4
    st.markdown('##### A *zona de influência* é compreendida pela soma das regiões familias e as regiões com colaboradores residentes, formando a zona de influência positiva')
    start_location = [df.loc[filtro, 'lat'].median(), df.loc[filtro,'lon'].median()]
    m3 = folium.Map(location= start_location, min_zoom = 0, zoom_start= 12, control_scale=True, max_bounds=True)
    marker_cluster = MarkerCluster().add_to(m3)
    
    folium.Polygon(locations=org_coordinates_m3,
                   color="blue",
                   weight=2,
                   fill_color="blue",
                   fill_opacity=0.2,
                   fill=True).add_to(m3)
    
    #adiciona os pontos geográficos ao mapa
    for index, location_info in df.iterrows():
        if (location_info['lon']!=0) & (location_info['lat']!=0):
            popup_text = 'Descrição: ' + str(location_info['Descricao'])
            folium.Marker( [location_info['lat'], location_info['lon']],
                            popup=location_info['Descricao'], 
                            icon=folium.Icon(icon='')
                         ).add_to(marker_cluster)

    
    with st.container(border=False):
    	folium_static(m3, width = max_width, height = max_height)
       