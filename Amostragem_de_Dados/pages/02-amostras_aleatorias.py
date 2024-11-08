
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

# Arquivos de entrada
try: #caminho para Streamlit
    df_raw = pd.read_csv('Amostragem_de_Dados/Dataset/trackLog_civic_dados_limpos.csv', delimiter=';', low_memory=False, usecols=[1,2,3,4,5,6])
except: #caminho para uso local
    df_raw = pd.read_csv('Dataset\\trackLog_civic_dados_limpos.csv', delimiter=';', low_memory=False, usecols=[1,2,3,4,5,6])


df_raw= df_raw.convert_dtypes()

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
st.subheader('Parte II - Amostras aleatoriamente distribuidas')

st.markdown("""___""")
st.sidebar.markdown('## Classificação e predição da posição da alavanca do câmbio durante uso do veículo.')
#Carrega o logo 
try: #caminho para Streamlit
    image = Image.open('Amostragem_de_Dados/logo_cambio.jpg')
except: #caminho para uso local
    image = Image.open('logo_cambio.jpg')
st.sidebar.image(image, width=240)

st.sidebar.markdown("""___""")

# permite que o usuário escolha o parâmetro k para ver como ele influencia o resultado
st.sidebar.markdown('### Configuração dos parâmetros para o modelo:')
st.sidebar.markdown('#### Parâmetro k - número de vizinhos mais próximos:')
k_auto = st.sidebar.checkbox('Escolher automaticamente o valor de k?', value=True)
    
# cria a lista de valores para o usuário escolher e coloca em uma lista de escolha única
k_list = np.arange(1, 16, 1)
k_user = st.sidebar.selectbox(
                        'Selecione o valor de k que deseja utilizar:',
                        k_list,
						disabled = k_auto)

k_max = st.sidebar.slider(
    'Defina a o valor máximo de k para o método de Elbow:',
    1,
    16,
    value = 5,
    disabled = False)

st.sidebar.markdown("""___""")
st.sidebar.markdown('### Configuração da proporção de amostras destinadas ao treino do modelo:')
st.sidebar.markdown('#### Proporção entre os dados para produção e treinamento do modelo:')
# permite que o usuário escolha tamanho das amostras de treino, teste e validação para ver como eles influenciam o resultado
train_range_auto = st.sidebar.checkbox('Escolher automaticamente.', value=True)

tam1_amostras_slider = st.sidebar.slider(
	'Defina tamanho da amostras para Treino-Validação-Teste do modelo[% dos dados]:',
	0.5,
	80.0,
	step=0.5,
	value = 4.5,
	disabled = train_range_auto)/100

tam2_amostras_slider = st.sidebar.slider(
	'Defina a proporção entre dados de Treino e Validação/Teste [% das amostras]:',
	0.5,
	80.0,
	step=0.5,
	value = 20.0,
	disabled = train_range_auto)/100

if train_range_auto:
	tam1_amostras_slider = 0.045 #define percentual de dados que serão separados para treino-validação-teste
	tam2_amostras_slider = 0.2  #define proporção dos dados separados que serão utilizados para treinamento, o restante será dividido igualmente entre validação e teste



#coloca o objeto LinkedIn na barra lateral
with st.sidebar:
    components.html(embed_component['linkedin'], height = 310)

st.sidebar.markdown("""___""")
st.sidebar.markdown('###### Imagem câmbio: https://www.vectorstock.com/royalty-free-vector/manual-gearshift-icon-car-and-transmission-vector-5518279')	
	
	
st.sidebar.markdown("""___""")
st.sidebar.markdown('###### Powered by Farzin Bassiri')


#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
#                                Tratamento dos dados
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
# a relação entre RPM do motor e a velocidade do carro é bem determinada, uma vez que o carro é dotado de câmbio manual.
# nas trocas de marcha, é esperado que ocorram variações aleatórias dessa relação devido ao escorregamento da embreagem.
    # esses dados foram eliminados da base de dados durante a fase de data wrangling.

features_list =['Engine RPM', 'Speed (OBD)(km/h)', 'Fuel flow(l/h)']

label_list = 'Marcha_Train2'

# monta os dados de classificação
X_raw = df_raw.loc[:,features_list]
# ".values" foi adicionado para fazer o y_train ser um array, assim fica compatível com o y_pred a ser gerado...
label_true = df_raw.loc[:, label_list]
    
#separa os dados de treino, teste e validação
X_prod, X, label_prod, label = ms.train_test_split(X_raw, label_true, test_size=tam1_amostras_slider, random_state=0)
X_train, X_test, label_train, label_test = ms.train_test_split(X, label, test_size=tam2_amostras_slider, random_state=0)
X_test, X_val, label_test, label_val   = ms.train_test_split(X_test, label_test, test_size=0.5, random_state=0)

#monta os dataframes de teste e produção
df_pred = pd.DataFrame(label_test, columns = ['Label'])

df_prod = df_raw.copy()
df_prod['Marcha_Train2'] = label_true


# calcula tamanho das amostras para exibição posterior
num_rows_m2_train = X_train.shape[0]
num_rows_m2_val   = X_val.shape[0]
num_rows_m2_test  = X_test.shape[0]
num_rows_m2_prod  = X_raw.shape[0]
pop_model2 = df_raw.shape[0]


# definição dos parâmetros do treinamento
values = [k for k in range(1,k_max+1)]
if k_auto:
	
	val_score = list()

	for k in values:
		model_train = KNeighborsClassifier(n_neighbors = k)
		model_train.fit(X_train, label_train)

		# classificação sobre o teste
		label_hat_val = model_train.predict(X_val)
		acc_val = mt.accuracy_score(label_val, label_hat_val)
		val_score.append(acc_val)

	# escolhe o k-valor (nro de vizinhos) que gera a maior acurácia
	k = val_score.index( max( val_score ) ) + 1
else:
	k = k_user

# retreino com o parâmetro escolhido
model_train = KNeighborsClassifier(n_neighbors = k)
model_train.fit(X_train, label_train)

# previsão sobre os dados de validação (inéditos ao modelo) para verificação do ajuste do modelo
label_hat_val = model_train.predict(X_val)
acc_val_model2 = mt.accuracy_score(label_val, label_hat_val)
#val_score.append(acc_val)

# modelo re-treinado com dados de validação
model_prod = KNeighborsClassifier(n_neighbors = k)
model_prod.fit(X_val,label_val)

# classificação sobre os dados de teste (inéditos aos modelo)
label_hat_test = model_prod.predict(X_test)

# Medição da performance do modelo com os dados de teste:
df_pred['predicted'] = label_hat_test
acc_test_model2 = mt.accuracy_score(label_test, label_hat_test)

# classificação sobre os dados de produção
label_hat_prod = model_prod.predict(X_raw)
df_prod['Marcha Pred'] = label_hat_prod

# Cálculo da acurácia com os dados de procução
acc_prod_model2 = mt.accuracy_score(label_true, label_hat_prod)
# calcuma a matriz confusão:
cf_matrix = mt.confusion_matrix(label_true, label_hat_prod)


# cálculo dos pontos que foram preditos com erro:
df_erro = pd.DataFrame()
for marcha in range(1,6):
    filtro = (df_prod['Marcha Pred']!=marcha) & (df_prod['Marcha_Train2']==marcha)
    erro = df_prod.loc[filtro,:]
    df_erro = pd.concat([erro, df_erro])

# calcula o numero de ocorrencias de cada combinação de predição incorreta
for marcha_real in range(1,6):
    for marcha_pred in range(1,6):
        filtro = (df_erro['Marcha_Train2'] == marcha_real) & (df_erro['Marcha Pred'] == marcha_pred)
        #print(filtro.head())
        df_erro.loc[filtro,'Ocorrencias'] = df_erro.loc[filtro,'Marcha_Train2'].count()
    
# guarda os dados para resumo posterior
erros_model2 = df_erro.shape[0]
pop_model2 = df_raw.shape[0]


		
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
#                                Mostrando os resultados
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------	

#criando abas
tab1, tab2 = st.tabs(['Parte II - Amostras Aleatórias', '-'])

with tab1:
	with st.container():
		with st.expander("Resumo Geral:", expanded=True):
			st.write(' - Quantidade de dados para treino do modelo: '+str(num_rows_m2_train) + ' (' + str(np.round((num_rows_m2_train/(num_rows_m2_train+num_rows_m2_test+num_rows_m2_val))*100,0))+'% das amostras Treino-Validação-Teste)')	
			st.write(' - Quantidade de dados para validação do modelo: '+str(num_rows_m2_val) + ' (' + str(np.round((num_rows_m2_val/(num_rows_m2_train+num_rows_m2_test+num_rows_m2_val))*100,0))+'% das amostras Treino-Validação-Teste)')	
			st.write(' - Quantidade de dados para teste do modelo: '+str(num_rows_m2_test) + ' (' + str(np.round((num_rows_m2_test/(num_rows_m2_train+num_rows_m2_test+num_rows_m2_val))*100,0))+'% das amostras Treino-Validação-Teste)')	
			st.write(' - Quantidade de dados para produção: '+str(num_rows_m2_prod))	
					 					
		with st.expander("Resultado obtido:"):
			st.write('Acurácia sobre dados de teste: ' + str(np.round(acc_test_model2,4)))
			st.write('Acurácia sobre produção: ' + str(np.round(acc_prod_model2,4)))

		with st.expander("Comentário:"):
			st.write('O modelo foi capaz de fazer uma boa generalização dos dados quando esses estavam "longe" das amostras usadas para a Estratégia Treino-Validação-Teste')
			

	with st.container():
		# monta o gráfico de velocidade x RPM do motor usando os dados de treinamento.

		fig, ax = plt.subplots(2, 1, figsize=(10, 7))
		#fig.suptitle('Visualização rápida do Dataset x Dados de Treino, Validação e Teste')
		#ax[0].text(1000, 120, 'Dados de treinamento distribuidos ao longo do dataset', color='dimgray', fontsize=11)

		#loop feito em ordem reversa para alinhar a ordem da legenda com o gráfico, assim fica mais intuitiva a leitura
		# cria o gráfico separando cada marcha em uma cor diferente.
		for marcha in range(5,0, -1):
			# faz o filtro separando as marchas
			filtro = label_true==marcha

			# cria o primeiro gráfico mostrando os dados do dataset, onde cada cor é uma das marchas
			ax[0].scatter(X_raw.loc[filtro,'Engine RPM'],X_raw.loc[filtro,'Speed (OBD)(km/h)'], 5)
			ax[0].set_title('Visualização rápida do Dataset')
			ax[0].set_xlabel('Velocidade do motor [RPM]')
			ax[0].set_ylabel('Velocidade do carro [km/h]')

			# cria o segundo gráfico mostrando os dados de treinamento, onde cada cor é uma das marchas
			ax[1].scatter(X_train.loc[filtro,'Engine RPM'],X_train.loc[filtro,'Speed (OBD)(km/h)'], 5)
			ax[1].set_title('Visualização rápida dos Dados de Treino, Validação e Teste')
			ax[1].set_xlabel('Velocidade do motor [RPM]')
			ax[1].set_ylabel('Velocidade do carro [km/h]')

		#configura o grid dos gráficos        
		ax[0].axes.grid(color='b', linestyle='-', linewidth=0.1)    
		ax[1].axes.grid(color='b', linestyle='-', linewidth=0.1)   

		# padroniza a escala
		start = min(ax[0].get_ylim()[0], ax[1].get_ylim()[0])
		end = max(ax[0].get_ylim()[1], ax[1].get_ylim()[1])

		ax[0].yaxis.set_ticks(np.arange(0, end, 20))
		ax[0].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))

		ax[1].yaxis.set_ticks(np.arange(0, end, 20))
		ax[1].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))

		start = min(ax[0].get_xlim()[0], ax[1].get_xlim()[0])
		end = max(ax[0].get_xlim()[1], ax[1].get_xlim()[1])

		ax[0].xaxis.set_ticks(np.arange(0, end, 500))
		ax[0].xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))

		ax[1].xaxis.set_ticks(np.arange(0, end, 500))
		ax[1].xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))

		# cria a legenda nos gráficos
		ax[0].legend(['5ª marcha','4ª marcha','3ª marcha','2ª marcha','1ª marcha'], fontsize=9, loc='upper left')
		ax[1].legend(['5ª marcha','4ª marcha','3ª marcha','2ª marcha','1ª marcha'], fontsize=9, loc='upper left')

		plt.tight_layout()		
		st.pyplot(fig, use_container_width=True)		
			
	with st.container():
		## plot of train and test scores vs tree depth
		if k_auto:
			st.markdown('#### Escolha do parâmetro K - Melhor resultado: ' + str(k))
			fig=plt.figure(figsize=(8,4))
			plt.plot( values, val_score, '-o', label='Validação' )

			plt.title('Determinação do ponto ótimo de configuração do algoritmo: Elbow Method')
			plt.xlabel('Valor do parâmetro "k - n_neighbors"')
			plt.ylabel('Acurácia')  
			plt.grid(color='b', linestyle='-', linewidth=0.1)   
			# coloca anotação
			xmin, xmax, ymin, ymax = plt.axis()
			x_annot = k
			plt.annotate("Valor escolhido", 
						 xy=(x_annot, (1-(ymax-ymin)/12)*ymax),
						 xytext=(x_annot, (1-(ymax-ymin)/3)*ymax), 
						 ha='center',
						 arrowprops=dict(facecolor='black', shrink=0.05))

			#specify axis tick step sizes
			plt.xticks(np.arange(1, k_max+1, 1))
			plt.xlim(0.5, k_max+0.5)
			st.pyplot(fig, use_container_width=True)	
		else:
			st.markdown('#### Parâmetro K definido pelo usuário: ' + str(k))

			
	
	with st.container():
		col1, col2 = st.columns(2, gap="large")
		with col1:
			# cria o gráfico da matriz confusão:
			fig = plt.figure(figsize=(5,5))
			#sns.heatmap(cf_matrix/np.sum(cf_matrix), annot=True, fmt='.2%', cmap='Blues')
			group_counts = ["{0:0.0f}".format(value) for value in cf_matrix.flatten()]
			group_percentages = ["{0:.2%}".format(value) for value in cf_matrix.flatten()/np.sum(cf_matrix)]
			labels = [f"{v1}\n{v2}" for v1, v2 in zip(group_counts,group_percentages)]
			labels = np.asarray(labels).reshape(5,5)
			sns.heatmap(cf_matrix, annot=labels, fmt='', cmap='Blues')
			plt.title('Matriz Confusão dos dados de Teste - Acurácia de ' + str(np.round(acc_test_model2,4)))
			plt.xlabel('Dados Preditos')
			plt.ylabel('Dados Reais')  
			st.pyplot(fig, use_container_width=True)			
			
		with col2:
			fig = px.scatter(df_erro, x='Marcha_Train2', y='Marcha Pred', size = 'Ocorrencias', color='Marcha_Train2',
							 hover_data={'Marcha_Train2':False,
										'Marcha Pred':False,
										'Ocorrencias':True})

			# configura o título do gráfico
				# title_x == 0.5 --> alinhamento central;  
				# Se < 0.5 --> desloca à esquerda
				# Se > 0.5 --> desloca à direita
			fig.update_layout(title_text=(f'Erro de predição com dados de produção: {df_erro.shape[0]} em {df_raw.shape[0]} pontos'), title_x=0.01, title_font = {"size": 20}) 
			fig.update_layout(width = 700, height=700) 

			fig.add_annotation(x=2, y=5.5,
							  text=(f'Acurácia em produção: {acc_prod_model2:.4f}'),
							  showarrow=False,
							  yshift=10,
							  font=dict(
								 family="Calibri, monospace",
								 size=18,
								 color="#000000"),
							  align="center")

			fig.update_layout(
							 hoverlabel=dict(
								 bgcolor="white",
								 font_size=14,
								 font_family="Calibri, monospace"))

			# configura os títulos dos eixos
			fig.update_xaxes(
							tickangle = 0,
							title_text = "Marcha Real [1 a 5]",
							title_font = {"size": 18, "color":"#000000"},
							ticklabelstep=1,
							showgrid=True)

			fig.update_yaxes(
							title_text = 'Marcha Predita [1 a 5]',
							title_font = {"size": 18, "color":"#000000"},
							range=[1, df_erro['Marcha Pred'].max()+1],
							showgrid=True)

			fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
			fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True)

			st.plotly_chart(fig, use_conteiner_width = True) 				
			
			

#fig.update_layout(title_text=(f'Erro de predição: {erros_model2} em {pop_model2} pontos'), title_x=0.5, title_font = {"size": 18}) 
	with st.container():
		# using the variable axs for multiple Axes
		fig, ax = plt.subplots(1, 1, figsize=(10, 5))
		fig.suptitle('Visualização dos dados Preditos')


		#loop feito em ordem reversa para alinhar a ordem da legenda com o gráfico, assim fica mais intuitiva a leitura
		# cria linhas em cores diferentes para cada posição do câmbio (marcha)
		for marcha in range(5,0, -1):
			# faz o filtro separando as marchas
			filtro = label_hat_prod==marcha

			# cria o primeiro gráfico mostrando a relação das marchas (velocidade x RPM do motor)
			plt.scatter(X_raw.loc[filtro,'Engine RPM'],X_raw.loc[filtro,'Speed (OBD)(km/h)'], 5)
			plt.xlabel('Velocidade do motor [RPM]')
			plt.ylabel('Velocidade do carro [km/h]')

		plt.grid(color='b', linestyle='-', linewidth=0.1)    


		#start, end = ax[0].get_ylim()
		#ax[0].yaxis.set_ticks(np.arange(0, end, 20))
		#ax[0].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))

		plt.legend(['5ª marcha','4ª marcha','3ª marcha','2ª marcha','1ª marcha'], fontsize=9, loc='upper left')
		plt.text(1000, 125, 'Erro de predição: cada reta representa uma marcha, \nlogo deveria haver apenas uma cor por reta.', color='dimgray', fontsize=11)

		plt.tight_layout()
		st.pyplot(fig, use_container_width=True)
		
	with st.container():
		# using the variable axs for multiple Axes

		fig, ax = plt.subplots(3, 2, figsize=(11, 8))
		plt.xlabel('RPM do motor')
		plt.ylabel('Velocidade [km/h]')
		plt.grid(color='b', linestyle='-', linewidth=0.1)  


		fig.suptitle('Clusters (marchas) isolados - Melhor visualização dos erros de predição')
		ax[0,0].scatter(X_raw.loc[label_hat_prod==1,'Engine RPM'],X_raw.loc[label_hat_prod==1,'Speed (OBD)(km/h)'], 5, color='darkorange')
		ax[0,0].set_title('Marcha = 1')
		ax[0,0].grid(color='b', linestyle='-', linewidth=0.1)  

		ax[1,0].scatter(X_raw.loc[label_hat_prod==2,'Engine RPM'],X_raw.loc[label_hat_prod==2,'Speed (OBD)(km/h)'], 5, color='forestgreen')
		ax[1,0].set_title('Marcha = 2')
		ax[1,0].grid(color='b', linestyle='-', linewidth=0.1)  

		ax[2,0].scatter(X_raw.loc[label_hat_prod==3,'Engine RPM'],X_raw.loc[label_hat_prod==3,'Speed (OBD)(km/h)'], 5, color='crimson')
		ax[2,0].set_title('Marcha = 3')
		ax[2,0].grid(color='b', linestyle='-', linewidth=0.1)  

		ax[0,1].scatter(X_raw.loc[label_hat_prod==4,'Engine RPM'],X_raw.loc[label_hat_prod==4,'Speed (OBD)(km/h)'], 5, color='mediumpurple')
		ax[0,1].set_title('Marcha = 4')
		ax[0,1].grid(color='b', linestyle='-', linewidth=0.1)  

		ax[1,1].scatter(X_raw.loc[label_hat_prod==5,'Engine RPM'],X_raw.loc[label_hat_prod==5,'Speed (OBD)(km/h)'], 5, color='saddlebrown')
		ax[1,1].set_title('Marcha = 5')
		ax[1,1].grid(color='b', linestyle='-', linewidth=0.1)  

		for i in range(0,6):
			ax[2,1].scatter(X_raw.loc[label_hat_prod==i,'Engine RPM'],X_raw.loc[label_hat_prod==i,'Speed (OBD)(km/h)'], 5)


		# padroniza a escala
		start = min(ax[0,0].get_ylim()[0], ax[1,0].get_ylim()[0], ax[2,0].get_ylim()[0], ax[0,1].get_ylim()[0], ax[1,1].get_ylim()[0])
		end   = max(ax[0,0].get_ylim()[1], ax[1,0].get_ylim()[1], ax[2,0].get_ylim()[0], ax[0,1].get_ylim()[1], ax[1,1].get_ylim()[1])

		ax[0,0].yaxis.set_ticks(np.arange(0, end, 20))
		ax[0,0].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))

		ax[1,0].yaxis.set_ticks(np.arange(0, end, 20))
		ax[1,0].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))

		ax[2,0].yaxis.set_ticks(np.arange(0, end, 20))
		ax[2,0].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))

		ax[0,1].yaxis.set_ticks(np.arange(0, end, 20))
		ax[0,1].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))

		ax[1,1].yaxis.set_ticks(np.arange(0, end, 20))
		ax[1,1].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))


		start = min(ax[0,0].get_xlim()[0], ax[1,0].get_xlim()[0], ax[2,0].get_xlim()[0], ax[0,1].get_xlim()[0], ax[1,1].get_xlim()[0])
		end   = max(ax[0,0].get_xlim()[1], ax[1,0].get_xlim()[1], ax[2,0].get_xlim()[1], ax[0,1].get_xlim()[1], ax[1,1].get_xlim()[1])

		ax[0,0].xaxis.set_ticks(np.arange(0, end, 500))
		ax[0,0].xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))

		ax[1,0].xaxis.set_ticks(np.arange(0, end, 500))
		ax[1,0].xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))

		ax[2,0].xaxis.set_ticks(np.arange(0, end, 500))
		ax[2,0].xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))

		ax[0,1].xaxis.set_ticks(np.arange(0, end, 500))
		ax[0,1].xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))

		ax[1,1].xaxis.set_ticks(np.arange(0, end, 500))
		ax[1,1].xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))


		ax[2,1].set_title('Todas juntas')
		ax[2,1].legend(['5ª marcha','4ª marcha','3ª marcha','2ª marcha','1ª marcha'], fontsize=9, loc='upper left')

		plt.tight_layout()		
		st.pyplot(fig, use_container_width=True)

