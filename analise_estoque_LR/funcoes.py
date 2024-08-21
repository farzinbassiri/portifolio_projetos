# biblioteca de importação de dados
import csv

# bibliotecas de manipulação de arquivos
import os

# Biblioteca para tratamento de dados
from   scipy.signal import argrelextrema # identifica os pontos de minimo e máximo
import holidays                          # identifica os dias úteis
import pandas   as pd
import numpy    as np

# Bibliotecas para visualização dos dados
from matplotlib import pyplot as plt
from termcolor import colored


# Bibliotecas para tratamento estatístico
import statsmodels.api as sm
import scipy.stats     as stats
from scipy.stats import shapiro 

# biblioteca de aprendizado de máquina
from sklearn.linear_model import LinearRegression
from sklearn              import metrics         as mt
from sklearn              import model_selection as ms


# Bibliotecas streamlit
import streamlit as st
import streamlit.components.v1 as component

# biblioteca de funções para análise de dados 

# faz a regressão linear dos dados
def LR(estoque_min, estoque_max, df, data_inicial_projecao, data_final_projecao):
    df_result = pd.DataFrame(columns = ['MAPE', 'Coef', 'Intercept', 'Residuo'])
    forecast_start = estoque_max.tail(1)
    for row in range(0,len(estoque_max)-1):
        df_aux=df.loc[estoque_max.index[row]:estoque_min.index[row],:]
        df_aux.index = (df_aux.index - df_aux.index[0])  / np.timedelta64(1,'D')
        X_train, X_test, y_train, y_test = ms.train_test_split(df_aux.index, df_aux.Estoque, test_size=0.3, random_state=0)
        X_train = X_train.values.reshape(-1, 1)
        y_train = y_train.values.reshape(-1, 1)
        X_test = X_test.values.reshape(-1, 1)
        y_test = y_test.values.reshape(-1, 1)
        
        # Treinamento do algoritmo
        lr_model = LinearRegression()
        lr_model.fit(X_train, y_train)
        
        # Previsão do algoritmo
        y_pred = lr_model.predict(X_test)
    
        #perform Shapiro-Wilk test for normality of residuals
        residual = y_test - y_pred
        if len(residual) > 3:
            residual_p_value = shapiro(residual)
            p_valor = residual_p_value[1]
            # avalia se o p_valor indica resíduos normais 
            if residual_p_value[1] > 0.05:
                normalidade = 'OK'
            else:
                normalidade = 'NOK'
        else:         
            normalidade = 'NOK'
            #st.write('Atenção: erro no teste Shapiro')
            p_valor = 99
        mape = np.round(mt.mean_absolute_percentage_error(y_test, y_pred),2)
        
        result_list = pd.Series(data={'MAPE': mape, 
                                      'Coef':lr_model.coef_[0][0],
                                      'Intercept':lr_model.intercept_[0],
                                      'p-valor': p_valor, 
                                      'Residuo': normalidade})
        
        if len(df_result) == 0:
            df_result = pd.concat([result_list.to_frame().T], ignore_index=True)
        else:
            df_result = pd.concat([df_result, result_list.to_frame().T], ignore_index=True)

    subdata_index = len(estoque_max)-1
    df_test = df.loc[estoque_max.index[subdata_index]:estoque_min.index[subdata_index],:]
    df_test.index = (df_test.index - df_test.index[0])  / np.timedelta64(1,'D')
    
    # calcula os valores médios de COEF e INTERCEPT (ou mediana)
    # lr_model.coef_[0][0] = df_result.Coef.loc[df_result.Residuo == 'OK'].mean()
    # lr_model.intercept_[0] = df_result.Intercept.loc[df_result.Residuo == 'OK'].mean()
    lr_model.coef_[0][0] = df_result.Coef.loc[df_result.Residuo == 'OK'].median()
    lr_model.intercept_[0] = df_result.Intercept.loc[df_result.Residuo == 'OK'].median()

    X_prod = df_test.index.values.reshape(-1, 1)
    y_prod = df_test.values.reshape(-1, 1)
    y_prod = lr_model.predict(X_prod)

    lr_model.intercept_[0] = (df_test.iloc[0].mean() - (y_prod[-1] - df_test.iloc[-1])/2).iloc[0]
    y_prod = lr_model.predict(X_prod)

    lr_model.intercept_[0] = forecast_start.Estoque.iloc[0]

    feriados = holidays.country_holidays("BR", subdiv="SP")
    dias = pd.Series()
    Lista_feriados = feriados[pd.Timestamp(forecast_start.index.values[0]):data_final_projecao]
    dias = pd.bdate_range(start=data_inicial_projecao, end=data_final_projecao, holidays = Lista_feriados, freq='C').values
    
    X_prod_data = dias
    X_prod = ((X_prod_data - data_inicial_projecao)  / np.timedelta64(1,'D')).reshape(-1, 1)
    
    # Previsão do algoritmo
    y_prod = lr_model.predict(X_prod)     

    #return df_result.style.apply(highlight_greaterthan, threshold=0.05, column='p-valor', axis=1), y_prod, X_prod, X_prod_data, lr_model
    return df_result, y_prod, X_prod, X_prod_data, lr_model


# função para dar cor verde/vermelho à visualização de dataframnes em formato de tabelas
def highlight_greaterthan(s, threshold, column):
    is_max = pd.Series(data=False, index=s.index)
    is_max[column] = s.loc[column] >= threshold
    return ['background-color: olivedrab' if is_max.any() else 'background-color: crimson' for v in is_max]

# função que retorna um vetor com numero de dias útes transcorridos.
# entrada: dataframe com timeindex
# saída: vetor com os dias úteis entre os index do df.
def dias_uteis(df):
    feriados = holidays.country_holidays("BR", subdiv="SP")
    data_inicial = 0
    dias = pd.Series()
    for data in df.index:
        if data_inicial !=0:
            Lista_feriados = feriados[data_inicial:data]
            dias[len(dias)] = (len(list(pd.bdate_range(start=data_inicial, end=data, holidays = Lista_feriados, freq='C'))))
        data_inicial = data
    return dias


# detecta os pontos de mínimo e máximo do dataframe
# é usado para identificar os pontos de máximo e mínimo do estoque
def min_max(df):
    n=5
    estoque_min = df.iloc[argrelextrema(df.values, np.less_equal, order=n)[0]]
    estoque_max = df.iloc[argrelextrema(df.values, np.greater_equal, order=n)[0]]
    if estoque_min.index[0] < estoque_max.index[0]:
        estoque_min = estoque_min.drop(estoque_min.index[0])
    if estoque_min.index[-1] < estoque_max.index[-1]:
        estoque_max = estoque_max.drop(estoque_max.index[-1])
    
    return estoque_min, estoque_max

# faz teste de normalidade do resíduo para saber se a LR está bem modelada
def LR_check(df_test, y_prod):
    
    #perform Shapiro-Wilk test for normality of residuals
    residual = df_test - y_prod
    residual_p_value = shapiro(residual)
    # avalia se o p_valor indica resíduos normais 
    if residual_p_value[1] > 0.05:
        normalidade = 'OK'
        st.write('Regressão Linear está bem modelada para esses dados.')
    else:
        normalidade = 'NOK'
        st.write('Regressão Linear NÃO está bem modelada para esses dados.')
    mape = np.round(mt.mean_absolute_percentage_error(y_test, y_pred),2)
    
    return residual_p_value, mape


# faz a projeção do estoque e monta os gráficos
def projecao_estq(produto, df_raw, lead_time, tempo_seguranca):
    erro = 0 # zera flag de erro
    
    dias = 10 # numero de dias de projeção do estoque... vai ser incrementado até chegar em estoque zero ou ter timeout
    df = df_raw.loc[df_raw.Produto == produto, ['Estoque']].copy()
    estoque_min, estoque_max = min_max(df)
    forecast_start = estoque_max.tail(1)

    data_inicial_projecao =  forecast_start.index.values[0]
    data_final_projecao = data_inicial_projecao + pd.DateOffset(dias)
    try:
        df_result, y_prod, X_prod, X_prod_data, lr_model = LR(estoque_min, estoque_max, df, data_inicial_projecao, data_final_projecao)    
    except:
        erro = 'LR: erro'
        return erro, 0, 0, 0
    timeout = 0
    while y_prod[-1][0] > 0:
        timeout += 1
        dias += 2
        data_final_projecao = data_inicial_projecao + pd.DateOffset(dias)
        df_result, y_prod, X_prod, X_prod_data, lr_model = LR(estoque_min, estoque_max, df, data_inicial_projecao, data_final_projecao)    
        if timeout > 180: 
            st.write('Não foi possível fazer a projeção de estoque!')
            st.write('Ponto de estoque nulo não foi encontrado.')
            break

    # imprime resultado para verificação
    aux1 = df.loc[df.index.isin(X_prod_data),:].values.reshape(-1,1)
    aux1 = pd.Series(aux1.reshape((aux1.shape[0],)))
    
    aux2 = y_prod[0:len(aux1)]
    aux2 = pd.Series(aux2.reshape((aux2.shape[0],)))

    data_inicio_real = df.loc[df.index>=X_prod_data[0]].index[0]
    data_final_real = df.loc[df.index>=X_prod_data[0]].index[-1]
    data_inicial_projecao = X_prod_data[0]
    data_final_projecao = X_prod_data[-1]

    # define o ponto de compra vigente
    ponto_compra_atual = pd.DataFrame(columns = ['valor', 'produto'])
    #ponto_compra_atual['produto'] = list(df_raw.Produto.sort_values().unique())
    #ponto_compra_atual['valor'] = [2000, 2500, 800, 500, 800, 200]

    # cria uma coluna com um numero inteiro que representa o tempo transcorrido desde o primeiro dado do dataframe
    df['Delta_tempo'] = (df.index - data_inicio_real)  / np.timedelta64(1,'D')
    
    y_0 = int(np.round(-lr_model.intercept_[0]/lr_model.coef_[0][0],0))
    try:
        y_0_index = np.where(X_prod == y_0)[0][0]
    except:
        try:
            y_0_index = np.where(X_prod == y_0+1)[0][0]
        except:
            new_y_0 = y_0
            count = 0
            while count<5:
                count += 1
                if count == 4:
                    # não deveria ter tantos dias sem expediente... então a reta não deve estar cruzando o zero ainda..
                    st.write('Não ocorre fim de estoque no intervalo de tempo definido.')
                    y_0_index = len(X_prod)-1
                new_y_0 = new_y_0 -1
                
                if new_y_0 == 0:
                    st.write('Zerou y_0 e não achou')
                    break
                else:
                    try:
                        y_0_index = np.where(X_prod == new_y_0)[0][0]
                        break
                    except:
                        pass
    
    y_0 = pd.to_datetime(X_prod_data[y_0_index]) #.strftime("%Y-%m-%d")
    
    # define os parâmetros
    # lead_time = 10
    # tempo_seguranca = 30
    autonomia_estoque = lead_time + tempo_seguranca
    y_1 = y_0 - pd.DateOffset(autonomia_estoque)
    
    
    feriados = holidays.country_holidays("BR", subdiv="SP")
    Lista_feriados = feriados[y_1:y_0]
    periodo = len(list(pd.bdate_range(start=y_1, end= y_0, holidays = Lista_feriados, freq='C')))
    dias = pd.bdate_range(start=y_1, end=y_0, holidays = Lista_feriados, freq='C').values
    X_aux_dias = pd.to_datetime(dias)
    X_aux = ((X_aux_dias - X_prod_data[0])  / np.timedelta64(1,'D')).values.reshape(-1, 1)
    

    fator_arrend = 100
    
    ponto_compra_sugerido = int(np.ceil(lr_model.predict(X_aux)[0][0]/fator_arrend)*fator_arrend)

    valores = np.subtract(list(estoque_max['Estoque'].values), list(estoque_min['Estoque'].values))
    datas = np.subtract(list(estoque_max.index), list(estoque_min.index))

    mtb = dias_uteis(estoque_max)
    consumo_medio_diario = 0
    for row in range(0,len(valores)-1):
        consumo_medio_diario = consumo_medio_diario + (valores[row]/mtb[row])
   
    consumo_medio_diario = int(np.ceil(consumo_medio_diario / (len(valores)-1)))
 
    MTB_compras = 0
    for row in range(0,len(valores)-1):
        MTB_compras += (-datas[row].days)

    
    MTB_compras = int(round(MTB_compras / (len(valores)-1),0))

   
    tempo_fim_estoque_atual = int(round(estoque_max.iloc[-1].iloc[0]/ consumo_medio_diario,0))
    tempo_fim_estoque_atual_dias_corridos = int(round(estoque_max.iloc[-1].iloc[0]/-lr_model.coef_[0][0],0))
    tempo_fim_estoque_novo = int(round(ponto_compra_sugerido / consumo_medio_diario,0))
    tempo_fim_estoque_novo_dias_corridos = int(round(ponto_compra_sugerido / -lr_model.coef_[0][0],0))

    st.markdown('### Análise do nivelamento de estoque: \n\n')

    mape = np.round(mt.mean_absolute_percentage_error(aux1, aux2)*100,1)
    if mape > 15:
        st.markdown('###### Regressão Linear **NÃO** está bem modelada para esses dados.')
        st.markdown('###### Erro Percentual Absoluto Médio (MAPE) está elevado: ' + str(mape) + '%')
        st.markdown('###### Tente novamente alterando o intervalo de início dos dados')
    else:
        st.markdown('- Regressão Linear **está bem** modelada para esses dados.')
        st.markdown('- Erro Percentual Absoluto Médio (MAPE): ' + str(mape) + '%')        

    st.markdown('- Tempo médio entre compras: '+ str(MTB_compras) + ' dias corridos.' )
    st.markdown('- Autonomia média atual do estoque: ' + 
                str(tempo_fim_estoque_atual) + ' dias úteis / ' + 
                str(tempo_fim_estoque_atual_dias_corridos) + 
                ' dias corridos.' )
    
    st.markdown('- Autonomia média sugerida para o estoque: ' + 
                str(tempo_fim_estoque_novo) + ' dias úteis / ' 
                + str(tempo_fim_estoque_novo_dias_corridos) + 
                ' dias corridos.')
    
    st.markdown('- Consumo médio: '+ 
                str(consumo_medio_diario) + 
                ' produtos/dia útil.')
    st.markdown('- Ponto de compra sugerido: ' + str(ponto_compra_sugerido))


# exclui pontos de maximo e mínimo que tiveram mape ruim
    try:
        filter_index = df_result.data.loc[df_result.data.Residuo == 'NOK'].index
    except:
        filter_index = df_result.loc[df_result.Residuo == 'NOK'].index
    # estoque_min_2 = estoque_min.drop(estoque_min.index[filter_index])
    # estoque_max_2 = estoque_max.drop(estoque_max.index[filter_index])   
    estoque_min_2 = estoque_min.loc[estoque_min.index[filter_index],:]
    estoque_max_2 = estoque_max.loc[estoque_max.index[filter_index],:]

    estoque_2 = pd.concat([estoque_min_2, estoque_max_2])
    estoque_2.sort_index(inplace=True)

    min_max_dots = pd.concat([estoque_min, estoque_max])
    min_max_dots.sort_index(inplace=True)
    
# monta os gráficos para visualização dos dados
    fig, ax = plt.subplots(1, 1, figsize=(7, 3)) # 7x5
    ax.plot(df.index, df.Estoque)
    ax.scatter(min_max_dots.index, min_max_dots, color='olivedrab')
    ax.scatter(estoque_2.index, estoque_2, color='crimson')
    ax.plot(X_prod_data,y_prod, color='orange')
    xmin, xmax, ymin, ymax = ax.axis()
    # ax.hlines(ponto_compra_atual.loc[ponto_compra_atual.produto==produto,'valor'].iloc[0], xmin, xmax, colors='gray', linestyles='dashed')
    ax.hlines(ponto_compra_sugerido, xmin, xmax, colors='black', linestyles='dashed')
    
    ax.grid(color='gray', linestyle='-', linewidth=0.1) 
    ax.set_ylabel('Nível de Estoque', fontsize= 9)
    ax.set_xlabel('Data', fontsize= 7)
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=7)
    ax.set_title('Projeção do Nível de Estoque: ' + produto)

    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])
    
    # Put a legend below current axis
    ax.legend(['Dados reais', 
               'Trecho aprovado: resíduo aleatório',
               'Trecho rejeitado: resíduo não aleatório',
               'Dados Projetados',
               'Ponto de Compra Sugerido'],
                 fontsize=8, loc='upper center', 
                 bbox_to_anchor=(0.5, -0.25),
                 fancybox=True, shadow=True, ncol=2)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    print()

    fig, ax = plt.subplots(1, 1, figsize=(7, 3)) # 7x5
    ax.plot(df.loc[df.index>=X_prod_data[0]].index, df.loc[df.index>=X_prod_data[0],'Estoque'],'-o')
    ax.plot(X_prod_data,y_prod, color='orange')  
    ax.grid(color='gray', linestyle='-', linewidth=0.1) 
    
    ax.set_ylabel('Nível de Estoque', fontsize= 9)
    ax.set_xlabel('Data', fontsize= 7)
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=7)
    ax.set_title('Zoom dados mais recentes')
    ax.legend(['Dados reais', 'Dados Projetados'], fontsize=9, loc='best')

    # Put a legend below current axis
    ax.legend(['Dados reais', 'Dados Projetados'],
                 fontsize=8, loc='upper center', 
                 bbox_to_anchor=(0.5, -0.25),
                 fancybox=True, shadow=True, ncol=2)

    # coloca os valores da LR - ver posição xy automatica
    posicao = ax.get_yticks()
    
    
    ax.annotate('Coef: ' + str(round(lr_model.coef_[0][0],2)), (X_prod_data[0],posicao[2]), fontsize=8)
    ax.annotate('Intercept: ' + str(round(lr_model.intercept_[0],2)), (X_prod_data[0],posicao[1]), fontsize=8)
    plt.tight_layout()


    st.pyplot(fig, use_container_width=True)
    #st.divider()
    # st.markdown('##### Tabela com resultados das regressões lineares para cada trecho dos dados.')
    # st.dataframe(df_result, use_container_width=True, hide_index=True)

    #df_result = df_result.data
    return erro, estoque_min, estoque_max, df_result

def detecta_demanda(df, df_result, produto, estoque_min, estoque_max,):
    df = df.loc[df.Produto==produto, :]
    try:
        df_result = df_result.data
    except:
        pass
    # cria a derivada do coef para estudo de variação de demanda
    #df_result['Coef_diff']= df_result.Coef.diff().abs()
    # elimina o primeiro calculado pois sempre será grande
    #coef_table_max = estoque_max.iloc[df_result.loc[filtro, 'Coef_diff'].index,:]
    #coef_table_min = estoque_min.iloc[df_result.loc[filtro, 'Coef_diff'].index,:]

    #st.dataframe(coef_table_max)
    #return coef_table_max, coef_table_min, df_result.loc[filtro, ['Coef_diff', 'Coef', 'Intercept', 'Residuo']]
    return df_result.loc[:, ['Coef', 'Residuo']]







    

