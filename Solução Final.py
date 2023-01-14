import pandas as pd
import matplotlib.pyplot as plt

# 1 Importar a base de dados

dados = pd.read_csv('Base de dados de imóveis.csv', sep=';')

# 2 Visualizar a base de dados

print('\n A base de dados é:')
print(dados)
print('\n A base de dados apresenta {} registros de imóveis e {} colunas.'.format(
    dados.shape[0], dados.shape[1]))

# 2.1 Mostrar os tipos de dados

tipos_de_dados = pd.DataFrame(dados.dtypes, columns=['Tipos de Dados'])
tipos_de_dados.columns.name = 'Variáveis'
print('\n Os tipos de dados estão expostos na tabela abaixo:\n')
print(tipos_de_dados)

# 2.2 Mostrar os tipos de imóveis

tipo_de_imovel = dados['Tipo']
tipo_de_imovel.drop_duplicates(inplace=True)
tipo_de_imovel = pd.DataFrame(tipo_de_imovel)


def adj_index(Data_Frame):
    Data_Frame.index = range(Data_Frame.shape[0])


adj_index(tipo_de_imovel)
tipo_de_imovel.columns.name = 'Id'
print('\n Os tipos de imóveis estão expostos na tabela abaixo:\n')
print(tipo_de_imovel)

# 2.3 Identificar os imóveis residenciais

residencial = ['Apartamento', 'Casa', 'Casa de Condomínio',
               'Casa de Vila', 'Quitinete']
selecao = dados['Tipo'].isin(residencial)
dados_residenciais = dados[selecao]
adj_index(dados_residenciais)
print('\n Os dados de imóveis residenciais são:\n')
print(dados_residenciais)

print(
    f'\n Temos {dados_residenciais.shape[0]} imóveis residenciais, dentre os {dados.shape[0]} imóveis totais.\n')

plt.rc('figure', figsize=(8, 4))
area = plt.figure()
g1 = area.add_subplot(1, 1, 1)
grupo1 = dados_residenciais.groupby('Tipo')['Aluguel']
label = grupo1.count().index
valores = grupo1.count().values
g1.pie(valores, labels=label, autopct='%1.1f%%', explode=(.1, .1, .1, .1, .1))
g1.set_title('Imóveis residenciais por Tipo')
area.savefig('Arquivos_gerados_no_código/ImoveisResidenciaisPorTipo.png',
             dpi=300, bbox_inches='tight')

dados_residenciais.to_csv(
    'Arquivos_gerados_no_código/Base de dados de imóveis residenciais.csv', sep=';', index=False)

# 3 Tratar os dados
# 3.1 Excluir colunas desnecessárias

dados_residenciais = dados_residenciais.drop(
    ["Vagas", "Suites", "IPTU"], axis=1)

# 3.2 Tratar valores nulos do aluguel

print(
    f" Existem {dados_residenciais[dados_residenciais['Aluguel'].isnull()].shape[0]} imóveis com valores nulos, podemos excluí-los.")
dados_residenciais.dropna(subset=['Aluguel'], inplace=True)

# 3.3 Tratar valores nulos do condomínio

print(
    f" Existem {dados_residenciais[dados_residenciais['Condominio'].isnull()].shape[0]} imóveis com condomínios nulos.")
selecao = (
    ((dados_residenciais['Tipo'] == 'Apartamento') |
     (dados_residenciais['Tipo'] == 'Quitinete') |
     (dados_residenciais['Tipo'] == 'Casa de Condomínio'))
    & dados_residenciais['Condominio'].isnull()
)
dados_residenciais = dados_residenciais[~selecao]
print(
    f"\n Excluímos os imóveis que deveriam ter algum valor de condomínio.\n Agora, existem {dados_residenciais[dados_residenciais['Condominio'].isnull()].shape[0]} imóveis com condomínios nulos, todos sendo casas.\n Atribuímos o valor zero à elas.")

dados_residenciais = dados_residenciais.fillna({'Condominio': 0})
adj_index(dados_residenciais)

# 4 Analisar os dados
# 4.1  Calcular do valor bruto e do metro quadrado

dados_residenciais['Valor Bruto'] = dados_residenciais['Aluguel'] + \
    dados_residenciais['Condominio']

dados_residenciais['Valor / m^2'] = dados_residenciais['Valor Bruto'] / \
    dados_residenciais['Area'].round(1)

# 4.2 Calcular os valores estatísticos descritivos por bairro

print(
    f"\n Há {dados_residenciais['Bairro'].drop_duplicates().shape[0]} bairros.")

# 4.2.1 Aluguel

grupo_bairro = dados_residenciais.groupby('Bairro')
grupo_bairro[['Aluguel', 'Condominio',
              'Valor Bruto', 'Valor / m^2']].mean().round(2)
grupo_bairro['Aluguel'].describe().round(2)
grupo_bairro['Aluguel'].aggregate([
    'count', 'mean', 'std', 'median', 'min', 'max', 'sum'
]).round(2).rename(columns={
    'count': 'Frequência',
    'mean': 'Média',
    'std': 'Desvio Padrão',
    'median': 'Mediana',
    'min': 'Mínimo',
    'max': 'Máximo',
    'sum': 'Soma'
}).sort_values(by='Média', ascending=True)


plt.rc('figure', figsize=(20, 10))

fig = grupo_bairro['Aluguel'].mean().plot.bar(color='blue')
fig.set_ylabel('Valor do Aluguel')
fig.set_title('Valor Médio do Aluguel por Bairro', {'fontsize': 22})

fig = grupo_bairro['Aluguel'].max().plot.bar(color='blue')
fig.set_ylabel('Valor do Aluguel')
fig.set_title('Valor Máximo do Aluguel por Bairro', {'fontsize': 22})

fig = grupo_bairro['Aluguel'].std().plot.bar(color='blue')
fig.set_ylabel('Valor do Aluguel')
fig.set_title('Desvio Padrão do Aluguel por Bairro', {'fontsize': 22})

# 4.2.2 Valor bruto

grupo_bairro['Valor Bruto'].aggregate([
    'count', 'mean', 'std', 'median', 'min', 'max', 'sum'
]).round(2).rename(columns={
    'count': 'Frequência',
    'mean': 'Média',
    'std': 'Desvio Padrão',
    'median': 'Mediana',
    'min': 'Mínimo',
    'max': 'Máximo',
    'sum': 'Soma'
}).sort_values(by='Média', ascending=True)

fig = grupo_bairro['Valor Bruto'].mean().plot.bar(color='blue')
fig.set_ylabel('Valor')
fig.set_title('Valor Médio do Valor Bruto por Bairro', {'fontsize': 22})

fig = grupo_bairro['Valor Bruto'].max().plot.bar(color='blue')
fig.set_ylabel('Valor')
fig.set_title('Valor Máximo do Valor Bruto por Bairro', {'fontsize': 22})

ig = grupo_bairro['Valor Bruto'].std().plot.bar(color='blue')
fig.set_ylabel('Valor')
fig.set_title('Desvio Padrão do Valor Bruto por Bairro', {'fontsize': 22})


# 4.3 Remover os outliers

# 4.3.1 Para todos os imóveis residenciais juntos

dados_residenciais.boxplot(['Aluguel'])
dados_residenciais.hist(['Aluguel'])

aluguel = dados_residenciais['Aluguel']

Q1 = aluguel.quantile(.25)
Q3 = aluguel.quantile(.75)
IIQ = Q3 - Q1
limite_inferior = Q1 - 1.5 * IIQ
limite_superior = Q3 + 1.5 * IIQ

selecao = ((aluguel >= limite_inferior) & (aluguel <= limite_superior))
dados_residenciais_boxplot = dados_residenciais[selecao]
adj_index(dados_residenciais_boxplot)


def boxplot_function(Dataframe1):
    #----------------Definindo os limites para o Box Plot------------------#
    aluguel = Dataframe1['Aluguel']
    Q1 = aluguel.quantile(.25)
    Q3 = aluguel.quantile(.75)
    IIQ = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IIQ
    limite_superior = Q3 + 1.5 * IIQ
    #----Retirando os outliers e organizando os dados para o Box Plot-----#
    selecao = ((aluguel >= limite_inferior) & (aluguel <= limite_superior))
    Dataframe2 = Dataframe1[selecao]
    adj_index(Dataframe2)
    Dataframe2.boxplot(['Aluguel'])
    return Dataframe2


dados_residenciais_boxplot1 = boxplot_function(dados_residenciais)

dados_residenciais_boxplot2 = boxplot_function(dados_residenciais_boxplot1)

dados_residenciais_boxplot3 = boxplot_function(dados_residenciais_boxplot2)

dados_residenciais_boxplot4 = boxplot_function(dados_residenciais_boxplot3)

dados_residenciais_boxplot5 = boxplot_function(dados_residenciais_boxplot4)

print(
    f'\n Usando o Box Plot para todos os dados juntos, foram excluídos {dados_residenciais.shape[0]-dados_residenciais_boxplot5.shape[0]} imóveis \n na forma de outliers. Diminuição equivalente à, aproximadamente, {100*(1-dados_residenciais_boxplot5.shape[0]/dados_residenciais.shape[0]):,.0f}%.')


def quantidade_excluidos(tipo_imovel):
    if tipo_imovel in residencial:
        selecao1 = dados_residenciais['Tipo'] == "{}".format(tipo_imovel)
        selecao2 = dados_residenciais_boxplot5['Tipo'] == "{}".format(
            tipo_imovel)
        if dados_residenciais[selecao1].shape[0] != 0:
            print(f'- Foram {dados_residenciais[selecao1].shape[0]-dados_residenciais_boxplot5[selecao2].shape[0]} imóveis do tipo "{tipo_imovel}". Diminuição equivalente à, aproximadamente, {100*(1-dados_residenciais_boxplot5[selecao2].shape[0]/dados_residenciais[selecao1].shape[0]):,.0f}%.')
        else:
            print(
                f'- Foram {dados_residenciais[selecao1].shape[0]-dados_residenciais_boxplot5[selecao2].shape[0]} imóveis do tipo "{tipo_imovel}". Diminuição equivalente à 0%.')
    else:
        print('É necessário que seja um dos elementos da lista:')
        print(residencial)


for tipo_imovel in residencial:
    quantidade_excluidos(tipo_imovel)

print(
    f"\n Com a retirada dos outliers, há {dados_residenciais_boxplot5['Bairro'].drop_duplicates().shape[0]} bairros.")

bairro_excluido = (set(list(dados_residenciais['Bairro'].drop_duplicates()))
                   - set(list(dados_residenciais_boxplot5['Bairro'].drop_duplicates()))
                   )

print(
    f" Excluimos o(s) bairro(s) {list(bairro_excluido)[0]}, que tinha(m) {dados_residenciais[dados_residenciais['Bairro'].isin(list(bairro_excluido))].shape[0]} imóvel(is).")

dados_residenciais_boxplot5.hist(['Aluguel'])

# 4.3.2 Para os tipos de imóveis residenciais

dados_residenciais.boxplot(['Aluguel'], by=['Tipo'])

grupo_tipo = dados_residenciais.groupby('Tipo')['Aluguel']

Q1 = grupo_tipo.quantile(.25)
Q3 = grupo_tipo.quantile(.75)
IIQ = Q3 - Q1
limite_inferior = Q1 - 1.5 * IIQ
limite_superior = Q3 + 1.5 * IIQ

dados_tipo_boxplot1 = pd.DataFrame()
for tipo in grupo_tipo.groups.keys():
    verificando_tipo = dados_residenciais['Tipo'] == tipo
    dentro_limite = (dados_residenciais['Aluguel'] >= limite_inferior[tipo]) & (
        dados_residenciais['Aluguel'] <= limite_superior[tipo])
    selecao = verificando_tipo & dentro_limite
    dados_selecao = dados_residenciais[selecao]
    dados_tipo_boxplot1 = pd.concat([dados_tipo_boxplot1, dados_selecao])
    adj_index(dados_tipo_boxplot1)

dados_tipo_boxplot1.boxplot(['Aluguel'], by=['Tipo'])


def boxplot_function_type(Data_frame1):
    #----------------Definindo os limites para o Box Plot------------------#
    grupo_tipo = Data_frame1.groupby('Tipo')['Aluguel']
    Q1 = grupo_tipo.quantile(.25)
    Q3 = grupo_tipo.quantile(.75)
    IIQ = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IIQ
    limite_superior = Q3 + 1.5 * IIQ
    #----Retirando os outliers e organizando os dados para o Box Plot-----#
    Data_frame2 = pd.DataFrame()
    for tipo in grupo_tipo.groups.keys():
        verificando_tipo = Data_frame1['Tipo'] == tipo
        dentro_limite = (Data_frame1['Aluguel'] >= limite_inferior[tipo]) & (
            Data_frame1['Aluguel'] <= limite_superior[tipo])
        selecao = verificando_tipo & dentro_limite
        dados_selecao = Data_frame1[selecao]
        Data_frame2 = pd.concat([Data_frame2, dados_selecao])
        adj_index(Data_frame2)
    Data_frame2.boxplot(['Aluguel'], by=['Tipo'])
    return Data_frame2


dados_tipo_boxplot2 = boxplot_function_type(dados_tipo_boxplot1)

dados_tipo_boxplot3 = boxplot_function_type(dados_tipo_boxplot2)

dados_tipo_boxplot4 = boxplot_function_type(dados_tipo_boxplot3)

dados_tipo_boxplot5 = boxplot_function_type(dados_tipo_boxplot4)

dados_tipo_boxplot6 = boxplot_function_type(dados_tipo_boxplot5)

dados_tipo_boxplot7 = boxplot_function_type(dados_tipo_boxplot6)

dados_tipo_boxplot8 = boxplot_function_type(dados_tipo_boxplot7)

dados_tipo_boxplot9 = boxplot_function_type(dados_tipo_boxplot8)

dados_tipo_boxplot10 = boxplot_function_type(dados_tipo_boxplot9)

print(
    f'\n Usando o Box Plot para os dados organizados por tipo, foram excluídos {dados_residenciais.shape[0]-dados_tipo_boxplot10.shape[0]} imóveis\n na forma de outliers, uma diminuição equivalente à, aproximadamente, {100*(1-dados_tipo_boxplot10.shape[0]/dados_residenciais.shape[0]):,.0f}%.')


def quantidade_excluidos_tipo(tipo_imovel):
    if tipo_imovel in residencial:
        selecao1 = dados_residenciais['Tipo'] == "{}".format(tipo_imovel)
        selecao2 = dados_tipo_boxplot10['Tipo'] == "{}".format(tipo_imovel)
        if dados_residenciais[selecao1].shape[0] != 0:
            print(f'- Foram {dados_residenciais[selecao1].shape[0]-dados_tipo_boxplot10[selecao2].shape[0]} imóveis do tipo "{tipo_imovel}". Diminuição equivalente à, aproximadamente, {100*(1-dados_tipo_boxplot10[selecao2].shape[0]/dados_residenciais[selecao1].shape[0]):,.0f}%.')
        else:
            print(
                f'- Foram {dados_residenciais[selecao1].shape[0]-dados_tipo_boxplot10[selecao2].shape[0]} imóveis do tipo "{tipo_imovel}". Diminuição equivalente à 0%.')
    else:
        print('É necessário que seja um dos elementos da lista:')
        print(residencial)


for tipo_imovel in residencial:
    quantidade_excluidos_tipo(tipo_imovel)

print(
    f"\n Com a retirada dos outliers, há {dados_tipo_boxplot10['Bairro'].drop_duplicates().shape[0]} bairros.")

bairro_excluido = (set(list(dados_residenciais['Bairro'].drop_duplicates()))
                   - set(list(dados_tipo_boxplot10['Bairro'].drop_duplicates()))
                   )

print(
    f" Excluímos o(s) bairro(s) {list(bairro_excluido)[0]}, que tinha(m) {dados_residenciais[dados_residenciais['Bairro'].isin(list(bairro_excluido))].shape[0]} imóvel(is).\n")

dados_tipo_boxplot10.to_csv(
    'Arquivos_gerados_no_código/Base de dados de imóveis residenciais - Versão final.csv', sep=';', index=False)

# 4.4 Recalculando dos valores estatísticos
# 4.2.2 Aluguel

grupo_bairro = dados_tipo_boxplot3.groupby('Bairro')
grupo_bairro['Aluguel'].describe().round(2)

plt.rc('figure', figsize=(20, 10))
fig = grupo_bairro['Aluguel'].mean().plot.bar(color='blue')
fig.set_ylabel('Valor do Aluguel')
fig.set_title('Valor Médio do Aluguel por Bairro', {'fontsize': 22})

fig = grupo_bairro['Aluguel'].max().plot.bar(color='blue')
fig.set_ylabel('Valor do Aluguel')
fig.set_title('Valor Máximo do Aluguel por Bairro', {'fontsize': 22})

fig = grupo_bairro['Aluguel'].std().plot.bar(color='blue')
fig.set_ylabel('Valor do Aluguel')
fig.set_title('Desvio Padrão do Aluguel por Bairro', {'fontsize': 22})

# 4.2.2 Valor bruto

grupo_bairro = dados_tipo_boxplot10.groupby('Bairro')
grupo_bairro['Aluguel'].describe().round(2)

plt.rc('figure', figsize=(20, 10))
fig = grupo_bairro['Aluguel'].mean().plot.bar(color='blue')
fig.set_ylabel('Valor do Aluguel')
fig.set_title('Valor Médio do Aluguel por Bairro', {'fontsize': 22})

fig = grupo_bairro['Aluguel'].max().plot.bar(color='blue')
fig.set_ylabel('Valor do Aluguel')
fig.set_title('Valor Máximo do Aluguel por Bairro', {'fontsize': 22})

fig = grupo_bairro['Aluguel'].std().plot.bar(color='blue')
fig.set_ylabel('Valor do Aluguel')
fig.set_title('Desvio Padrão do Aluguel por Bairro', {'fontsize': 22})
