import linecache as lc
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

# bibliotecas para manipulação de dados
import pandas as pd
import numpy as np

# bibliotecas de visualização de dados:
from matplotlib           import pyplot  as plt

# biblioteca de aprendizado de máquina
from sklearn.linear_model import LinearRegression
from sklearn.neighbors    import KNeighborsClassifier
from sklearn              import metrics         as mt
from sklearn              import datasets        as ds
from sklearn              import model_selection as ms


st.set_page_config(page_title= 'Aprendizado de Máquina - Classificação - KNN', layout='wide')

#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
#                                Barra Lateral
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
# coloca o link do LinkedIn no objeto

embed_component = {'linkedin':"""<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
                  <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL" data-vanity="farzinbassiri" data-version="v1"><a class="badge-base__link LI-simple-link" href="https://br.linkedin.com/in/farzinbassiri?trk=profile-badge">"""}


st.header('Regressão Linear:')
st.subheader('Influência de Outliers nas Métricas de Performance.')
st.markdown("""___""")
st.sidebar.markdown('## Regressão Linear: Influência de Outliers nas Métricas de Performance.')
#Carrega o logo 
try: #caminho para Streamlit
    image = Image.open('Outliers_and_metrics/logo.jpg')
except: #caminho para uso local
	image = Image.open('logo.jpg')
st.sidebar.image(image, width=240)

st.sidebar.markdown("""___""")
#coloca o objeto LinkedIn na barra lateral
with st.sidebar:
    components.html(embed_component['linkedin'], height = 310)

	
st.sidebar.markdown("""___""")
st.sidebar.markdown('###### Powered by Farzin Bassiri')


st.markdown('### I. Motivação para o projeto:')
st.markdown("""Durante aulas de regressão linear, quando adicionados outliers, existe uma alteração significativa nos coeficientes linear e angular da regressão ao mesmo tempo em que as métricas de desempenho se deterioram.   
			**Mas como seria o comportamento da métrica de desempenho se os coeficientes não se alterassem?**  
			Durante o projeto, houve o cuidado em balancear os outliers para minimizar a alteração dos coeficientes da regressão linear, podendo, desta forma, aprender sobre o comportamento das métricas isoladamente ao serem influenciadas pelos outliers. """)

st.markdown('### II. Contextualizando o Estudo:')
st.markdown("""Ao iniciar os estudos sobre as métricas de desempenho nas regressões lineares resolvi isolar a deterioração da performance gerada por uma alteração nos coeficientes da regressão e a deterioração causada pelos pontos distantes da reta de regressão adicionados como outliers. Ao fazer isso pude entender melhor como cada métrica é sensível à adição de outliers.

Neste estudo utilizei as métricas:  
- RMSE:  
	Erro Quadrático Médio de Raiz. Em resumo, ele mede a diferença média entre os valores previstos por um modelo (neste caso a regressão linear) e os valores reais observados. Ele leva em conta o tamanho da diferença ao elevar as diferenças ao quadrado, o que penaliza mais erros maiores. Por fim, calcula a raiz quadrada desses quadrados para obter de forma a obter a mesma unidade de medida das variáveis do modelo.
				
- MAPE:  
	O MAPE calcula a média das diferenças percentuais entre os valores previstos por um modelo (neste caso a regressão linear) e os valores reais observados. Ele mede o erro como uma porcentagem da magnitude real do valor, tornando-o útil para comparar performance do modelo em dados com grande escala de valores.
- MAE:  
	O Erro Médio Absoluto (MAE) é uma métrica de desempenho em regressão linear que mede a diferença média entre os valores previstos por um modelo e os valores reais observados. Ele é calculado como a média dos erros absolutos, ou seja, o valor absoluto da diferença entre o valor previsto e o valor real.

- R²:  
Coeficiente de determinação (R²): O R² é uma medida da variância dos dados explicada pela regressão. Quando outliers são adicionados a um conjunto de dados, o R² geralmente diminui. Isso ocorre porque os outliers são valores que não estão bem representados pela linha de regressão. O R² varia entre 0 e 1, sendo 1 o valor para uma regressão linear perfeita.

""")


st.markdown('### III. Metodologia:')
st.markdown("""Para adicionar outliers a um conjunto de dados, criei um vetor indexador. O vetor indexador foi criado com números inteiros aleatórios, entre 0 e o tamanho do conjunto de dados.\n
O tamanho do vetor indexador foi definido como um percentual do tamanho do conjunto de dados.  \n
Por exemplo, se o conjunto de dados tem 1.000 pontos e é desejado 10% de outliers, o vetor terá 100 pontos.  \n
O vetor indexador foi, então, utilizado para apontar quais elementos do conjunto de dados seriam alterados.  \n
Os valores pares do vetor foram acrescidos de um valor fixo, enquanto os valores impares foram decrementados do mesmo valor.
""")

st.markdown('### V. Organização do Dashboard:')
st.markdown("""O dashboard possui uma barra lateral de configurações. O usuário pode deixar no modo pré-definido ou escolher:  
- A quantidade de pontos no dataset;
- A dispersão dos pontos no dataset;
- A proporção de outliers a ser inserido no dataset;
- Variar a '*semente*' (seed/random_state) que irá determinar a aleatoriedade tanto do dataset quanto dos outliers;  
- Definir o offset dos outliers;
- Definir o offset dos dados.

\n Na janela principal, existem 3 abas:
- **Gráficos**:  
	- Gráfico dos dados sem outlier inserido (dados de referência) junto com a regressão linear;
	- Blocos de texto com:
		- Métricas da regressão linear;
		- Coeficientes da regressão linear;
		- Teste de normalidade dos resíduos (via Shapiro-Wilk). Esse teste é necessário para avaliar a qualidade da regressão linear. É esperado que uma boa regressão linear gere resíduos com distribuição normal. Uma ausência de normalidade deve ser investigada.
	- Histograma com a análise de dispersão dos resíduos da regressão linear sobre os dados de referência;
- **Comparativo**:
	- Gráfico dos dados sem outlier inserido (dados de referência) junto com todas as diferentes regressões lineares geradas, mostrando a variação dos coeficientes da regressão ao adicionar diferentes proporções de outliers;
	- Conjunto de gráficos de barras mostrando como cada métrica se comporta ao adicionar diferentes proporções de outliers;
	- Gráfico de barras com as **variações** das métricas em diferentes proporções de outliers. Todas as variações são tomadas em relação às métricas da regressão linear sem outliers inseridos;
	- Gráficos com a evolução dos coeficientes linear e angular da reta de regressão ao adicionar as diferentes proporções de outliers e suas dispersões;
	- Tabela com as informações agrupadas de forma a fazer comparações entre os dados;
- **Conclusões**:
	- Percepções e aprendizados.
""")

