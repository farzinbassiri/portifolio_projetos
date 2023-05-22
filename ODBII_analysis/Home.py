### Dados de funcionamento Jipe Tarja Preta - ODBII
# carregar protótipo via comando no terminal: streamlit run "torque - dashboard.py"
#--------------------------------------------------------------------------------------------------------------
# Documentação inicial: 
#    - Dados obtidos via ODBII e app Torque Pro durante o uso do app.
#    - Arquivo exportado para formato CSV e importado para análise de conteúdo.
#    - Foram geradas dois dataframes - df1 e df_GPS:
#        - df_GPS: eventualmente a comunicação do APP e o módulo de GPS era interrompido pelo
#                sistema operacional. Nesses casos algumas columas com dados vinculados ao GPS ficaram vazios;
#                 neste dataframe, as linhas com dados de GPS faltantes foram excluidas. Como na ocasião 
#                repesentavam cerca de 40% dos dados, então os dados integrais firam mantidos em outro dataframe
#        - df1: dataframe que contém os dados integrais, mesmo faltando dados do GPS.
#    - O dataframe df_GPS é exportado para um arquivo chamado trackLog_DW.xlsx para ser visualizado via Excel.
#
#    - sugestões de melhoria:
#       1. configurar Torque Pro para colocar o arquivo CSV na nuvem e fazer atualização automática
#       2. Melhorar o registro do log 
#--------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
#                                PREPARAÇÃO DOS DADOS
# Os dados foram previamente tratados e colocados em um arquivo csv para serem carregados e analizados
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------

# Definindo as bibliotecas a serem importadas:

# Bibliotecas de manipulação de arquivos
#

# bibliotecas necessárias de manipulação de dados
import pandas as pd
from haversine import haversine
import numpy as np

# Bibliotecas para construção do dashboard
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
import folium

# Bibliotecas de manipulação de tempo
from datetime import datetime, timedelta

# bBiblioteca de função matemática
import math
# Arquivos de entrada e saída

#define arquivo de origem dos dados e converte a coluna de data para o formato adequado
df_GPS = pd.read_csv('trackLog_DW.csv')
df_GPS['Device Time'] = pd.to_datetime(df_GPS['Device Time'])

df_analise1 = pd.read_csv('trackLog_DW - Consumo.csv')
df_analise1['Data inicial'] = pd.to_datetime(df_analise1['Data inicial'])
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
#                                ANÁLISE INICIAL DOS DADOS
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------



# 1.Gerar um gráfico dinâmico com informaçãoes sobre o funcionamento do carro, tais como: Quantos trechos diferentes de coleta de dados foram realizados e qual o tempo médio de condução, consumo, distância percorrida, etc..


# a. Qual o consumo médio?
# fazer média regional para tentar normalizar os dados:



# 4. É possivel determinar se houve troca de combustível?


# 5. Existe algum padrão no consumo de combustível?
    # a. região geográfica;
    # b. modo de condução; etc.

    
    
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
#                                Barra Lateral
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------

st.header('OBDII - Torque Pro - Análise dados veiculares')

#Carrega o logo 
image = Image.open('logo_ODBII.jpg')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Análise de Dados Veiculares - Via ODBII')
st.sidebar.markdown('## Dados de funcionamento Pajero TR4 Flex 2009')
st.sidebar.markdown("""___""")
st.sidebar.markdown('## Selecione um intevalo de datas para análise')


# cria o slider para definição da data de interesse do usuário.
# essa data fica restrita ao intervalo de datas com dados disponíveis
# seleção da data de interesse pelo usuário
data_inicial= df_GPS['Device Time'].min()
data_final= df_GPS['Device Time'].max()

date_slider = st.sidebar.slider(
     'Defina o intervalo com as datas desejadas:',
     datetime(data_inicial.year, data_inicial.month, data_inicial.day),
     datetime(data_final.year, data_final.month, data_final.day),
     value = (datetime(data_inicial.year, data_inicial.month, data_inicial.day), 
              datetime(data_final.year, data_final.month, data_final.day)),
     format = 'DD-MM-YYYY')
st.sidebar.markdown("""___""")

# cria o slider com o parâmetro de resample das amostras
#obs: os dados podem não ser normais, neste caso, fazer pequenos agrupamentos de dados e tirar a média deles torna os dados normais. 
st.sidebar.markdown('## Resample para normalização dos dados')
resample_slider = st.sidebar.slider(
     'Defina a quantidade de minutos a serem concatenados em uma amostra:',
     1,
     20,
     value = 5)
st.sidebar.markdown('1 --> não faz resample para normalização dos dados')
st.sidebar.markdown("""___""")

# usa a Regra de Sturges para sugerir o número de classes no histograma
nbins_inicial = int(1 + 3.322 * math.log(len(df_GPS)))
nbins_auto = st.sidebar.checkbox('Nro de Classes automático?', value=True)
if nbins_auto:
    status = True
else:
    status = False
nbins_slider = st.sidebar.slider(
     'Defina o número de classes do histograma:',
     2,
     100,
     value = nbins_inicial,
     disabled = status)


st.sidebar.markdown("""___""")
st.sidebar.markdown('###### Powered by Farzin Bassiri')


# aplica os filtros do sidebar na tabela de dados
# filtro de data
linhas_selecionadas = (df_GPS['Device Time'] > date_slider[0]) & (df_GPS['Device Time'] < date_slider[1])  
df_param = df_GPS.loc[linhas_selecionadas,:]

linhas_selecionadas2 = (df_analise1['Data inicial'] > date_slider[0]) & (df_analise1['Data inicial'] < date_slider[1])  
df_param2 = df_analise1.loc[linhas_selecionadas2,:]

#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
#                                ANÁLISE INICIAL DOS DADOS
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------

# fazer resampling com média dos agrupamentos para normalizar os dados:

# colunas = ['Device Time', 'km/l(Instant)', 'Fuel flow(l/h)', 'Speed (OBD)(km/h)', 'Engine RPM']
# # qdo a velocidade é nula, então o fluxo de combustivel está no mínimo não nulo.Limitando o RPM do motor temos maior probabilidade de coletrar apenas os dados da marcha lenta
# linhas_selecionadas = (df1['Fuel flow(l/h)'] != 0) & (df1['km/l(Instant)'] != 0) & (df1['Speed (OBD)(km/h)'] !=0) 
# consumo = df1.loc[linhas_selecionadas, colunas]




       
            



#criando abas
tab1, tab2, tab3 = st.tabs(['Visão Geral', 'Visão "Teste"', '-'])

# separa os códigos para cada aba
# todo código que estiber em 'with tab1 vai aparecer naquela aba
with tab1:
      
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('### Indicadores Gerais')

            data_inicial= df_GPS['Device Time'].min()
            data_final= df_GPS['Device Time'].max()
            tempo_total = int(np.round(df_analise1.loc[:,'Tempo[h]'].sum()))
            dias = int(np.round((data_final - data_inicial).total_seconds()/(3600*24)))
            texto = ("- Quantidade de horas de funcionamento: " + str(tempo_total) + " horas ao longo de " +
                     str(dias) + " dias")
            st.info(texto)
            
            distancia_total = int(df_analise1.loc[:,'Distancia[km]'].sum())
            texto = "- Distância percorrida: " + str(distancia_total) + "km"
            st.info(texto)

            combustivel_total =df_analise1.loc[:,'Combustivel[l]'].sum()
            texto = "- Quantidade de combustível consumido: " + str( int(np.round(combustivel_total))) + "l"
            st.info(texto)
            
            consumo_medio = (np.round(distancia_total/combustivel_total, 2))
            texto = "- Consumo médio: " + str(consumo_medio) + "km/l"
            st.info(texto)    

            st.markdown("""___""")            

        with col2:
            st.markdown('### Indicadores por trecho')      
            tempo_medio = (np.round(df_analise1.loc[:,'Tempo[h]'].mean()*60,1))
            texto = ("- Tempo médio por trecho percorrido: " + str(tempo_medio) + " minutos")
            st.info(texto)
            
            distancia_trecho = int(df_analise1.loc[:,'Distancia[km]'].mean())
            texto = "- Distância média percorrida em cada trecho: " + str(distancia_trecho) + "km"
            st.info(texto)
            
            combustivel_medio =df_analise1.loc[:,'Combustivel[l]'].mean()
            texto = "- Quantidade média de combustível consumido por trecho: " + str( np.round(combustivel_medio,2)) + "l"
            st.info(texto)            
            
            st.markdown("""___""")

            
    with st.container():
            st.markdown('### Indicadores Diários')

            data_inicial= df_GPS['Device Time'].min()
            data_final= df_GPS['Device Time'].max()
            tempo_total = int(np.round(df_analise1.loc[:,'Tempo[h]'].sum()))
            dias = int(np.round((data_final - data_inicial).total_seconds()/(3600*24)))
            texto = ("- Quantidade média de horas de funcionamento por dia: " + str(np.round(tempo_total/dias,2)))
            st.info(texto)
            
            distancia_dia = df_analise1.loc[:,'Distancia[km]'].sum()/dias
            texto = "- Distância média percorrida por dia: " + str(np.round(distancia_dia,1)) + "km"
            st.info(texto)            
            
            combustivel_dia =df_analise1.loc[:,'Combustivel[l]'].sum()/dias
            texto = "- Quantidade média de combustível consumido por dia: " + str( int(np.round(combustivel_dia))) + "l"
            st.info(texto)
            
            consumo_medio = (np.round(distancia_dia/combustivel_dia, 2))
            texto = "- Consumo médio: " + str(consumo_medio) + "km/l"
            st.info(texto)    
            st.markdown("""___""")   
            
            
    with st.container():
        st.markdown('## Indicadores Parametrizados')    
        data_inicial= df_param2['Data inicial'].min()
        data_final= df_param2['Data inicial'].max()
        tempo_total = int(np.round(df_param2.loc[:,'Tempo[h]'].sum()))
        dias = int(np.round((data_final - data_inicial).total_seconds()/(3600*24))+1)
        texto = ("- Quantidade de horas de funcionamento: " + str(tempo_total) + " horas ao longo de " +
                 str(dias) + " dias")
        st.info(texto)

        distancia_total = int(df_param2.loc[:,'Distancia[km]'].sum())
        texto = "- Distância percorrida: " + str(distancia_total) + "km"
        st.info(texto)

        combustivel_total =df_param2.loc[:,'Combustivel[l]'].sum()
        texto = "- Quantidade de combustível consumido: " + str( int(np.round(combustivel_total))) + "l"
        st.info(texto)

        consumo_medio = (np.round(distancia_total/combustivel_total, 1))
        texto = "- Consumo médio do intervalo: " + str(consumo_medio) + "km/l"
        st.info(texto)            
        st.markdown("""___""")

        
with tab2:
            with st.container():
                colunas = ['Device Time', 'km/l(Instant)', 'Fuel flow(l/h)']
                linhas_selecionadas = (df_param['km/l(Instant)'] != 0) & (df_param['km/l(Instant)'] != 181.2480011)
                consumo = df_param.loc[linhas_selecionadas, colunas]
                consumo_medio = df_param.loc[linhas_selecionadas, 'km/l(Instant)'].mean()
                tempo_inicial= consumo['Device Time'].min()
                tempo_final= consumo['Device Time'].max()

                if resample_slider !=1:
                    resample_rate = str(resample_slider) + 'min'
                    teste = consumo.resample(rule= resample_rate, on = 'Device Time', origin= 'start').mean()
                else:
                    teste = consumo
                texto = 'Quantidade de pontos na amostra: ' + str(len(teste))
                st.markdown(texto)

                linhas_validas = teste['km/l(Instant)'] != 'NaN'
                #transfere para o dataframe apenas as linhas que contém dados
                teste = teste.loc[linhas_validas, :]

                #nbins_slider
                if nbins_auto:
                    nbins_slider = int(1 + 3.322 * math.log(len(teste)))
                fig = px.histogram(teste, 
                                   x='Fuel flow(l/h)', 
                                   nbins=nbins_slider,
                                   title='Fuel Flow [l/h]', 
                                   color_discrete_sequence=['blue'] )
                fig.update_layout(bargap=0.2)
                st.plotly_chart(fig, use_conteiner_width = True)  

with tab3:
    with st.container():
        st.markdown('# Indicadores Gerais')

        # monta o gráfico
        fig = px.bar(df_param, x= 'Device Time', y='Fuel flow(l/h)', width=700, height=400)

        # configura os títulos dos eixos
        fig.update_xaxes(
                tickangle = 0,
                title_text = "Dia da amostra",
                title_font = {"size": 16})

        fig.update_yaxes(
                title_text = 'Fuel flow(l/h)',
                title_font = {"size": 14})

        # configura o título do gráfico
            # title_x --> alinhamento central;  
            # Se < 0.5 --> desloca à esquerda
            # Se > 0.5 --> desloca à direita
        fig.update_layout(title_text='Fluxo de combustível', title_x=0.5)
        #fig.update_xaxes(type='category')
        #st.plotly_chart(fig, use_conteiner_width = True)


#         fig2 = px.bar(df_param, x= 'Device Time', y='Engine RPM', width=700, height=400)
#         # configura os títulos dos eixos
#         fig2.update_xaxes(
#                 tickangle = 0,
#                 title_text = "Dia da amostra",
#                 title_font = {"size": 16})

#         fig2.update_yaxes(
#                 title_text = 'Engine RPM',
#                 title_font = {"size": 14})  
        
#         fig2.update_layout(title_text='RMP do motor', title_x=0.5)
        
        #st.plotly_chart(fig2, use_conteiner_width = True)     
