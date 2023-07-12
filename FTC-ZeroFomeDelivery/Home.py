
# importanto módulos e funções criadas para limpeza e pré-tratamento dos dados
from data_wrangling_modules import *
# carregando demais biliotecas
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
#from PIL import Image

# carregando a base de dados
# dados obtidos no site: https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv
df_raw = pd.read_csv('FTC-ZeroFomeDelivery/dataset/zomato.csv') 
#df_raw = pd.read_csv('dataset\\zomato.csv')
#for deploy:
#df_raw = pd.read_csv('FTC-ZeroFomeDelivery/dataset/zomato.csv')

df = data_wrangling(df_raw)

st.set_page_config(page_title= 'Fome Zero Delivery', layout='wide')

#--------------------------------------------------------------
#                    Barra Lateral    
#--------------------------------------------------------------
st.sidebar.markdown('# Fome Zero Delivery')
st.sidebar.markdown('## O Melhor lugar para encontrar seu mais novo restaurante favorito!')
st.sidebar.markdown("""___""")
with st.sidebar:
    components.html(embed_component['linkedin'], height = 310)

st.write('## FCT - Ciência de Dados com Python - Projeto Final')
st.write("# Fome Zero Delivery Dashboard")

st.markdown(
"""
### I. Contexto do Problema de Negócio:
    A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro 
    e negociações entre consumidores e restaurantes.  Os restaurantes fazem o cadastro dentro da plataforma 
    da Fome Zero, que disponibiliza informações como endereço, tipo de culinária servida, se possui sistema 
    de reservas, se faz entregas e permite ao consumidor atribuir uma nota de avaliação aos serviços e produtos
    do restaurante, dentre outras informações.
    Essa estapa do projeto, um dashboard com alguns KPI's relevantes foi criado para ajudar na gestão da 
    plataforma e obter alguns insights para alavancar o seu crescimento.

	
### II. Premissas do projeto:
    1. Os dados utilizados nesse projeto foram obtidos via plataforma kraggle:
        https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv
    2. O CEO disponibilizou um conjunto de KPI's iniciais ao dashborad, mas não sendo necessário limitar-se a elas;
	3. Os indicadores foram agrupados por algumas perspectivas de negócio:
		a. Visão por Países;
		b. Visão por Cidades;
		c. Visão por Restaurantes;
		d. Visão por Culinárias.
	4. Como cada país tem sua moeda, foi utilizado o câmbio do dia câmbio de 30/05/2023, 09:21 UTC para 
    conversão dos valores dos pratos em dólar.
	5. Durante a exploração dos dados, os poucos dados discrepantes foram substituidos pelo valor 
    médio correspondente
	6. Existem restaurantes não avaliados ou sem registro do valor do prato, esses restaurantes foram 
    mantidos na base e podem ser eliminados dos gráficos através dos filtros na barra lateral;

### III. Organização do Dashboard:
#### i. Visão Geral:
    - Principais números referentes à plataforma de delivery;
    - Mapa com geolocalização dos restaurantes cadastrados;
        - Através da ferramente de zoom pode-se ver os restaurantes individualmente;
        - Na barra lateral é possivel fazer um filtro por país de interesse ou configurar a página para mostrar N países com mais restaurantes na base.
    
    - Neste dashboard, é esperado que sejam respondidas as seguintes questões:
        a. Quantos restaurantes únicos estão registrados?
        b. Quantos países únicos estão registrados?
        c. Quantas cidades únicas estão registradas?
        d. Qual o total de avaliações feitas?
        e. Qual o total de tipos de culinária registrados?

#### ii. Visão Paises:  
    - Na barra lateral é possível:
        - exluir ou incluir restaurantes sem avaliação
        - exluir ou incluir restaurantes sem registro de custo médio do prato para duas pessoas;
        - escolher o conjunto de países de interesse;
    
    - Neste dashboard, é esperado que sejam respondidas as seguintes questões:            
        a. Qual o nome do país que possui mais cidades registradas?
        b. Qual o nome do país que possui mais restaurantes registrados?
        c. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 (Gourmet) registrados?
        d. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?
        e. Qual o nome do país que possui a maior quantidade de avaliações feitas?
        f. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?
        g. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?
        h. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?
        i. Qual o nome do país que possui, na média, a maior nota média registrada?
        j. Qual o nome do país que possui, na média, a menor nota média registrada?
        k. Qual a média de preço de um prato para dois por país?

#### iii. Visão Cidades:
    - Na barra lateral é possível:
        - exluir ou incluir restaurantes sem avaliação
        - exluir ou incluir restaurantes sem registro de custo médio do prato para duas pessoas;
        - escolher o conjunto de países de interesse;
        - É possivel configurar o dashdoard para limitar os gráficos aos mais relevantes, sendo possível configurar a quantidade a ser exibida. 
          Ao se escolher todos os restaurantes, o sistema pode apresentar um pouco de lentidão no processamento dos dados;
        - É possível adicionar cores aos gráficos sinalizando o país;

    - Neste dashboard, é esperado que sejam respondidas as seguintes questões:  
        a. Qual o nome da cidade que possui mais restaurantes registrados?
        b. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?
        c. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?
        d. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
        e. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?
        f. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?
        g. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?
        h. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?

#### iv. Visão Restaurantes:
    - Na barra lateral é possível:
        - exluir ou incluir restaurantes sem avaliação
        - exluir ou incluir restaurantes sem registro de custo médio do prato para duas pessoas;
        - escolher o conjunto de países de interesse;
        - É possível adicionar cores aos gráficos sinalizando o país;
        
    - Neste dashboard, é esperado que sejam respondidas as seguintes questões:  
        a. Qual o nome do restaurante que possui a maior quantidade de avaliações?
        b. Qual o nome do restaurante com a maior nota média?
        c. Qual o nome do restaurante que possui o maior valor de uma prato para duas pessoas?
        d. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação?
        e. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação?
        f. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas?
        g. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?
        h. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)?

#### v. Visão Tipos de Culinária:
    - Na barra lateral é possível:
        - exluir ou incluir restaurantes sem avaliação
        - exluir ou incluir restaurantes sem registro de custo médio do prato para duas pessoas;
        - escolher o conjunto de países de interesse;
        
    - Neste dashboard, é esperado que sejam respondidas as seguintes questões:  
        a. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?
        b. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?
        c. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?
        d. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a menor média de avaliação?
        e. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a maior média de avaliação?
        f. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a menor média de avaliação?
        g. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação?
        h. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a menor média de avaliação?
        i. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a maior média de avaliação?
        j. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a menor média de avaliação?
        k. Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas?
        l. Qual o tipo de culinária que possui a maior nota média?
        m. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas?


### IV. Proximos passos:
    i. adicionar a opção de avaliar apenas os os restaurantes sem avaliação e/ou preço de prato.
    ii. fazer uma avaliação global dos dados para obter mais insights para o negócio.


""")

