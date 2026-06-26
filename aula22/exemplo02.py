# Bibliotecas
import os
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

# Limpeza do terminal
os.system('cls')

# estrutura for para cada região
# Obtenção dos dados dos estudos e Preparação dos dados
try:
    print('Obtendo os dados...')
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    # utf-8, iso-8859-1, latin1, cp1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep= ';', encoding= 'iso-8859-1')

    # Filtro por ano: 2025 e 2026
    df_ocorrencias = df_ocorrencias[df_ocorrencias['ano'].isin([2025, 2026])]

    # Por região: Baixada Fluminense
    df_ocorrencias = df_ocorrencias[df_ocorrencias['regiao'] == 'Baixada Fluminense']
    
    # conferencia dos dados obtidos
    #print(df_ocorrencias.head())

    # delimitando as variáveis
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]
    
    # Checando o dataframe delimitado
    #print(df_roubo_veiculo.head(50))

    # Agrupando e Totalizando os roubos por municipios
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum( ) # as_index=False para retornar com os números de indices

    # Organizando por ordem decrescente
    df_roubo_veiculo = df_roubo_veiculo.sort_values(by='roubo_veiculo', ascending=False)

    # Checando o agrupamento por cidade
    #print(df_roubo_veiculo.head(25))

except Exception as e:
    print(f'Erro ao obter dados {e}')

# Obtendo as medidas
try:
    print('Calculando as medidas... ')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo']) # array é uma estrutura do numpy com ganho computacional

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    distancia = abs((media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo * 100) # abs é para obtermos o valor absoluto

    # Verificando as medidas estatísticas
    print('\nMedidas de Tendência Central ')
    print(50*"=")
    print(f'Média: {media_roubo_veiculo:.2f}')
    print(f'Mediana: {mediana_roubo_veiculo:.2f}')
    print(f'Distância: {distancia:.2f}%')
    # quando for de 0 a 10% = tendencia a serem dados simetricos (dados menos dispersos)  - dados considerados homogeneos 
    # quando for de 10 a 25% = tendencia a ter uma assimetria moderada (a distribuição pode estar sendo influenciada por valores extremos gerando dispersão) 
    # quando for acima de 25% = tendencia de assimetria forte - dados heterogeneos
    
except Exception as e:
    print(f'Erro ao processar as medidas: {e}')

#Obtendo a distribuição
try:
    array_roubo_veiculo    
    quartil_inferior = np.quantile(array_roubo_veiculo, 0.25)    
    quartil_superior = np.quantile(array_roubo_veiculo, 0.75)

    # Verificando os quartis
    print('\nQuartis ')
    print(50*"=")
    print(f'Quartil inferior: {quartil_inferior:.2f}') # representa os 25% menores com até 47.25 roubos
    print(f'Mediana: {mediana_roubo_veiculo:.2f}')
    print(f'Quartil superior: {quartil_superior:.2f}') # representando 75% das cidades do estado tiveram menos que 1016.75

    # Encontrando os municípios com menos roubos
    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < quartil_inferior]

    # Encontrando os municípios com menos roubos
    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > quartil_superior] 

    # print('\nMunicípios com menos casos de roubos: ')
    # print(50 * '=')
    # print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))

    # print('\nMunicípios com maiores casos de roubos: ')
    # print(50 * '=')
    # print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False)) # ja esta ordenado na sintaxe acima na linha 40

except Exception as e:
    print(f'Erro ao obter a distribuição: {e}')

    # Obtendo as Medidas de Posição 
try:
    # Amplitude total => amplitude = (máximo - mínimo) 
    # Resultado: mais próximo do mínimo, baixa dispersão (dados mais homogeneos)
    # Resultado: Zero, quer dizer que todos os dados são iguais
    # Resultado: mais próximo do máximo, alta variabilidade ou dispersão

    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo    

    print('\nMedidas de Posição ')
        
    print(f'Máximo: {maximo}')
    print(f'Mínimo: {minimo}')
    print(f'Amplitude Total: {amplitude}') 

except Exception as e:
    print(f'Erro ao calcular medidas de posição: {e}')

    # Calculando os outliers, medidas de dispersão
try:
    # IQR (INTERVALO INTERQUARTIL) => é a amplitude dos 50% dos dados mais centrais
    # IQR = q4 - q1
    # Ele ignora os valores extremos. Max e Min estão fora do IQR
    # Não sofre interferência dos valores extremos
    # Quanto mais próximo do Q1, mais homogeneos são os dados 
    # Quanto mais próximo do Q3, mais heterogeneos são os dados 

    iqr = quartil_superior - quartil_inferior

    # Limite Inferior
    # É uma medida que vai identificar os outliers, os valores abaixo do que o limite inferior
    limite_inferior = quartil_inferior - (1.5 * iqr)

    # Limite Superior
    # É uma medida que vai identificar os outliers, os valores maiores do que o limite superior
    limite_superior = quartil_superior + (1.5 * iqr)

    print('\nMedidas de Dispersão ')
    print(50*"=")
    print(f'IQR: {iqr}')
    print(f'Limite Inferior: {limite_inferior}')
    print(f'Limite Superior: {limite_superior}') 

except Exception as e:
    print(f'Erro ao calcular as medidas de dispersão: {e}')

    #Calculando os Outliers
try:
    # Outliers Superiores
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]    

    # Outliers Inferiores
    df_roubo_veiculo_outliers_inferiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]

    # Exibindo os Outliers
    print('\nMunicípios com Outliers Inferiores: ')
    print(50 * '=')
    if len(df_roubo_veiculo_outliers_inferiores) == 0:
        print('Não existem Outliers inferiores')
    else:
        print(df_roubo_veiculo_outliers_inferiores.sort_values(by= 'roubo_veiculo', ascending=True))

    print('\nMunicípios com Outliers Superiores: ')
    print(50 * '=')
    print(df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))
    
except Exception as e:
    print(f'Erro ao calcular os Outliers: {e}')

    # Assimetria e Curtose
try:
    print('\nCalculando a assimetria...')
    # Assimetria
    # Indica como os dados estão distribuidos em torno de um valor central.
    # Usada para descrever o grau de assimetria de uma distribuição.
    # Os valores estão equilibrados?
    # Existe uma maior quantidade de observações de registros maiores ou menores?
    # O peso da distribuição está mais para qual lado? "p/ os mais baixos ou mais altos"

    # Interpretação:
    # Resultado da Assimetria > 1 => Assimetria Positiva Alta, Calda Longa à direita, existem valores muito alto puxando para cima, a tendência de que a média seja muito maior que a mediana.
    
    # Resultado da Assimetria entre 0.5 e 1 => Assimetria Positiva Moderada, Calda à direita, existem valores altos puxando a média para cima, mas é menos acentuada, a tendência de que a média seja maior que a mediana.

    # Resultado da Assimetria entre -0.5 e +0.5 => Distribuição aproximadamente simétrica, os dados estão equilibrados em torno da média, a tendência que a média seja muito próxima da mediana

    # Resultado da Assimetria entre -0.5 e -1 => Assimetria Negativa Moderada, Calda à esquerda, existem valores baixos puxando a média para baixo, mas é menos acentuada, a tendência de que a média seja menor que a mediana.

    # Resultado da Assimetria < 1 => Assimetria Negativa Alta, Calda Longa à esquerda, existem valores muito baixos puxando para baixo, a tendência de que a média seja muito menor que a mediana.

    # Calcular através do Pandas
    assimetria = df_roubo_veiculo['roubo_veiculo'].skew()

    # Curtose:
    # Medida que descreve o formato da distribuição
    # Nos ajuda a entender se os valores estão espalhados ou mais próximos da média.
    # Ajuda a entender se existem outliers.

    # Interpretação:
    # Curtose Alta, geralmente temos muitos valores distribuidos em torno da média e alguns outros muito distantes dela.
    # Curtose Baixa, os dados tendem a estar distribuidos ao longo do conjunto.

    # Interpretação segundo Fisher
    # Resultado da Curtose = 0 (Mesocúrtica), distribuição normal, concentração dos dados moderada no centro, Outliers são raros.

    # Resultado da Curtose < 1 (Platicúrtica), pico achatado, dados mais afastados 'espalhados', poucos extremos "Mas podem haver outliers"

    # Resultado da Curtose > 1 (Leptocúrtica), pico mais alto, muitos valores próximos à média, Outliers mais comuns e mais fortes, caldas mais pesadas. 

    # Calcular através do Pandas para a interpretação de Fisher, na biblioteca Sunspy segue a interpretação de Pearson (padrão 3)

    curtose = df_roubo_veiculo['roubo_veiculo'].kurtosis()

    print('\nMedidas de Distribuição: ')
    print(50 * '=')
    print(f'Assimetria: {assimetria:.2f}')
    print(f'Curtose: {curtose:.2f}')

except Exception as e:
    print(f'Erro ao calcular a assimetria e/ou curtose: {e}')

    # Variabilidade
try:
    print('\nCalculando a variabilidade dos dados...')
    # Varância => é uma medida para verificar a dispersão dos dados.
    # Observa-se em relação a média.
    # É a média dos quadrados das diferenças entre cada valor e média.
    # Observação: o resultado da variância está elevado ao quadrado.

    # Interpretação:
    # Quanto maior a variância, maior o afastamento dos valores em relação a média, indicando alta dispersão.
    
    variancia = np.var(array_roubo_veiculo)

    # Distância entre a Média e a Variância
    # Até 10% -> Baixa dispersão em relação a média,
    # Entre 10% e 25% -> Dispersão moderada em relação a média,
    # Acima de 25% -> Alta dispersão em relação a média,
    
    distancia_var_media = (variancia / (media_roubo_veiculo ** 2)) *100

    # Desvio Padrão
    # É a raiz quadrada da variância.
    # É a normalização da variância.
    # Apresenta o quanto os dados podem estar afastados em relação a média (tanto para mais, quanto para menos)

    desvio_padrao = np.std(array_roubo_veiculo)

    # Coeficiente de Variação
    # É a magnitude(mensuração) do desvio padrão em relação a média

    coeficiente_variacao = desvio_padrao / media_roubo_veiculo * 100

    print('\nMedidas de Variabilidade: ')
    print(50 * '=')
    print(f'Variância: {variancia:.2f}')
    print(f'Distância entre Variância e a Média: {distancia_var_media:.2f}%') 
    print(f'Desvio Padrão: {desvio_padrao:.2f}') 
    print(f'Coeficiente de Variação: {coeficiente_variacao:.2f}%') 
        
except Exception as e:
    print(f'Erro ao calcular as medidas de variabilidade: {e}')

# Visualizando o Boxplot
try:
    print('\nVisualizando os dados...')
    plt.subplots(2, 2, figsize=(18, 10))
    plt.suptitle('Roubo de Veículos por Município', fontsize=16, fontweight='bold', color='blue')
    plt.subplots_adjust(
    wspace=0.5, #wspace = espaço horizontal.
    hspace=0.4  #hspace = espaço vertical.
    )    
    #plt.tight_layout()

    # POSIÇÃO 1: BOXPLOT
    plt.subplot(2, 2, 1) # 2 linhas e 2 colunas para a área 1
    plt.boxplot(array_roubo_veiculo, vert=False, showmeans=True)
    plt.title('Boxplot dos Índices de Roubo de Veículo')

    # POSIÇÃO 2: MEDIDAS
    plt.subplot(2, 2, 2)
    plt.text(0.1, 0.9, f'Média: {media_roubo_veiculo:.2f}', fontsize=9)  
    plt.text(0.1, 0.8, f'Distância: {distancia:.2f}%', fontsize=9)  
    plt.text(0.1, 0.7, f'Limite Inferior: {limite_inferior:.2f}', fontsize=9)
    plt.text(0.1, 0.6, f'Mínimo: {minimo:.2f}', fontsize=9)
    plt.text(0.1, 0.5, f'Quartil Inferior: {quartil_inferior:.2f}', fontsize=9)    
    plt.text(0.1, 0.4, f'Mediana: {mediana_roubo_veiculo:.2f}', fontsize=9)
    plt.text(0.1, 0.3, f'Quartil Superior: {quartil_superior:.2f}', fontsize=9)
    plt.text(0.1, 0.2, f'Limite Superior: {limite_superior:.2f}', fontsize=9)    
    plt.text(0.1, 0.1, f'Máximo: {maximo:.2f}', fontsize=9)    
    plt.text(0.1, 0.0, f'Amplitude: {amplitude:.2f}', fontsize=9)

    plt.axis('off')
    plt.title('Resumo Estatístico',)

    # POSIÇÃO 3 - DEMONSTRAÇÃO DOS OUTLIERS SUPERIORES
    plt.subplot(2, 2, 3)
    df_roubo_veiculo_outliers_superiores = (        
        df_roubo_veiculo_outliers_superiores
        .head(10)
        .sort_values(by= 'roubo_veiculo', ascending=False)
        )    

    plt.bar(
        df_roubo_veiculo_outliers_superiores['munic'], #.str.slice(0, 10),  str slice limita os caracteres
        df_roubo_veiculo_outliers_superiores['roubo_veiculo']
    )

    deslocamento = max(df_roubo_veiculo_outliers_superiores['roubo_veiculo']) * 0.01

     # Rotulo dos dados:
    for i, valor in enumerate(df_roubo_veiculo_outliers_superiores['roubo_veiculo']):
        plt.text(        
        i, # posição X
        valor + deslocamento, # posição Y 
        f'{valor:,}',
        ha= 'center'
        )

    plt.xticks(rotation=45, ha='right') # Rotaciona o texto eixo x
    plt.title('Municípios com Outliers Superiores')

    # POSIÇÃO 4 - HISTOGRAMA
    plt.subplot(2, 2, 4)
    plt.hist(array_roubo_veiculo, bins=100) # bins são intervalos (quantidade de 100 intervalos no histograma)
    plt.axvline(media_roubo_veiculo, color='green', linewidth=1)
    plt.axvline(mediana_roubo_veiculo, color='orange', linewidth=1)

    plt.title('Medidas de Distribuição')




    # # POSIÇÃO 4 - DEMONSTRAÇÃO DOS OUTLIERS INFERIORES OU DADOS MENORES - retirado para colocarmos Assimetria e Curtose
    # plt.subplot(2, 2, 4)
    
    # if len(df_roubo_veiculo_outliers_inferiores) > 0:
    #     df_roubo_veiculo_outliers_inferiores = (
    #         df_roubo_veiculo_outliers_inferiores            
    #         .sort_values(by= 'roubo_veiculo', ascending=True)
    #     )

    #     plt.barh(
    #         df_roubo_veiculo_outliers_inferiores['munic'],
    #         df_roubo_veiculo_outliers_inferiores['roubo_veiculo']
    #     )     

    #     plt.title ('Municipios c/Outliers Inferiores')

    # else:
    #     df_roubo_veiculo_menores = (
    #         df_roubo_veiculo_menores
    #         .head(10)
    #         .sort_values(by='roubo_veiculo', ascending=False)    
    #     )   

    #     plt.barh(
    #         df_roubo_veiculo_menores['munic'].str.slice(0, 25),
    #         df_roubo_veiculo_menores['roubo_veiculo']
    #     )

    #     deslocamento = max(df_roubo_veiculo_menores['roubo_veiculo']) * 0.03

    #        # Rotulo dos dados:
    #     for i, valor in enumerate(df_roubo_veiculo_menores['roubo_veiculo']):
    #         plt.text(
    #             valor + deslocamento, # psição X 
    #             i, # posição Y
    #             f'{valor:,}',
    #             ha= 'center'
    #         )

    #         plt.title('Municipios com Menores Índices de Roubo')

    plt.show()

except Exception as e:
    print(f'Erro ao plotar o gráfico: {e}')
    