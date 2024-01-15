 
# Bibliotecas de manipulação de arquivos
import linecache as lc

import streamlit as st
import streamlit.components.v1 as components

from PIL import Image

# bibliotecas para manipulação de dados
import pandas as pd
import numpy as np
from scipy.stats import shapiro 
import scipy

# bibliotecas de visualização de dados:
import matplotlib.ticker  as ticker
from matplotlib           import pyplot    as plt

	
# biblioteca de aprendizado de máquina
from sklearn.linear_model  import LinearRegression
from sklearn.neighbors     import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics       import ConfusionMatrixDisplay
from sklearn               import metrics                as mt
from sklearn               import datasets               as ds
from sklearn               import model_selection        as ms

#from sklearn.metrics       import PredictionErrorDisplay

st.set_page_config(page_title= 'Regressão Linear', layout='wide', page_icon="chart_with_upwards_trend")

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
#st.markdown("""___""")
st.sidebar.markdown('## Regressão Linear: Influência de Outliers nas Métricas de Performance.')
#Carrega o logo 
try: #caminho para Streamlit
    image = Image.open('Outliers_and_metrics/logo.jpg')
except: #caminho para uso local
	image = Image.open('logo.jpg')
st.sidebar.image(image, width=240)

st.sidebar.markdown("""___""")

# cria a lista de valores para o usuário escolher e coloca em uma lista de escolha única

auto_mode = st.sidebar.checkbox('##### Deseja utilizar os parâmetros pré-definidos?', value=True)
if auto_mode == True:
	st.sidebar.markdown('   - Quantidade de pontos = 1000')
	st.sidebar.markdown('   - Dispersão dos dados = 50')
	st.sidebar.markdown('   - Percentual de outliers = 10')
	st.sidebar.markdown('   - Aleatoriedade (*seed/random_state*) = 0')
	st.sidebar.markdown('   - Offset dos outliers = 250')
	st.sidebar.markdown('   - Offset dos dados = 300')

n_samples = st.sidebar.selectbox(
                        'Selecione a quantidade de pontos:',
                        np.arange(500, 10001, 100),
						index = 5,
						disabled = auto_mode)

noise = st.sidebar.selectbox(
                        'Selecione a dispersão dos dados:',
                        np.arange(10, 101, 5),
						index = 8,
						disabled = auto_mode)

percent_max = st.sidebar.selectbox(
                        'Selecione a quantidade de outliers (% sobre os dados):',
                        np.arange(1, 21, 1),
						index = 9,
						disabled = auto_mode)

random_state = st.sidebar.selectbox(
                        'Selecione o padrão de aleatoriedade (seed/random_state):',
                        np.arange(0, 41, 1),
						disabled = auto_mode)

offset_slider = st.sidebar.slider(
						'Offset desejado para os outliers',
						min_value = noise*2,
						max_value = 500,
						value = noise*5,
						step = 25,
						disabled = auto_mode)

bias_slider = st.sidebar.slider(
						'Offset desejado para os dados sem outliers',
						min_value = 0,
						max_value = 500,
						step = 25,
						value = 300,
						disabled = auto_mode)

st.sidebar.divider()
#coloca o objeto LinkedIn na barra lateral
with st.sidebar:
    components.html(embed_component['linkedin'], height = 310)
	
st.sidebar.divider()
st.sidebar.markdown('###### Powered by Farzin Bassiri')



#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
#                                Iniciando os arrays & dados
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------

#cria o vetor de métricas para comparar efeito de outliers
result_list = []
X = []
y = []
residual = []

df_result = pd.DataFrame(columns = ['Percent', 'RMSE', 'MAPE', 'MAE', 'R2', 'Delta_RMSE(%)', 'Delta_MAPE(%)', 'Delta_MAE(%)','Delta_R2(%)','Coef', 'Intercept'])

# dataset será construido a partir de dados sintéticos, conforme o conhecimento for expandindo, a complexidade dos dados será aumentada

if auto_mode == True:
	noise = 50.0
	random_state = 0
	percent_max = 10
	n_samples = 1000
	offset_slider = noise*5
	bias_slider = 300

n_features = 1
n_informative = 1
n_targets = 1

start_outlier_index = 0
end_outlier_index = 0
percent = 0
ncols = 2
# cria uma lista aleatória que vai servir de indice para os outliers
np.random.seed(40)
outlier_index = np.random.choice(n_samples, size=int(n_samples*percent_max/100), replace=False)

# cria os dados sintéticos para a Regressão Linear
X_raw, y_raw = ds.make_regression(
    n_samples = n_samples, 
    n_features = n_features,
    n_informative = n_informative,
    n_targets = n_targets,
    noise = noise, 
	bias = bias_slider,
    random_state = random_state)

X = np.copy(X_raw)
y = np.copy(y_raw)



#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
#                                Gerando os resultados
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------


#criando abas
tab1, tab2, tab3 = st.tabs(['📈 Gráficos', ':thinking_face: Comparativo', '💡 Conclusões'])


with tab1:
	# cria o grid dos gráficos, primeiro com uma coluna, depois com duas colunas
	
	# gráfico dos dados sem outliers
	with st.container(border=True):
		#separa os dados de treino e teste
		X_train, X_test, y_train, y_test = ms.train_test_split(X, y, test_size=0.2, random_state=0)

		# Treinamento do algoritmo
		lr_model = LinearRegression()
		lr_model.fit( X_train, y_train )

		# Previsão do algoritmo
		y_pred = lr_model.predict( X_test )

		#perform Shapiro-Wilk test for normality of residuals
		residual = y_test - y_pred
		residual_p_value = shapiro(residual)
		# avalia se o p_valor indica resíduos normais 
		if residual_p_value[1] > 0.05:
			normalidade = 'Resíduo da regressão linear é normal. ' + '\n' + 'A Regressão Linear está bem modelada.'
		else:
			normalidade = 'Resíduo da regressão linear não é normal.' +'\n' + 'A Regressão Linear não está bem modelada.'		

		RMSE = np.round(mt.mean_squared_error(y_test, y_pred, squared=False), 2)
		mape = np.round(mt.mean_absolute_percentage_error(y_test, y_pred),2)
		mae = np.round(mt.mean_absolute_error(y_test, y_pred),2)
		R2 = np.round(mt.r2_score(y_test, y_pred),2)

		result_list = pd.Series(data={'Percent': percent, 
									  'RMSE': RMSE,
									  'MAPE': mape, 
									  'MAE': mae,
									  'R2': R2,
									  'Coef':np.round(lr_model.coef_[0],4),
									  'Intercept':np.round(lr_model.intercept_,4)})

		df_result = pd.concat([df_result, result_list.to_frame().T], ignore_index=True)

		
		fig = plt.figure(constrained_layout=True, figsize=(7,2))
		plt.title('Influência dos Outliers na regressão linear: Dados de referência (sem outliers)', fontsize=9)
		plt.scatter(x=X, y=y, label = 'Dados Sintéticos', s=5)
		plt.plot(X_test, y_pred, color='red', label = 'Regressão Linear')
		plt.grid(color='b', linestyle='-', linewidth=0.1)  
		plt.legend(fontsize=7)
		st.pyplot(fig, use_container_width=True) 
		
		text_box1, text_box2, text_box3 = st.columns(3, gap="small")

		with text_box1:
			st.text_area('**Resultados da Regressão Linear:**', 'RMSE: '+str(RMSE)+'\n'+'MAPE: '+str(mape)+'\n'+'MAE: '+str(mae) + '\n' + 'R2: '+str(R2), height = 110)
		with text_box2:
			st.text_area('**Coeficientes da Regressão Linear:**', 'Coeficiente Linear (Intercept): '+str(np.round(lr_model.intercept_,2))+'\n'+'Coeficiente Angular (Coef): '+str(np.round(lr_model.coef_[0],2)), height = 110)		
		with text_box3:
			st.text_area('**Teste de Normalidade dos Resídues (Teste Shapiro-Wilk):**', 'P-valor = ' + str(np.round(residual_p_value[1],4)) + '\n' + normalidade, height = 110)
			
		
		
		with st.container():
			#nbins = int(1 + 3.322 * math.log(len(y_pred)))
			fig = plt.figure(constrained_layout=True, figsize=(12,3))
			plt.title('Distribuição dos Resíduos da Regressão Linear (sem outliers)', fontsize=12)
			plt.hist(residual, density = True, histtype = 'bar', rwidth = 0.9, align = 'mid')
			plt.ylabel('Densidade de probalibilidade', fontsize=10)
			plt.legend(fontsize=7)
			st.pyplot(fig, use_container_width=True) 			
		
		
		
		
	cols = st.columns(ncols)
	for col in range(ncols):
		with cols[col]:
			for percent in range(col+1,percent_max+1,ncols):
				with st.container(border=True):
					#criando outliers
					outlier_size = int(n_samples*percent/100)  
					
					start_outlier_index = 0
					end_outlier_index = start_outlier_index + outlier_size
					outliers = outlier_index[start_outlier_index:end_outlier_index]
					
					X_out = X[outliers]
					y_out = y[outliers]
					# coloca offsset diferente nos dados com índice par x impar
					y_out[0::2] += offset_slider
					y_out[1::2] -= offset_slider
					
					y[outliers] = y_out

					outliers = outlier_index[:outlier_size]
					X_out = X[outliers]
					y_out = y[outliers]					

					#separa os dados de treino e teste
					X_train, X_test, y_train, y_test = ms.train_test_split(X, y, test_size=0.2, random_state=0)

					# Treinamento do algoritmo
					lr_model = LinearRegression()
					lr_model.fit( X_train, y_train )


					# Previsão do algoritmo
					y_pred = lr_model.predict( X_test )

					RMSE = mt.mean_squared_error(y_test, y_pred, squared=False)
					mape = mt.mean_absolute_percentage_error(y_test, y_pred)
					mae = mt.mean_absolute_error(y_test, y_pred)
					R2 = mt.r2_score(y_test, y_pred)
					coef = lr_model.coef_[0]
					intercept = lr_model.intercept_

					# cria uma série para formar o dataframe com os resultados
					result_list = pd.Series(data={'Percent': percent, 
												  'RMSE': RMSE,
												  'MAPE': mape, 
												  'MAE': mae,
												  'R2': R2,
												  'Coef': coef,
												  'Intercept':intercept})
					
					#cria o dataframe de resultados
					df_result = pd.concat([df_result, result_list.to_frame().T], ignore_index=True)
					
					#calcula a variação de cada métrica em relação à regresão linear sem outliers
					filtro = df_result['Percent'] == 0
					delta_rmse = np.round(((RMSE / df_result.loc[filtro, 'RMSE'].values)-1)*100,1)
					delta_mape = np.round(((mape / df_result.loc[filtro, 'MAPE'].values)-1)*100,1)
					delta_mae = np.round(((mae / df_result.loc[filtro, 'MAE'].values)-1)*100,1)
					delta_R2 = np.round(((R2 / df_result.loc[filtro, 'R2'].values)-1)*100,1)

					
					filtro = df_result['Percent'] == percent
					df_result.loc[filtro, 'Delta_RMSE(%)'] = np.round(delta_rmse,2)
					df_result.loc[filtro, 'Delta_MAPE(%)'] = np.round(delta_mape,2)
					df_result.loc[filtro, 'Delta_MAE(%)']  = np.round(delta_mae,2)
					df_result.loc[filtro, 'Delta_R2(%)']   = np.round(delta_R2,2)
					
					
					df_result = df_result.sort_values(by='Percent', ascending=True)
					
					fig = plt.figure(constrained_layout=True, figsize=(7,3))
					plt.title('Influência dos Outliers na regressão linear: '+ str(percent) + '% de outliers inseridos', fontsize=9)
					plt.scatter(X_raw, y_raw, label = 'Dados', s=3)
					plt.scatter(X_out, y_out, label = 'Outliers', s=5, c='lime')        					
					plt.plot(X_test, y_pred, color='red', label = 'Regressão Linear')
					plt.grid(color='b', linestyle='-', linewidth=0.1)  
					plt.legend(fontsize=7)
					st.pyplot(fig, use_container_width=True) 

					X = np.copy(X_raw)
					y = np.copy(y_raw)
					
					text_box1, text_box2 = st.columns(2, gap="small")
					
					with text_box1:
						text = 'RMSE: '+str(np.round(RMSE,2))+'\n'+'MAPE: '+str(np.round(mape,2))+'\n'+'MAE: '+str(np.round(mae,2))+ '\n' + 'R2: '+str(np.round(R2,2))
						st.text_area('**Resultados da Regressão Linear:**', text, key=percent*y[col], height = 110)
						
					with text_box2:
						with st.container():
							text = 'Coeficiente Linear (Intercept): '+str(np.round(lr_model.intercept_,2))+'\n'+'Coeficiente Angular (Coef): '+str(np.round(lr_model.coef_[0],2))
							st.text_area('**Coeficientes da Regressão Linear:**', text, key=percent*X[col], height = 110)

					
with tab2:
	with st.container():
		x_lr = np.arange(X.min()*1.05,X.max()*1.05,0.1)
		fig = plt.figure(constrained_layout=True, figsize=(10,4))
		plt.scatter(X,y, label='Dados Sintéticos sem outliers')
		for i in range(percent_max+1):
			y_lr = df_result.loc[i,'Coef'] * x_lr + df_result.loc[i,'Intercept'] 
			plt.plot(x_lr, y_lr, label='LR: Percentual de outliers: ' + str(i) + '%')
			
		plt.grid(color='b', linestyle='-', linewidth=0.1)  
		plt.title('Variação entre as regressões lineares (LR) ao adicionar outliers em diferentes proporções', fontsize=9)
		
		
		plt.legend(fontsize=7)
		st.pyplot(fig, use_container_width=True) 
		

	with st.container(border=True):
		st.subheader('Métricas da regressão linear')
		width = 0.75
		
		fig, ax1 = plt.subplots(2,2, figsize=(10,5))
		#ax1[0,0].set_title('Métricas da regressão linear', fontsize=10)
		
		ax1[0,0].set_xlabel('Percentual de outlier adicionado', fontsize=9)
		ax1[0,0].set_ylabel('Valor da Métrica \n (Desejável ser pequeno)', color='k', fontsize=7)
		ax1[0,0].tick_params(axis='y', labelcolor='k')
		ax1[0,0].grid(color='b', linestyle='-', linewidth=0.1)  
		ax1[0,0].set_xticks(np.arange(0, percent_max+1, 1)) #Define os valores do eixo X
		ax1[0,0].bar(df_result['Percent'], df_result['MAPE'], width, label='MAPE', color='cornflowerblue')
		ax1[0,0].legend(fontsize=7) 
		ax1[0,0].tick_params(axis = 'both', labelsize = '7')
		
		ax1[0,1].set_xlabel('Percentual de outlier adicionado', fontsize=9)
		ax1[0,1].set_ylabel('Valor da Métrica \n (Desejável ser pequeno)', color='k', fontsize=7)
		ax1[0,1].tick_params(axis='y', labelcolor='k')
		ax1[0,1].grid(color='b', linestyle='-', linewidth=0.1)  
		ax1[0,1].set_xticks(np.arange(0, percent_max+1, 1)) #Define os valores do eixo X
		ax1[0,1].bar(df_result['Percent'], df_result['MAE'], width, label='MAE', color='darkorange')
		ax1[0,1].legend(fontsize=7) 
		ax1[0,1].tick_params(axis = 'both', labelsize = '7')
		
		ax1[1,0].set_xlabel('Percentual de outlier adicionado', fontsize=9)
		ax1[1,0].set_ylabel('Valor da Métrica \n (Desejável ser pequeno)', color='k', fontsize=7)
		ax1[1,0].tick_params(axis='y', labelcolor='k')
		ax1[1,0].grid(color='b', linestyle='-', linewidth=0.1)  
		ax1[1,0].set_xticks(np.arange(0, percent_max+1, 1)) #Define os valores do eixo X
		ax1[1,0].bar(df_result['Percent'], df_result['RMSE'], width, label='RMSE', color = 'firebrick')		
		ax1[1,0].legend(fontsize=7) 
		ax1[1,0].tick_params(axis = 'both', labelsize = '7')
		
		ax1[1,1].set_xlabel('Percentual de outlier adicionado', fontsize=9)
		ax1[1,1].set_ylabel('Valor da Métrica \n (Desejável ser próximo de 1)', color='k', fontsize=7)
		ax1[1,1].tick_params(axis='y', labelcolor='k')
		ax1[1,1].grid(color='b', linestyle='-', linewidth=0.1)  
		ax1[1,1].set_xticks(np.arange(0, percent_max+1, 1)) #Define os valores do eixo X
		ax1[1,1].bar(df_result['Percent'], df_result['R2'], width, label='R2', color = 'forestgreen')		
		ax1[1,1].legend(fontsize=7) 
		ax1[1,1].tick_params(axis = 'both', labelsize = '7')
		
		plt.subplots_adjust(hspace=0.5)
		st.pyplot(fig, use_container_width=True) 				
		
	with st.container(border=True):
		# Create some mock data
		fig, ax1 = plt.subplots(1,2, figsize=(10,4))

		ax1[1].set_xlabel('Percentual de outlier adicionado', fontsize=9)
		ax1[1].set_ylabel('Coeficiente Angular(Coef)', color='k', fontsize=9)
		ax1[1].plot(df_result['Percent'], df_result['Coef'], label='Coeficiente Angular(Coef)', color='k')
		ax1[1].tick_params(axis='y', labelcolor='k')
		ax1[1].grid(color='b', linestyle='-', linewidth=0.1)  
		ax1[1].tick_params(axis = 'both', labelsize = '7')

		ax2 = ax1[1].twinx()  # instantiate a second axes that shares the same x-axis
		ax2.set_ylabel('Coeficiente Linear (Intercept)', color='b', fontsize=9)  # we already handled the x-label with ax1
		ax2.plot(df_result['Percent'], df_result['Intercept'], label='Coeficiente Linear (Intercept)', color='b')
		ax2.tick_params(axis='y', labelcolor='b')
		ax2.tick_params(axis = 'both', labelsize = '7')

		fig.tight_layout(pad=5.0)  # otherwise the right y-label is slightly clipped

		plt.title('Variação dos coeficientes da regressão linear', fontsize=10)

		
		width = 0.25
		ax1[0].bar(df_result['Percent'], df_result['Delta_MAPE(%)'], width, label='Delta_MAPE(%)', color = 'cornflowerblue')
		ax1[0].bar(df_result['Percent']+ width, df_result['Delta_MAE(%)'], width, label='Delta_MAE(%)', color='darkorange')
		ax1[0].bar(df_result['Percent']+ width*2, df_result['Delta_RMSE(%)'], width, label='Delta_RMSE(%)', color = 'firebrick')
		ax1[0].bar(df_result['Percent']+ width*3, df_result['Delta_R2(%)'], width, label='Delta_R2(%)', color = 'forestgreen')
		ax1[0].set_title('Variação percentual sobre o valor sem outlier', fontsize=10)
		ax1[0].set_ylabel('Variação percentual', loc='center', fontsize=9)
		ax1[0].set_xlabel('Percentual de outlier adicionado', fontsize=9)
		ax1[0].legend(fontsize=7, loc='upper left') 
		#specify axis tick step sizes
		ax1[0].set_xticks(np.arange(0, percent_max+1, 1))
		ax1[0].grid(color='b', linestyle='-', linewidth=0.05)  
		ax1[0].tick_params(axis = 'both', labelsize = '7')
		ax1[1].set_xticks(np.arange(0, percent_max+1, 1))

		plt.subplots_adjust(hspace=3)

		st.pyplot(fig, use_container_width=True) 

			
	with st.container():
		fig, ax = plt.subplots(1,2, figsize=(12,4))
		ax[0].boxplot(df_result['Coef'], showmeans=True)
		ax[1].boxplot(df_result['Intercept'], showmeans=True)
		ax[0].grid(color='b', linestyle='-', linewidth=0.05)  
		ax[1].grid(color='b', linestyle='-', linewidth=0.05)  

		ax[0].set_title('Variação do Coeficiente Angular (Coef) ao adicionar outliers', fontsize=10)
		ax[0].set_ylabel('Coeficiente Angular (Coef)', loc='center')
		
		ax[1].set_title('Variação do Coeficiente Linear (Intercept) ao adicionar outliers', fontsize=10)
		ax[1].set_ylabel('Coeficiente Linear (Intercept)', loc='center')
		
		plt.subplots_adjust(hspace=3)
		fig.tight_layout(pad=5.0)  
		plt.legend(fontsize=7)
		st.pyplot(fig, use_container_width=True) 
		
	with st.container():
		# Mostra a tabela com o resumo dos resultados obtidos
		st.subheader('Resultado Compilado')
		st.dataframe(df_result, hide_index=True, use_container_width=True, height=3+35*(percent_max+2))
	
		
with tab3:
	with st.container():
		st.title('Conclusões')
		with st.expander('Aprendizados obtidos:', expanded=True):			
			st.markdown('### I. Percepções iniciais:')
			st.markdown(f"""
			- A métrica MAPE é a que apresenta menor susceptibilidade à presença de outliers:
				- Dados originais: MAPE = {df_result.loc[0,'MAPE']}
				- Maior MAPE = {np.round(df_result.loc[1:,'MAPE'].max(),2)} ({df_result.loc[1:,'Delta_MAPE(%)'].max()})% 
				- Menor MAPE = {np.round(df_result.loc[1:,'MAPE'].min(),2)} ({df_result.loc[1:,'Delta_MAPE(%)'].min()})%
			- A métrica RMSE é a que apresenta maior susceptibilidade à presença de outliers
				- Dados originais: RMSE = {df_result.loc[0,'RMSE']}
				- Maior RMSE = {np.round(df_result.loc[1:,'RMSE'].max(),2)} ({df_result.loc[1:,'Delta_RMSE(%)'].max()})% 
				- Menor RMSE = {np.round(df_result.loc[1:,'RMSE'].min(),2)} ({df_result.loc[1:,'Delta_RMSE(%)'].min()})%			
			""") 
			st.markdown('### II. Observações sobre as métricas:')
			st.markdown("""
			- Ao introduzir um offset nos dados, sem alterar a distribuição dos pontos ou dos outliers, as métricas sofrem pouca alteração.  
			- A quando os dados possuem pouca dispersão e poucos outliers, a métrica MAPE é quase nula (desempenho muito bom do modelo), ao adicionar um pouco de outliers, a métrica quase não sofre alteração, mas após certo limiar, um ocorre uma variação brusca na métrica que se estabiliza quase não alterando o valor ao aumentar a quantidade de outliers.
			- As demais métricas tem uma degradação aproximadamente linear com o aumento da quantidade dos outliers.
			- Uma boa visualização desse comportamento ocorre com a configuração abaixo:
				- Quantidade de pontos: 1000
				- Dispersão dos pontos: 15
				- Quantidade percentual de outliers: 20
				- Padrão de aleatoriedade (seed): 0 
				- Offset dos outliers: 75 
				- Offset dos dados: 200
				
			""")
			
			st.markdown('### III. Normalidade dos resíduos')
			st.markdown("""Em uma versão futura desse estudo irei adicionar a análise de normalidade dos resíduos da regressão linear após a adição dos outliers.
			""")
			
		