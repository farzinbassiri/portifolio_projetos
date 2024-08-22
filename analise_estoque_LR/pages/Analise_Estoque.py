# Biblioteca de funções
from funcoes import *

# biblioteca de importação de dados e arquivos
import csv
import os

# Biblioteca para tratamento de dados
from   scipy.signal import argrelextrema # identifica os pontos de minimo e máximo
import holidays                          # identifica os dias úteis
import pandas   as pd
import numpy    as np
import datetime as dt


# Bibliotecas para visualização dos dados
from matplotlib import pyplot as plt
from termcolor import colored

# Bibliotecas para tratamento estatístico
import statsmodels.api as sm
import scipy.stats     as stats
from   scipy.stats import shapiro 

# biblioteca de aprendizado de máquina
from sklearn.linear_model        import LinearRegression
from sklearn                     import metrics         as mt
from sklearn                     import model_selection as ms
from statsmodels.tsa.seasonal    import seasonal_decompose

# Bibliotecas streamlit
#import linecache as lc
import streamlit as st
import streamlit.components.v1 as components

# importa biblioteca para logo da página
from PIL import Image


#from dateutil.relativedelta import relativedelta


# configura página
st.set_page_config(layout="wide")
# le os dados do giro de estoque

# Arquivos de entrada
try: #caminho para Streamlit
    df_raw = pd.read_csv('analise_estoque_LR/dataset/Giro de Estoque.csv')
except: #caminho para uso local
    df_raw = pd.read_csv('..\\dataset\\Giro de Estoque.csv')

# converte data em index do df e corta dados anteriores à 01/jul/2010
df_raw['Data']= pd.to_datetime(df_raw['Data'])
filtro = df_raw.Data>= '2010-07-01'
df_raw = df_raw.loc[filtro,:]
df_raw.index = pd.to_datetime(df_raw.Data, format="%Y-%m-%d")
df_raw.sort_index(inplace=True)
df_raw.drop("Data", inplace=True, axis=1)



#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
#                                Monta barra lateral
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------	
st.sidebar.markdown('#### - Regressão Linear para análise de estoque.')
st.sidebar.markdown('#### - Decomposição de Séries Temporais para análise de tendência de consumo.')


#Carrega o logo 
try: #caminho para Streamlit
    image = Image.open('Amostragem_de_Dados/logo.png')
except: #caminho para uso local
    image = Image.open('logo.png')
st.sidebar.image(image, width=270)

st.sidebar.markdown("""___""")

# permite que o usuário escolha o intervalo de datas para ver como os parâmetros influenciam o resultado
# Lead time --> prazo de entrega do fornecedor
# Autonomia de estoque define o tamanho do estoque estratégico, ou seja, se o material atrasar ou não for comprado e a demanda se manter constante, quanto tempo dura o estoque.
st.sidebar.markdown('### Configuração dos parâmetros para o modelo:')
st.sidebar.markdown('##### Escolha o *Lead Time*(LT) do fornecedor (dias corridos).')
lead_time = st.sidebar.slider('', min_value=1, value=10 ,max_value=30)

st.sidebar.markdown('##### Escolha a *Autonomia do Estoque* aproximada (dias úteis).')
tempo_seguranca = st.sidebar.slider('', min_value=1, value=22 ,max_value=120)


st.sidebar.markdown('##### Escolha o intervalo para a análise.')

# define p formato das datas a serem exibidas
format = 'DD-MM-YYYY'  # format output

# monta os parâmetros sugeridos para a análise
data_inicial = df_raw.index.min()
data_final = df_raw.index.max()

# Define como data inical de análise o ponto 2023-10-10. Essa data é arbitrária e foi escolhida pois apresentou o menor MAPE geral sem deixar de ter amostas suficientes para as análises
# ponto de corte dos dados para COVID 19 foi definida baseada nos dados de interrupção das operações notariais
auto_mode  = st.sidebar.checkbox('##### Deseja utilizar os datas pré-definidas?', value=True)
covid_mode = st.sidebar.checkbox('##### Deseja utilizar os dados pós-COVID?', value=False)
if auto_mode == True:
    data_auto = dt.datetime(2023,6,21)
else:
    data_auto = dt.datetime(data_inicial.year, data_inicial.month, data_inicial.day)

if covid_mode:
    data_auto = dt.datetime(2020, 4, 6)

#slider_intervalo = list(st.sidebar.date_input('Escolha o intervalo', min_value=data_inicial, value=[data_auto, data_final] ,max_value=data_final, format=format))
# captura as datas desejadas
data_inicial = st.sidebar.date_input('Escolha ou digite a data de início:', value=data_auto, format=format)
data_final   = st.sidebar.date_input('Escolha ou digite a data de fim:', value=data_final, format=format)

# na versão inicial deste projeto, um slider duplo foi utilizado para determinar as datas de interesse. 
# Nesta versão foi utilizado o formato de calendário, para manter o legado de formato foi feito por lista, 
# assim não precisa mudar o código dos demais módulos.
slider_intervalo = []
slider_intervalo = [dt.datetime(data_inicial.year, data_inicial.month, data_inicial.day, 0, 0, 0), 
                    dt.datetime(data_final.year, data_final.month, data_final.day, 0, 0, 0)]

# verifica se a data inicial é menor que a data final. Se não for, inverte o intervalo e notifica
if slider_intervalo[0] > slider_intervalo[1]:
    tmp = slider_intervalo[0]
    slider_intervalo[0] = slider_intervalo[1]
    slider_intervalo[1] = tmp
    del tmp
    st.warning('Atenção: Data de início é maior que data de fim. Valores foram invertidos automaticamente.', icon="⚠️")
    
# verifica se o interfalo escolhido está fora do range dos dados, corrige e alerta se estiver fora
if slider_intervalo[0] < df_raw.index.min():
    st.write(slider_intervalo[0])
    slider_intervalo[0] = df_raw.index.min()    
    st.warning('Atenção: Data selecionada é inválida.', icon="⚠️")
    
if slider_intervalo[1] > df_raw.index.max():
    st.write(slider_intervalo[1])
    slider_intervalo[1] = df_raw.index.max()   
    st.warning('Atenção: Data selecionada é inválida.', icon="⚠️")

# slider desativado. foi substituido pelo calendario...
# data_inicial = dt.datetime(data_inicial.year, data_inicial.month, data_inicial.day)
# data_final = dt.datetime(data_final.year, data_final.month, data_final.day)

#slider_intervalo = st.sidebar.slider('Escolha as datas', min_value=data_inicial, value=[data_auto, data_final] ,max_value=data_final, format=format)

# monta uma lista ordenada dos produtos para escolha. Essa lista será utilizada também mais adiante no código
lista_produtos = sorted(list(df_raw.Produto.unique()))
produto = st.sidebar.selectbox('Escolha o produto', lista_produtos, index=0)

# limita os dados conforme os parâmetros escolhidos: datas e produto.
filtro = (df_raw.index >= slider_intervalo[0]) & (df_raw.index <= slider_intervalo[1]) & (df_raw.Produto == produto)
df = df_raw.loc[filtro,['Produto','Estoque']].copy()


#criando abas
tab1, tab2, tab3, tab4 = st.tabs(['Estudo Estoque', 'Análise Demanda (Todos os Dados)', 'Analise Demanda (Por Intervalo)', 'Espalhamento Coef'])



#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
#                                Visão Geral do Algoritmo
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------	

# os dados passam por um módulo que ideintifica os pontos de mínimo e máximo local da curva dente de serra.
# estoque_min e estoque_max guardam esses dados.
# Os dados do estoque são decompostos em segmentos de reta descendentes (curva descendente pois o estoque está
# sendo consumido). Cada segmento de reta servirá de dado para um modelo de regressão linear
# os diversos modelos de regressão linear são validados ou rejeitados através da análise da normalidade dos
# resídulos da regressão via teste de Shapiro-Wilk. 
# o MAPE de cada modelo também é calculado, mas não influencia a decisão de validação/rejeição do modelo.
# Uma tabela com os resultados é gerada (df_result) contendo:
#    - MAPE do modelo;
#    - Coeficiente Angular (Coef);
#    - Coeficiente linear(Intercept);
#    - P-valor do teste de normalidade (necessário ser > 0.05 para aprovação do modelo);
#    - Normalidade do Resíduo (ok/nok).
#    - a tabela de resultado foi inicialmente formatada para exibição, sendo:
#        - marcação em verde: modelos validados
#        - marcação em vermelho: modelos rejeitados
#    - posteriormente a exibição foi removida e a formação retirada, podendo ser recolocada posteriormente
# São calculados os dias úteis de cada período e é feita a conversão do consumo médio (seria o Coef da LR),
# A mediana dos diversos coeficientes angulares é usada para fazer a projeção do estoque para os dados mais 
# recentes, identificando o ponto de zeramento do estoque.
# Com essas informações e considerando adicionalmente o lead time de fornecimento, é feita a estimativa 
# da autonomia do estoque e determinação do ponto de compra mais otimizado.
# os gráficos são então montados.

# Uma vez em posse de um conjunto de coeficientes angulares (indicativos do consumo médio entre duas compras),
# é possivel fazer um estudo rápido de tendencia ao transformar o coeficiente angular em uma série temporal.
# Ao fazer a decomposição da série temporal verifica-se o comportamento do consumo e é possivel fazer uma 
# readequação dos parâmetros considerando a tendencia do consumo, por exemplo:
#     - Se o produto_1 indicar tendencia de queda do consumo, se os parâmetros de compra forem ajustados para 
#       a sugestão do algoritmo e for mantida permanentemente desta forma, chegará um momento que esses 
#       parâmetros de compra não serão mais adequados aos propósitos da organização, levando a um estoque 
#       demasiadamente elevado, uma vez que o consumo está decrescente.
#     - Por outro lado, caso o produtomostre uma tendência de aumento de demanda, será necessário uma alterção
#       dos parâmetros de compra para evitar uma queda na autonomia do estoque.


#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
#                                Mostrando os resultados
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------	


with tab1:    
    with st.container(border=True):
        # monta o conjunto de LR para o período de tempo escolhido.
        # o módulo projecao_estq chama as rotinas que escrevem o resultado e monta os gráficos.
        # caso os dados não sejam suficientes para a LR, retorna um erro ('LR: erro'), caso contrário, retorna 0
        erro, estoque_min, estoque_max, df_result = projecao_estq(produto, df, lead_time, tempo_seguranca)
        if erro != 0:
            st.warning('Atenção: Dados insuficientes para realização da análise do estoque. Escolha um intervalo de tempo maior.', icon="⚠️")
            exit()            
        try:
            df_result = df_result.data   
        except:
            pass

with tab2:    
    with st.container(border=True):
        for prod in lista_produtos:
            st.write(prod)
            df_giro = pd.DataFrame()
            filtro = df_raw.Produto == prod
            estq_min, estq_max = min_max(df_raw.loc[filtro,['Estoque']])

            if estq_max.index[0] > estq_min.index[0]:
                df_giro['Data_max'] = estq_max.iloc[1:,0].index
                df_giro['Data_min'] = estq_min.index[:-1].index
                
            else:
                df_giro['Data_max'] = estq_max.index
                df_giro['Data_min'] = estq_min.index

            for linha in df_giro.index:
                filtro = (df_raw.index >= df_giro.iloc[linha,0]) & (df_raw.index <= df_giro.iloc[linha,1]) & (df_raw.Produto == prod)
                
                df_giro.loc[linha,'Coef'] = -(df_raw.loc[filtro,'Consumo'].sum())/df_raw.loc[filtro,'Consumo'].count()
            
            df_giro.index = pd.to_datetime(df_giro.Data_max, format="%Y-%m-%d")
            df_giro.sort_index(inplace=True)
            df_giro.drop(['Data_max', 'Data_min'], inplace=True, axis=1)   
    
            #faz a decomposição da sazionaalidade
            decomposicao_sazional = seasonal_decompose(df_giro['Coef'], period=4)
            trend = decomposicao_sazional.trend
            seasonal = decomposicao_sazional.seasonal
            residual = decomposicao_sazional.resid
            observed = decomposicao_sazional.observed
    
            # detemrina ponto de corte COVID e marcação de ultimos 24 meses
            filtro = (trend.index > '2020-02-16') & (trend.index < '2020-02-19') 
            corte = trend.loc[filtro]
            # determina ponto médio do trend para últimos 24 meses
            filtro = (trend.index > trend.index.max() - pd.DateOffset(730))
            trend_24_mean = trend.loc[filtro].mean()
            abs(trend_24_mean)
            
            # monta gráfico
            fig, (ax, bx) = plt.subplots(1,2, figsize=(12,3))
            ax.plot(trend, '-o' , label='Tendência Consumo')
            ax.set_title('Tendência: ' + prod)
            ax.vlines(corte.index, trend.min(), trend.max(), color='black', linestyle='dashed', label='COVID19')
            ax.hlines(trend_24_mean, trend.index.max() - pd.DateOffset(730), trend.index.max(), color='maroon',  
                      linestyle='dashed', label='Media 24 meses', linewidth=1.5)
            ax.grid(color='b', linestyle='-', linewidth=0.1)  
            ax.legend(fontsize=9)
            ax.set_ylabel('Consumo médio', fontsize=9)
            ax.tick_params(axis='x', rotation=35)
            # zoom nos últimos 24 meses
            filtro = (trend.index > '2022-01-01')
            
            bx.plot(trend.loc[filtro], '-o' , label='Tendência Consumo')
            bx.set_title('Zoom - Tendência: ' + prod)
            bx.hlines(trend_24_mean, trend.index.max() - pd.DateOffset(730), trend.index.max(), color='maroon', 
                      linestyle='dashed', label='Media 24 meses', linewidth=1.5)
            bx.grid(color='b', linestyle='-', linewidth=0.1)  
            bx.legend(fontsize=9)
            bx.set_ylabel('Consumo médio', fontsize=9)
            bx.tick_params(axis='x', rotation=35)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)


with tab3:    
    with st.container(border=True):
        for prod in lista_produtos:
            df_giro = pd.DataFrame()
            df_giro['Data_max'] = estoque_max.index
            df_giro['Data_min'] = estoque_min.index
            
            for linha in df_giro.index:
                filtro = (df_raw.index >= df_giro.iloc[linha,0]) & (df_raw.index <= df_giro.iloc[linha,1]) & (df_raw.Produto == prod)
                df_giro.loc[linha,'Coef'] = -(df_raw.loc[filtro,'Consumo'].sum())/df_raw.loc[filtro,'Consumo'].count()
            
            df_giro.index = pd.to_datetime(df_giro.Data_max, format="%Y-%m-%d")
            df_giro.sort_index(inplace=True)
            df_giro.drop(['Data_max', 'Data_min'], inplace=True, axis=1)        
    
            periodo = 4
            # checa se tem o número de períodos mínimo necessário
            if len(df_giro) < 2*periodo:
                st.warning('Atenção: Intervalo selecionado tem poucos dados para análise de demanda.', icon="⚠️")
                exit()
            
            #faz a decomposição da sazionaalidade
            decomposicao_sazional = seasonal_decompose(df_giro['Coef'], period=periodo)
            trend = decomposicao_sazional.trend
            seasonal = decomposicao_sazional.seasonal
            residual = decomposicao_sazional.resid
            observed = decomposicao_sazional.observed

            # detemrina ponto de corte COVID e marcação de ultimos 24 meses
            filtro = (trend.index > '2020-02-16') & (trend.index < '2020-02-19') 
            corte = trend.loc[filtro]
            # determina ponto médio do trend para últimos 24 meses
            filtro = (trend.index > trend.index.max() - pd.DateOffset(730))
            trend_24_mean = trend.loc[filtro].mean()
            abs(trend_24_mean)
            
            # monta gráfico
            fig, ax = plt.subplots(1,1, figsize=(8,4))
            ax.plot(trend, '-o' , label='Tendência Consumo')
            ax.set_title('Tendência: ' + prod)


            filtro_trend = trend.isna()==False
            
            
            y_min = trend.loc[filtro_trend].index.max() - pd.DateOffset(730)
            text_mean = 'Media 24 meses'
            if y_min < trend.loc[filtro_trend].index.min():
                y_min = trend.loc[filtro_trend].index.min()
                text_mean = 'Media período'

            y_max =  trend.loc[filtro_trend].index.max()

            ax.vlines(corte.index, trend.min(), trend.max(), color='black', linestyle='dashed', label='COVID19')
            ax.hlines(trend_24_mean, y_min, y_max, color='maroon', 
                      linestyle='dashed', label=text_mean, linewidth=1.5)
            ax.grid(color='b', linestyle='-', linewidth=0.1)  
            ax.legend(fontsize=9)
            ax.set_ylabel('Consumo médio', fontsize=9)
            ax.tick_params(axis='x', rotation=35)

            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)


with tab4:
    with st.container(border=True):
        col1, col2 = st.columns([1,1])
        # monta dois bloxplot para verificação do espalhamento do COEF encontrado.
        # Como o algoritmo exclui segmentos de dados cuja LR não foi aceitável, um dos gráficos é 
        # para os dados validados e utilizados e o outro para os dados eliminados.
        with col1:
            with st.container():
                # seleciona os resultados validados
                filtro = df_result.Residuo=='OK'
                
                fig, ax = plt.subplots(1, 1, figsize=(2, 3))
                ax.boxplot(df_result.loc[filtro, 'Coef'])
                ax.grid(color='gray', linestyle='-', linewidth=0.1) 
                ax.set_ylabel('Coef', fontsize= 11)
                ax.set_xlabel(produto, fontsize= 9)
                ax.tick_params(axis='x', labelsize=10)
                ax.tick_params(axis='y', labelsize=9)
                ax.set_title('Variação do Coeficiente Angular\n Apenas trechos aprovados')
                
                plt.tight_layout()		
                st.pyplot(fig, use_container_width=True)
                
            with st.container():
                filtro = df_result.Residuo=='OK'
                st.dataframe(df_result.loc[filtro, :], use_container_width=True, hide_index=True)
                
        with col2:
            with st.container():
                filtro = (df_result.Residuo=='NOK') #| (df_result.Residuo=='OK')
                
                fig, ax = plt.subplots(1, 1, figsize=(2, 3))
                # cria o primeiro gráfico mostrando os dados do dataset, onde cada cor é uma das marchas
                ax.boxplot(df_result.loc[filtro, 'Coef'])
                #ax.boxplot(df_result.Intercept)
                #configura o grid dos gráficos        
                ax.grid(color='gray', linestyle='-', linewidth=0.1) 
                ax.set_ylabel('Coef', fontsize= 11)
                ax.set_xlabel(produto, fontsize= 9)
                ax.tick_params(axis='x', labelsize=10)
                ax.tick_params(axis='y', labelsize=9)
                ax.set_title('Variação do Coeficiente Angular\n Trechos reprovados')
                
                plt.tight_layout()		
                st.pyplot(fig, use_container_width=True)
                
            with st.container():
                filtro = df_result.Residuo=='NOK'
                st.dataframe(df_result.loc[filtro, :], use_container_width=True, hide_index=True)
