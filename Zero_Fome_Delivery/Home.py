
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
df_raw = pd.read_csv('dataset\\zomato.csv')

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
A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core
business é facilitar o encontro e negociações de clientes e restaurantes. Os
restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza
informações como endereço, tipo de culinária servida, se possui reservas, se faz
entregas e também uma nota de avaliação dos serviços e produtos do restaurante,
dentre outras informações.

### II. Desafio:
Responder um conjunto de perguntas a partir da análise dos dados disponibilizados via plataforma kraggle

#### i. Geral
    a. Quantos restaurantes únicos estão registrados?
    b. Quantos países únicos estão registrados?
    c. Quantas cidades únicas estão registradas?
    d. Qual o total de avaliações feitas?
    e. Qual o total de tipos de culinária registrados?

#### ii. Pais
    a. Qual o nome do país que possui mais cidades registradas?
    b. Qual o nome do país que possui mais restaurantes registrados?
    c. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?
    d. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?
    e. Qual o nome do país que possui a maior quantidade de avaliações feitas?
    f. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?
    g. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?
    h. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?
    i. Qual o nome do país que possui, na média, a maior nota média registrada?
    j. Qual o nome do país que possui, na média, a menor nota média registrada?
    k. Qual a média de preço de um prato para dois por país?

#### iii. Cidade
    a. Qual o nome da cidade que possui mais restaurantes registrados?
    b. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?
    c. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?
    d. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
    e. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?
    f. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?
    g. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?
    h. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?

#### iv. Restaurantes
    a. Qual o nome do restaurante que possui a maior quantidade de avaliações?
    b. Qual o nome do restaurante com a maior nota média?
    c. Qual o nome do restaurante que possui o maior valor de uma prato para duas pessoas?
    d. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação?
    e. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação?
    f. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas?
    g. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?
    h. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)?

#### v. Tipos de Culinária
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

### III. Considerações sobre os dados
    i. Parte dos restaurantes não possuem avaliações. Esses restaurantes foram mantidos na base;
    ii. Parte dos restaurantes não possuem dados sobre valor do prato para 2 pessoas, esses restaurantes foram mantidos na base;
    iii. Os valores dos pratos foram convertidos para o Dollar usando como referência a cotação do dia 30/05/2023, 09:21 UTC;
    iv. uma avaliação de outliers foi realizada e, quando necessário, o valor foram substituidos pelo valor médio do conjunto;

### IV. Proximos passos:
    i. adicionar a opção de excluir os restaurantes sem avaliação e/ou preço de prato
    ii. adicionar a opção de avaliar apenas os os restaurantes sem avaliação e/ou preço de prato.
    iii. avaliar se existe alguma conclusão adicional que pode ser obtida, por exemplo sobre a cultura de avaliação.


""")


st.markdown(
"""
### Como utilizar esse Dashboard? \n
    - Visão Geral:
        - Principais números referentes à plataforma de delivery;
        - Mapa com geolocalização dos restaurantes cadastrados;
            - Através da ferramente de zoom pode-se ver os restaurantes individualmente;
            - Na barra lateral é possivel fazer um filtro por país de interesse ou configurar a página para mostrar N países com mais restaurantes na base.
    - Visão Paises:  
        - Aba "Indicadores Absolutos":
            - contém indicadores baseados em contagem, média, etc.
        - Aba "Indicadores Relativos [%]": 
            - contém indicadores comparados a quantidade de restaurantes no país, mostrando um número relativo.
            - Esses indicadores são relevantes pois retiram a distorção gerada pela variedade a quantidade de restaurantes em cada país.
            - Por exemplo: Restaurantes estilo "gourmet", olhando os números absolutos, USA tem mais restaurantes neste estilo, mas eles representam apenas 30% dos restaurantes cadastrados. Verificando na aba de Indicadores Relativos [%], pode-se ver que em Singapura mais de 70% dos restaurantes são deste tipo.
    - Visão Cidades:
        - É possivel configurar o dashdoard para limitar os gráficos nos N dados mais significativos ou, permitir mostrar todo o conteúdo. Neste caso o sistema pode apresentar um pouco de lentidão no processamento dos dados;
        - É possível também adicionar cores aos gráficos sinalizando o país;
    - Visão Restaurantes e Visão Culinária:
        - mesmas referências citadas nas páginas anteriores.
"""
)