
# Bibliotecas de manipulação de arquivos
import linecache as lc

import streamlit as st
import streamlit.components.v1 as components

from PIL import Image

# bibliotecas para manipulação de dados
import pandas as pd
import numpy as np

# bibliotecas de visualização de dados:
import plotly.express     as px
import matplotlib.ticker  as ticker
import seaborn            as sns
from matplotlib           import pyplot    as plt

	
# biblioteca de aprendizado de máquina
from sklearn.linear_model  import LinearRegression
from sklearn.neighbors     import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics       import ConfusionMatrixDisplay
from sklearn               import metrics                as mt
from sklearn               import datasets               as ds
from sklearn               import model_selection        as ms

st.set_page_config(page_title= 'Aprendizado de Máquina - Classificação - KNN', layout='wide')

#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
#                                Barra Lateral
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
# coloca o link do LinkedIn no objeto

embed_component = {'linkedin':"""<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
                  <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL" data-vanity="farzinbassiri" data-version="v1"><a class="badge-base__link LI-simple-link" href="https://br.linkedin.com/in/farzinbassiri?trk=profile-badge">"""}


st.header('O Poder da Amostragem Adequada na Classificação de Dados:')
st.subheader('Classificação e predição da posição da alavanca do câmbio durante uso do veículo.')
st.markdown("""___""")
st.sidebar.markdown('## Classificação e predição da posição da alavanca do câmbio durante uso do veículo.')
#Carrega o logo 
try: #caminho para Streamlit
    image = Image.open('Amostragem_de_Dados/logo_cambio.jpg')
except: #caminho para uso local
    image = Image.open('logo_cambio.jpg')
st.sidebar.image(image, width=240)

st.sidebar.markdown("""___""")
#coloca o objeto LinkedIn na barra lateral
with st.sidebar:
    components.html(embed_component['linkedin'], height = 310)

st.sidebar.markdown("""___""")
st.sidebar.markdown('###### Imagem câmbio: https://www.vectorstock.com/royalty-free-vector/manual-gearshift-icon-car-and-transmission-vector-5518279')	
	
	
st.sidebar.markdown("""___""")
st.sidebar.markdown('###### Powered by Farzin Bassiri')


st.markdown('### I. Contexto do Problema de Negócio:')
st.markdown("""A qualidade da amostragem de dados de treinamento desempenha um papel crucial no sucesso dos algoritmos de classificação.
	Neste breve artigo, vou compartilhar insights valiosos provenientes de um estudo  que estou conduzindo sobre diferentes 
	algoritmos de classificação, destacando como duas abordagens distintas na amostragem dos mesmos dados podem determinar o 
	êxito ou o fracasso do algoritmo escolhido.
""")

st.markdown('### II. Contextualizando o Estudo:')
st.markdown("""A qualidade da amostragem de dados de treinamento desempenha um papel crucial no sucesso dos algoritmos de classificação. Neste breve artigo, vou compartilhar insights valiosos provenientes de um estudo que estou conduzindo sobre diferentes algoritmos de classificação, destacando como duas abordagens distintas na amostragem dos mesmos dados podem determinar o êxito ou o fracasso do algoritmo escolhido.""")

st.markdown('### III. Sobre os dados:')
st.markdown("""O conjunto de dados possui 20 graus de liberdade, incluindo informações como data e hora da coleta, consumo instantâneo de combustível, velocidade do veículo, velocidade do motor, fluxo de combustível para o motor, posição do pedal do acelerador, emissão média de carbono, entre outras.  
Algumas variáveis apresentam correlações claras, como a velocidade do veículo e a velocidade do motor, assim como o fluxo de combustível para o motor e a posição do pedal do acelerador.  
No âmbito deste estudo, selecionei as variáveis *'Velocidade do veículo'*, *'Velocidade do motor'* e *'Fluxo de combustível para o motor'* para categorizar as 5 posições do câmbio. Após a limpeza e organização dos dados, a classificação das marchas foi adicionada manualmente ao conjunto de dados com o propósito de validar a classificação das marchas feitas pelo modelo em estudo.  
Por se tratar de um veículo de câmbio manual, para cada posição do câmbio (ou para cada marcha) existe uma relação linear entre a velocidade do veículo e a velocidade do motor. Desta forma é de se esperar que possa ser possível predizer a marcha a partir dessas duas variáveis. A variável 'Fluxo de combustível para o motor' se mostrou capaz de melhorar a acurácia dos modelos de classificação e por isso foi utilizada também. Outras variáveis do conjunto de dados foram excluídas do escopo desse estudo.  
Adicionalmente, é esperado que ocorram variações aleatórias da relação velocidade do veículo e velocidade do motor devido ao escorregamento da embreagem. Os dados coletados durante a troca das marchas foram eliminados da base de dados durante a fase de organização e limpeza dos dados.

* Dados do Veículo:
	* **Marca/Modelo:** Honda Civic
	* **Ano/modelo:** 2003/2003
	* **Câmbio**: Manual de 5 velocidades 
	* **Motor:** 1.7cc a gasolina
""")

st.markdown('### IV. Metodologia:')
st.markdown("""Neste artigo utilizei a biblioteca sklearn para fazer a classificação dos dados e diferentes bibliotecas de visualização gráfica de forma a enriquecer o conhecimento geral das ferramentas.  
O modelo de classificação escolhido foi o KNN, embora outros tenham sido utilizados durante o estudo, o KNN se mostrou simples e com resultado bastante satisfatório.  
Utilizei a técnica Treino-Validação-Teste e me vali do Elbow Method para determinação do ponto ótimo de configuração do algoritmo (melhor valor k).  
A proporção de amostras para cada uma das fases (treino, validação e teste) foi escolhido empiricamente de forma a maximizar a acurácia da classificação.  
O estudo é dividido em duas partes onde a primeira é baseada em cerca de 9.000 amostras concentradas em 3 diferentes velocidades do motor: 1.000 RPM, 2.000 RPM e 3.000 RPM (apenas 1ª marcha) ou 4.000 RPM (demais marchas). Já a segunda parte do estudo foram utilizados cerca de 9.000 amostras aleatoriamente escolhidas no conjunto de dados. 
""")

st.markdown('### V. Organização do Dashboard:')
st.markdown("""Cada uma das formas amostragem foi organizada em uma página diferente do dashboard:

a. Amostras Concentradas;

b. Amostras Aleatórias.

Na barra lateral é possivel:
* Escolher se o parâmetro K será o obtido via Elbow Method ou escolher manualmente o K desejado;
	* caso o valor de K seja definido pelo usuário, o gráfico que mostra o resultado do Elbow Method é suprimido do dashboard;
* Definir a faixa de valores a ser utilizada pelo Elbow Method, aumentar a faixa pode impactar a velocidade do algoritmo;
* Para as amostras concentradas: 
	* Alterar a quantidade de amostras destinadas ao teste, as amostras restantes serão sempre igualmente divididas entre Validação e Teste;
* Para as amostras aleatórias:
	* Alterar a quantidade total de amostras disponíveis para Treino-Validação-Teste. A barra de seleção apresenta o valor percentual em relação à totalidade de dados disponíveis;
	* Alterar a quantidade de amostras destinadas ao teste, as amostras restantes serão sempre igualmente divididas entre Validação e Teste;
	
""")

st.markdown('###')
st.markdown("""
""")

st.markdown("""Detalhamento dos dados coletados: 
 * Dados obtidos via dispositivo conectado à interface ODBII e app Torque Pro durante o uso do app entre 22/jun/2023 e 01/nov/2023.
* Arquivo exportado para formato CSV pelo proprio app.
 Os dados obtidos são:
 	* Device Time   --> data e hora da coleta do dado	
	* Engine RPM	--> velocidade do motor em Rotações por Minuto (RPM)
	* Fuel flow(l/h)	--> vazão de combustivel no motor. Essa métrica permite avaliar consumo de combustivel com o veículo parado, por exemplo
	* Speed (OBD)(km/h) --> velocidade do veiculo
    * Relacao --> dado adicionado ao dataset durante data wrangling: é a razão entre velocidade do motor e velocidade do veículo, ou seja a "relação da marcha". É esperado haver um cluster de dados para cada marcha, onde o valor central de cada marcha é:
		* 1ª marcha: 145
		* 2ª marcha: 73
		* 3ª marcha: 48
		* 4ª marcha: 37
		* 5ª marcha: 31
    * Marcha --> dado adicionado ao dataset durante o data wrangling: é a posição do câmbio para aquele dado, ou seja, a marcha. Esse é o campo de "label" para o algoritmo Essa coluna possui dois formatos a serem carregados ao longo do estudo:
		* Amostragem concentrada em 3 regiões da faixa de dados:
			* Indicação da marcha correta inseridas na região de 1.000 RPM, 2.000 RPM, 3.000 RPM (apenas 1ª marcha) e 4.000 RPM (demais marchas)
		* Amostragem ampla, varrendo toda a faixa de dados.  
""")