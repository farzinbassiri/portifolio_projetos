"""
Projeto Final do curso FTC Análise de Dados com Python
Objetivo: 
    - tomar as melhores decisões estratégicas e alavancar ainda mais a Fome Zero, e para isso, fazer uma análise nos dados da empresa, geração de dashboards, a partir dessas análises, para responder às diversas perguntas.

Este módulo contem as funções que serão utilizadas no progrma principal.

"""

# carregando biliotecas
import pandas as pd
import plotly.express as px
import numpy as np
import folium
from streamlit_folium import folium_static
import streamlit.components.v1 as components
from folium.plugins import MarkerCluster


# transforma os dados da coluna "Price Range" 
def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
    

def data_wrangling(df):

    # ordena os dados para os cadastros mais antigos serem os primeiros da lista
    df = df.sort_values('Restaurant ID', ascending = True)
    # elimina cadastros repetidos
    df = df.drop_duplicates(subset=['Restaurant ID', 'Restaurant Name'], keep='first', inplace=False, ignore_index=False)

    # converte as colunas com dados 0 ou 1 para boolean.
    df['Has Table booking'] = df['Has Table booking'].astype(bool)
    df['Has Online delivery'] = df['Has Online delivery'].astype(bool)
    df['Is delivering now'] = df['Is delivering now'].astype(bool)
    df['Switch to order menu'] = df['Switch to order menu'].astype(bool)

    # separa os dados de tipos de culinária e retem apenas o primeiro listado
    df['Cuisines'] = df['Cuisines'].astype(str)
    df['Cuisines'] = df.loc[:, 'Cuisines'].apply(lambda x: x.split(",")[0])
    linhas_validas = df['Cuisines'] != 'nan'
    #transfere para o dataframe apenas as linhas que contém dados
    df = df.loc[linhas_validas, :]
    # refaz o index depois de remover as linhas inválidas
    df = df.reset_index(drop = True)

    # cria coluna nova com o nome dos países
    linhas_selecionadas = (df['Country Code'] == 1)
    df.loc[linhas_selecionadas, 'Country_Name'] = 'India'
    linhas_selecionadas = (df['Country Code'] == 14)
    df.loc[linhas_selecionadas, 'Country_Name'] = 'Australia'
    linhas_selecionadas = (df['Country Code'] == 30)
    df.loc[linhas_selecionadas, 'Country_Name'] = 'Brazil'
    linhas_selecionadas = (df['Country Code'] == 37)
    df.loc[linhas_selecionadas, 'Country_Name'] = 'Canada'
    linhas_selecionadas = (df['Country Code'] == 94)
    df.loc[linhas_selecionadas, 'Country_Name'] = 'Indonesia'
    linhas_selecionadas = (df['Country Code'] == 148)
    df.loc[linhas_selecionadas, 'Country_Name'] = 'New Zeland'
    linhas_selecionadas = (df['Country Code'] == 162)
    df.loc[linhas_selecionadas, 'Country_Name'] = 'Philippines'
    linhas_selecionadas = (df['Country Code'] == 166)
    df.loc[linhas_selecionadas, 'Country_Name'] = 'Qatar'
    linhas_selecionadas = (df['Country Code'] == 184)
    df.loc[linhas_selecionadas, 'Country_Name'] = 'Singapure'
    linhas_selecionadas = (df['Country Code'] == 189)
    df.loc[linhas_selecionadas, 'Country_Name'] = 'South Africa'
    linhas_selecionadas = (df['Country Code'] == 191)
    df.loc[linhas_selecionadas, 'Country_Name'] = 'Sri Lanka'
    linhas_selecionadas = (df['Country Code'] == 208)
    df.loc[linhas_selecionadas, 'Country_Name'] = 'Turkey'
    linhas_selecionadas = (df['Country Code'] == 214)
    df.loc[linhas_selecionadas, 'Country_Name'] = 'United Arab Emirates'
    linhas_selecionadas = (df['Country Code'] == 215)
    df.loc[linhas_selecionadas, 'Country_Name'] = 'England'
    linhas_selecionadas = (df['Country Code'] == 216)
    df.loc[linhas_selecionadas, 'Country_Name'] = 'United States of America'


    # faz conversão de moeda local para USD, baseado no câmbio de 30/05/2023, 09:21 UTC
        # 1 INR = 0.012085 USD 
        # 1 $ = 1USD
        # 1 GBP	= 1.23494 USD
        # 1 R = 0.051 USD
        # 1 AED = 0.27 USD
        # 1 R$ = 0.20 USD
        # 1 NZD = 0.60445 USD
        # 1 TL = 0.0497803 USD
        # 1 P = 0.073 USD
        # 1 IDR = 0.000067 USD
        # 1 QR = 0.27 USD
        # 1 LKR = 0.0034014481 USD


    cols = ['Average Cost for two', 'Currency','Country_Name']
    df_currency = df.loc[:,cols].groupby('Currency').count().reset_index()


    # novos valores são registrados em uma nova coluna 'AVG_cos_4_2'
    for moeda in df_currency['Currency']:
        linhas_selec = df.loc[:, 'Currency'] == moeda
        if moeda == 'Indian Rupees(Rs.)':
            df.loc[linhas_selec, 'AVG_cost_4_2'] = df.loc[linhas_selec, 'Average Cost for two']*0.012085
        elif moeda == 'Dollar($)':
            df.loc[linhas_selec, 'AVG_cost_4_2'] = df.loc[linhas_selec, 'Average Cost for two']
        elif moeda == 'Pounds(£)':
            df.loc[linhas_selec, 'AVG_cost_4_2'] = df.loc[linhas_selec, 'Average Cost for two']*1.23494
        elif moeda == 'Rand(R)':
            df.loc[linhas_selec, 'AVG_cost_4_2'] = df.loc[linhas_selec, 'Average Cost for two']*0.051
        elif moeda == 'Emirati Diram(AED)':
            df.loc[linhas_selec, 'AVG_cost_4_2'] = df.loc[linhas_selec, 'Average Cost for two']*0.27
        elif moeda == 'Brazilian Real(R$)':
            df.loc[linhas_selec, 'AVG_cost_4_2'] = df.loc[linhas_selec, 'Average Cost for two']*0.20
        elif moeda == 'NewZealand($)':
            df.loc[linhas_selec, 'AVG_cost_4_2'] = df.loc[linhas_selec, 'Average Cost for two']*0.60445
        elif moeda == 'Turkish Lira(TL)':
            df.loc[linhas_selec, 'AVG_cost_4_2'] = df.loc[linhas_selec, 'Average Cost for two']*0.0497803
        elif moeda == 'Botswana Pula(P)':
            df.loc[linhas_selec, 'AVG_cost_4_2'] = df.loc[linhas_selec, 'Average Cost for two']*0.073
        elif moeda == 'Indonesian Rupiah(IDR)':
            df.loc[linhas_selec, 'AVG_cost_4_2'] = df.loc[linhas_selec, 'Average Cost for two']*0.000067
        elif moeda == 'Qatari Rial(QR)':
            df.loc[linhas_selec, 'AVG_cost_4_2'] = df.loc[linhas_selec, 'Average Cost for two']*0.27
        elif moeda == 'Sri Lankan Rupee(LKR)':        
            df.loc[linhas_selec, 'AVG_cost_4_2'] = df.loc[linhas_selec, 'Average Cost for two']*0.0034014481


                
    # limpa linha que tem outlier na Austrália
    cols = ['Restaurant ID', 'AVG_cost_4_2', 'Country_Name']
    group_by_col = 'Country_Name'
    sort_by_col = 'AVG_cos_4_2'

    linhas_selec = df.loc[:, 'Country_Name'] == 'Australia'
    drop_row = df.loc[linhas_selec,cols]['AVG_cost_4_2'].idxmax()
    df=df.drop(index = drop_row)                

    # apaga a coluna que contém apenas dados nulos
    df=df.drop('Switch to order menu', axis = 1)    
                

    for valor in range(1,5):
        linhas = df.loc[:, 'Price range'] == valor
        price_range = create_price_tye(valor)
        df.loc[linhas, 'Price range'] = price_range
        
    
    # atribui cor ao codigo de cores
    linhas_selecionadas = (df['Rating color'] == "3F7E00")
    df.loc[linhas_selecionadas, 'Rating_color'] = 'darkgreen'

    linhas_selecionadas = (df['Rating color'] == "5BA829")
    df.loc[linhas_selecionadas, 'Rating_color'] = 'green'

    linhas_selecionadas = (df['Rating color'] == "9ACD32")
    df.loc[linhas_selecionadas, 'Rating_color'] = 'lightgreen'

    linhas_selecionadas = (df['Rating color'] == "CDD614")
    df.loc[linhas_selecionadas, 'Rating_color'] = 'orange'

    linhas_selecionadas = (df['Rating color'] == "FFBA00")
    df.loc[linhas_selecionadas, 'Rating_color'] = 'lightred'

    linhas_selecionadas = (df['Rating color'] == "CBCBC8")
    df.loc[linhas_selecionadas, 'Rating_color'] = 'red'

    linhas_selecionadas = (df['Rating color'] == "FF7800")
    df.loc[linhas_selecionadas, 'Rating_color'] = 'darkred'    


    
    # padroniza as avaliações. Os dados foram todos colocados em ingles.
    linhas_selecionadas = ((df['Rating text'] == 'Excelente') |
                            (df['Rating text'] == 'Eccellente') |
                            (df['Rating text'] == 'Harika') |
                            (df['Rating text'] == 'Vynikajúce') |
                            (df['Rating text'] == 'Terbaik') |
                            (df['Rating text'] == 'Wybitnie') |
                            (df['Rating text'] == 'Skvělé')| 
                            (df['Rating text'] == 'Skvělá volba'))

    df.loc[linhas_selecionadas, 'Rating text'] = 'Excellent'

    linhas_selecionadas = ((df['Rating text'] == 'Muito Bom') |
                         (df['Rating text'] == 'Muito Bom') |
                         (df['Rating text'] == 'Muito bom') |
                         (df['Rating text'] == 'Muy Bueno') |
                         (df['Rating text'] == 'Çok iyi') |
                         (df['Rating text'] == 'Velmi dobré') |
                         (df['Rating text'] == 'Bardzo dobrze') |
                         (df['Rating text'] == 'Sangat Baik') |
                         (df['Rating text'] == 'Veľmi dobré'))

    df.loc[linhas_selecionadas, 'Rating text'] = 'Very Good'

    linhas_selecionadas = ((df['Rating text'] == 'Bueno') |
                         (df['Rating text'] == 'Buono') |
                         (df['Rating text'] == 'Bom') |
                         (df['Rating text'] == 'Baik') |
                         (df['Rating text'] == 'İyi'))

    df.loc[linhas_selecionadas, 'Rating text'] = 'Good'

    linhas_selecionadas = (df['Rating text'] == 'Biasa')
    df.loc[linhas_selecionadas, 'Rating text'] = 'Average'    
    
    #cria coluna com nota numérica
    linhas_selecionadas = (df['Rating text'] == 'Excellent')
    df.loc[linhas_selecionadas, 'Rating_note'] = 5

    linhas_selecionadas = (df['Rating text'] == 'Very Good')
    df.loc[linhas_selecionadas, 'Rating_note'] = 4

    linhas_selecionadas = (df['Rating text'] == 'Good')
    df.loc[linhas_selecionadas, 'Rating_note'] = 3

    linhas_selecionadas = (df['Rating text'] == 'Average')
    df.loc[linhas_selecionadas, 'Rating_note'] = 2

    linhas_selecionadas = (df['Rating text'] == 'Poor')
    df.loc[linhas_selecionadas, 'Rating_note'] = 1

    #coloca um valor impossível para ser depois trocado pelo valor médio do pais
    linhas_selecionadas = (df['Rating text'] == 'Not rated')
    df.loc[linhas_selecionadas, 'Rating_note'] = 100

    #converte avaliações em numero
    df['Rating_note'] = df['Rating_note'].astype(int)    
    
    # coloca a nota média nas linhas sem voto
    cols = ['Rating text', 'Rating_note', 'Country_Name']
    sort_by_col = 'Rating_note'
    group_by_col = 'Country_Name' 

    filtro = ((df['Rating_note'] > 10) )

    df_aux = df.loc[filtro, cols].groupby(group_by_col).mean(sort_by_col).sort_values(sort_by_col, ascending = False).reset_index()
    
    
    for pais in df_aux.loc[:,'Country_Name']:
        filtro = ((df['Rating text'] == 'Not rated') & (df['Country_Name'] == pais))
        filtro_media = ((df['Rating_note'] < 10) & (df['Country_Name'] == pais) )

        tmp = df.loc[filtro_media, cols].groupby(group_by_col).mean(sort_by_col).sort_values(sort_by_col, ascending = False).reset_index()
        df.loc[filtro, 'Rating_note'] = tmp.iloc[0,1]
    
    
    return df


def grafico_barras(dados_relativos, filtro, df1, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, 
                   x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, color_attribute, top_mode):
    percentual = pd.DataFrame()
    
    if filtro.empty == True:
        #não faz filtro
        if operacao == 'nunique':
            df_aux = df1.loc[:,cols].groupby(group_by_col).nunique().sort_values(sort_by_col, ascending = sort_by_col_order).reset_index()
        elif operacao == 'count':
            df_aux = df1.loc[:, cols].groupby(group_by_col).count().sort_values(sort_by_col, ascending = sort_by_col_order).reset_index()    
        elif operacao == 'sum':
            df_aux = df1.loc[:, cols].groupby(group_by_col).sum().sort_values(sort_by_col, ascending = sort_by_col_order).reset_index()    
        elif operacao == 'mean':
            df_aux = df1.loc[:, cols].groupby(group_by_col).mean().round(decimals=2).sort_values(sort_by_col, ascending = sort_by_col_order).reset_index()            
    else:
        # faz filtro
        if operacao == 'nunique':
            df_aux = df1.loc[filtro,cols].groupby(group_by_col).nunique().sort_values(sort_by_col, ascending = sort_by_col_order).reset_index()
        elif operacao == 'count':
            df_aux = df1.loc[filtro, cols].groupby(group_by_col).count().sort_values(sort_by_col, ascending = sort_by_col_order).reset_index()
        elif operacao == 'sum':
            df_aux = df1.loc[filtro, cols].groupby(group_by_col).sum().sort_values(sort_by_col, ascending = sort_by_col_order).reset_index()    
        elif operacao == 'mean':
            df_aux = df1.loc[filtro, cols].groupby(group_by_col).mean().round(decimals=2).sort_values(sort_by_col, ascending = sort_by_col_order).reset_index()               

    # altera o nome da coluna ID
    #df_aux.columns = [x_axis, y_axis]
    
    if color_attribute == False:  
        #se não vai por cor nas colunas
        if dados_relativos == True:
            # determina o numero total de restaurantes por pais
            df_qde_rest = (df1.loc[:,[cols[0], cols[1]]]
                               .groupby(cols[1])
                               .count()
                               .sort_values(cols[0], ascending = False)
                               .reset_index())    

            # calcula os dados relativos
            for row in df_aux.index:
                pais = df_aux.loc[row,cols[1]] 
                numerador = df_aux.loc[row, cols[0]]
                denominador = (df_qde_rest.loc[df_qde_rest[cols[1]] == pais]
                                          .iloc[0,1])

                percentual.loc[row,cols[1]] = pais
                percentual.loc[row,cols[0]] = np.round(100*(numerador/denominador),1)
            df_aux = percentual
    else:
        #se vai por cor nas colunas
        # determina o numero total de restaurantes por pais
        if dados_relativos == True:
            df_qde_rest = (df1.loc[:,[cols[0], cols[1], cols[2]]]
                               .groupby([cols[1], cols[2]])
                               .count()
                               .sort_values(cols[0], ascending = False)
                               .reset_index())    

            # calcula os dados relativos
            for row in df_aux.index:
                pais = df_aux.loc[row,cols[1]] 
                numerador = df_aux.loc[row, cols[0]]
                denominador = (df_qde_rest.loc[df_qde_rest[cols[1]] == pais]
                                          .iloc[0,2])
                percentual.loc[row,cols[2]] = df_aux.loc[row,cols[2]] 
                percentual.loc[row,cols[1]] = pais
                percentual.loc[row,cols[0]] = np.round(100*(numerador/denominador),1)
            df_aux = percentual    
            
    df_aux = df_aux.sort_values(sort_by_col, ascending = sort_by_col_order)
    
    if top_mode != 'all':
        df_aux = df_aux.iloc[0:(top_mode-1), :]
    
    
    # define a escala do gráfico, coloca o ponto de máximo do eixo em 20% acima do valor máximo a ser exibido
    graph_range = df_aux[y_axis].max()*1.2
    # gráfico
    if color_attribute != False:
        
        fig = px.bar(df_aux, 
                     x=x_axis, 
                     y=y_axis, 
                     range_y= [0,graph_range], 
                     labels={ x_axis: x_label, y_axis: y_label},
                     title=graph_label,
                     width=int(max_width),
                     height=int(max_height),
                     text_auto=True, 
                     color = color_attribute)
    else:
        fig = px.bar(df_aux, 
                     x=x_axis, 
                     y=y_axis, 
                     range_y= [0,graph_range], 
                     labels={ x_axis: x_label, y_axis: y_label},
                     title=graph_label,
                     width=int(max_width),
                     height=int(max_height),
                     text_auto=True)        

    # configura o título do gráfico
    # title_x --> alinhamento central;  
    # Se < 0.5 --> desloca à esquerda
    # Se > 0.5 --> desloca à direita
    fig.update_layout(
            title_font = {"size": 20},
            font_family="Arial",
            font_color="Black",
            title_font_family="Arial",
            title_font_color="black",
            title_x=0.25)
    # configura os títulos dos eixos
    fig.update_xaxes(
            tickangle = 45,
            title_text = x_label,
            title_font = {"size": 14},
            tickfont_size=12)

    fig.update_yaxes(
            title_text = y_label,
            title_font = {"size": 14},
            tickfont_size=12)    
    return fig



def classificacao(filtro, df1, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, col_calc):
    if operacao == 'nunique':
        df_aux = df1.loc[filtro,cols].groupby(group_by_col).nunique().sort_values(sort_by_col, ascending = sort_by_col_order).reset_index()
    elif operacao == 'count':
        df_aux = df1.loc[filtro, cols].groupby(group_by_col).count().sort_values(sort_by_col, ascending = sort_by_col_order).reset_index()
    elif operacao == 'sum':
        df_aux = df1.loc[filtro, cols].groupby(group_by_col).sum().sort_values(sort_by_col, ascending = sort_by_col_order).reset_index()    
    elif operacao == 'mean':
        df_aux = df1.loc[filtro, cols].groupby(group_by_col).mean(col_calc).round(decimals=2).sort_values(sort_by_col, ascending = sort_by_col_order).reset_index()       
    
    return df_aux


def newLegend(fig, newNames):
    for item in newNames:
        for i, elem in enumerate(fig.data[0].labels):
            if elem == item:
                fig.data[0].labels[i] = newNames[item]
    return(fig)


def pie_chart(filtro, df1, operacao, cols, group_by_col, sort_by_col, sort_by_col_order, col_calc,
                   x_axis, y_axis, x_label, y_label, graph_label, max_width, max_height, top_mode, pie_hole):

    df_aux = df1.loc[filtro, cols].groupby(group_by_col).mean(col_calc).round().reset_index()

    fig = px.pie(df_aux, values= x_axis, names= y_axis,
                 title= graph_label,
                 width = max_width,
                 height = max_height,
                 hole = pie_hole)
    fig = newLegend(fig = fig, newNames = {True: x_label,
                                           False : y_label})
    fig.update_traces(textposition='inside', textinfo='percent+value')
    
    return fig
            
    
    
    
def grafico_country_map(df1, cols, group_by_col, latitude, longitude):
    
    start_location = [0,0]#[df1.loc[:, latitude].median(), df1.loc[:,longitude].median()]
    mapa = folium.Map(location= start_location, min_zoom = 0, zoom_start= 1.8, control_scale=False)
    marker_cluster = MarkerCluster().add_to(mapa)
    #adiciona os pontos geográficos ao mapa
    for index, location_info in df1.iterrows():
        color_marker = location_info['Rating_color']
        if (location_info[longitude]!=0) & (location_info[latitude]!=0):
            popup_text = 'Restaurante: ' + str(location_info['Restaurant Name']) + '\n\n Valor médio para duas pessoas: ' + str(location_info['AVG_cost_4_2'])
            folium.Marker( [location_info[latitude], location_info[longitude]],
                            popup=popup_text,
                            tooltip=location_info['Aggregate rating'], 
                            icon=folium.Icon(color=color_marker, icon='')
                         ).add_to(marker_cluster)
    
    return mapa    




embed_component = {'linkedin':"""<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
                  <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL" data-vanity="" data-version="v1"><a class="badge-base__link LI-simple-link" href="https://br.linkedin.com/in/farzinbassiri?trk=profile-badge">Farzin Bassiri</a></div>"""}
