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
from sklearn.linear_model import LinearRegression
from sklearn              import metrics         as mt
from sklearn              import model_selection as ms

# Bibliotecas streamlit
#import linecache as lc
import streamlit as st
import streamlit.components.v1 as components

# importa biblioteca para logo da página
from PIL import Image


from dateutil.relativedelta import relativedelta


# le os dados do giro de estoque

# Arquivos de entrada
try: #caminho para Streamlit
    df_raw = pd.read_csv('LR_previsao_estoque/Dataset/Giro de Estoque.csv')
except: #caminho para uso local
    df_raw = pd.read_csv('Dataset\\Giro de Estoque.csv')

df_raw['Data']= pd.to_datetime(df_raw['Data'])



# converte a data em index
df_raw.index = pd.to_datetime(df_raw.Data, format="%Y-%m-%d")
df_raw.sort_index(inplace=True)
df_raw.drop("Data", inplace=True, axis=1)

#df = df_raw.copy()


#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
#                                Barra Lateral
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
# coloca o link do LinkedIn na barra lateral
embed_component = {'linkedin':"""<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
                  <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL" data-vanity="farzinbassiri" data-version="v1"><a class="badge-base__link LI-simple-link" href="https://br.linkedin.com/in/farzinbassiri?trk=profile-badge">"""}


st.header('Projeção do Nível de Estoque')
# st.subheader('...')
# st.subheader('...')

st.markdown("""___""")

st.sidebar.markdown('#### - Regressão Linear para análise de estoque.')
st.sidebar.markdown('#### - Decomposição de Séries Temporais para análise de tendência de consumo.')


#Carrega o logo 
try: #caminho para Streamlit
    image = Image.open('Amostragem_de_Dados/logo.png')
except: #caminho para uso local
    image = Image.open('logo.png')
st.sidebar.image(image, width=270)

st.sidebar.markdown("""___""")


#coloca o objeto LinkedIn na barra lateral
with st.sidebar:
    components.html(embed_component['linkedin'], height = 310)

	
st.sidebar.markdown("""___""")
st.sidebar.markdown('###### Powered by Farzin Bassiri')


#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
#                                Janela Principal
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------

 

st.markdown('### I. Introdução:') 

st.markdown(""" 

- Os dados utilizados nesse projeto são reais e foram anonimizados a pedido do titular dos dados; 

- A solução encontrada neste projeto está em fase de piloto de implantação.  

""") 

  

st.markdown('### II. Motivação para o projeto:') 

  

st.markdown("""A empresa _Acco-Chambers Ltda._ fez uma análise de risco operacional e detectou que um conjunto de materiais era crítico para sua operação, sendo necessário o aprimoramento do planejamento de compras e gestão do estoque para evitar: 

  

- **Falta de Materiais:** 

    - Interrupção do Faturamento;   

    - Interrupção no atendimento aos clientes levando à sua insatisfação; 

- **Sobre Estoque:** 

    - Custo Financeiro Elevado; 

    - Risco de Obsolescência. 

  

O **novo modelo de gestão** deve também ser capaz de: 

- **Determinar o nível ideal de estoque:** equilíbrio entre disponibilidade e custos de armazenamento; 

- **Planejamento de compras eficiente:** previsões precisas e estratégias considerando prazos, custos e mercado; 

- **Adaptabilidade às mudanças na demanda:** ajuste do estoque às necessidades do negócio. 

""") 

  

  

  

st.markdown('### III. Contextualizando o Estudo:') 

st.markdown("""Diversos produtos apresentam demanda relativamente estável, resultando em um padrão de giro de estoque similar a uma "curva dente de serra". Nesses casos, técnicas de Machine Learning, como a análise de Séries Temporais e Regressão Linear, podem ser utilizadas para prever com precisão o momento ideal para reposição do estoque. 

  

- **Abordagens Tradicionais:** 

    - Tradicionalmente, as empresas dependem de sistemas ERP que sinalizam a necessidade de compra quando o estoque atinge um nível mínimo pré-determinado; 

    - Esse valor é calculado com base na demanda do material, no lead time (tempo entre o pedido e o recebimento) e em uma reserva técnica para imprevistos; 

    - O sistema não percebe tendências de alteração de demanda, sendo essa responsabilidade atribuída ao time de negócios da empresa; 

- **Otimização com Regressão Linear:** 

    - Este projeto propõe a utilização da curva dente de serra para gerar múltiplas regressões lineares; 

    - Através delas, é possível determinar um estoque mínimo otimizado e ajustável às variações temporais da demanda; 

    - A variação do coeficiente angular das regressões lineares poderá indicar a tendência da demanda de cada produto; 

- **Análise de Séries Temporais: Uma Alternativa Viável?**  

    - Embora a análise de séries temporais também seja uma opção para previsões, o "Time to Market" para implementação dessa solução foi considerado um fator crucial; 

    - O esforço seria consideravelmente maior do que o uso de modelos de regressão linear para realizar: 

        - Exploração de dados; 

        - Modelagem; 

        - Testes; e  

        - Validação. 

    - Uma abordagem de série temporal foi parcialmente implementada para a variação do coeficiente angular das regressões lineares, através da decomposição da série temporal formada pelos diferentes coeficientes obtidos, assim, o parâmetro Trend (tendência) da decomposição de séries temporais possibilitou a análise da demanda futura. 

- **Desafio Adicional: Agrupamento de Modelos:** 

    - O principal desafio deste projeto reside na identificação da forma mais adequada de agrupar os diversos modelos de regressão linear da série de dados. 

  

""") 

  

st.markdown('### IV. Metodologia:') 

st.markdown(""" 

A biblioteca _scipy_ através de sua função _argrelextrema_ permitiram identificar os pontos de máximo e mínimo local da curva de giro de estoque.  

- Ponto de máximo local: início dos dados para a regressão linear do ciclo de consumo; 

- Ponto de mínimo local: fim dos dados para a regressão linear do ciclo de consumo; 

  

Assim, para um conjunto de dados selecionado, vários trechos de dados são gerados contendo o comportamento do consumo do material. 

Para cada trecho de dado um modelo de LR foi gerado, sendo o resultado desse modelo uma reta com os coeficientes angulares (Coef) e linear (Intercept) bem definidos. 

Cada modelo é validado através da análise da normalidade dos resíduos (_Shapiro-Wilk_), os resíduos não normais levam à rejeição do modelo e consequentemente do segmento de dados. 

Uma vez avaliados os modelos, a mediana do Coeficiente Angular é considerada para gerar a Regressão linear que vai predizer o trecho em que os dados mais recentes estão. Neste caso o valor do Coeficiente Linear se torna o próprio ponto de máximo local. 

Assim é possível prever com certa precisão o momento em que o estoque irá acabar. 

Juntando isso às informações: 

- Data prevista para fim do estoque; 

- Lead time do fornecedor; 

- Autonomia desejada para o estoque em caso de atraso na entrega pelo fornecedor (estoque estratégico); 

  

É possível determinar o ponto de compra otimizado para cada produto. Neste caso a autonomia sugerida poderá ser diferente da desejada inicialmente, uma vez que a o ponto de compra é definido como múltiplos de 100 ou 1000 para facilitar o processo de compra, impactando na autonomia do estoque, sempre incrementando seu valor. 
""") 

  

st.markdown('### V. Resultados:') 

st.markdown(""" 

- em geral, o coeficiente angular obtido na Regressão Linear (LR) representa a demanda média do produto naquele período estudado. Neste modelo de LR, o coeficiente angular é diferente do consumo médio apontado pelo sumário. Por exemplo: 

    - Para o Produto_1, no período entre os dias 06-04-2021 e 15-07-2024: 

        - Coef: -71,63, ou seja, consumo médio de aproximadamente 72 produtos/dia; 

        - Consumo médio apresentado: 99 produtos/dia útil. 
""") 

#Carrega o logo  

try: #caminho para Streamlit 

    image = Image.open('Amostragem_de_Dados/Imagem 01.png') 

except: #caminho para uso local 

    image = Image.open('Imagem 01.png') 

st.image(image, width=850)         

st.markdown(""" 

A diferença se deve à característica do consumo e da LR. O consumo acontece apenas nos dias úteis. A LR considera os dias corridos. 

Na imagem acima, é possível identificar os dias úteis na curva em azul: 

- Cada *marker* do gráfico é um dia útil; 

- O espaçamento entre um grupo de *markers* é o final de semana; 

- Um espaço interno ao grupo de *markers* é um feriado. 

Ao fazer a conversão de dias corridos para dias úteis, chega-se no valor indicado de 99 produtos/dia útil. 

""") 

st.markdown('### VI. Ferramentas utilizadas:') 
st.markdown(""" 
- Bibliotecas:
    - _scipy_ através de sua função _argrelextrema_ --> cálculo de mínimos e máximos locais;
    - _holidays_ --> cálculo de dias úteis entre duas datas, considerando o calendário oficial do Brasil;
    -_sklearn_ --> ferramentas de regressão linear e métricas;
    
- 

""")
st.markdown('### VII. Próximos Passos:') 

st.markdown(""" 

- Implantação de dashboard para monitoramento semanal dos indicadores e definição de estratégias de negócio. 
""") 

 
