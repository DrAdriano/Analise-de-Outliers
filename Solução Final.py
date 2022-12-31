import pandas as pd
import matplotlib.pyplot as plt

# 1 Importar a base de dados

dados = pd.read_csv('Base de dados de imóveis.csv', sep=';')

# 2 Visualizar a base de dados

print('\n A base de dados é:')
print(dados)
print('\n A base de dados apresenta {} registros de imóveis e {} colunas com informações sobre os mesmos.'.format(
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
    f"Existem {dados_residenciais[dados_residenciais['Aluguel'].isnull()].shape[0]} imóveis com valores nulos, podemos excluí-los.")
dados_residenciais.dropna(subset=['Aluguel'], inplace=True)

# 3.3 Tratar valores nulos do condomínio

print(
    f"Existem {dados_residenciais[dados_residenciais['Condominio'].isnull()].shape[0]} imóveis com condomínios nulos.")
selecao = (
    ((dados_residenciais['Tipo'] == 'Apartamento') |
     (dados_residenciais['Tipo'] == 'Quitinete') |
     (dados_residenciais['Tipo'] == 'Casa de Condomínio'))
    & dados_residenciais['Condominio'].isnull()
)
dados_residenciais = dados_residenciais[~selecao]
print(
    f"Agora, existem {dados_residenciais[dados_residenciais['Condominio'].isnull()].shape[0]} imóveis com condomínios nulos, todos sendo casas.")
dados_residenciais = dados_residenciais.fillna({'Condominio': 0})
adj_index(dados_residenciais)

# 4 Resolver as tarefas e realizar uma análise
# 4.1 Calcular do valor bruto para morar em cada imóvel

dados_residenciais['Valor Bruto'] = dados_residenciais['Aluguel'] + \
    dados_residenciais['Condominio']

# 4.2 Calcular do valor do metro quadrado de cada imóvel

dados_residenciais['Valor / m^2'] = dados_residenciais['Valor Bruto'] / \
    dados_residenciais['Area'].round(1)

# 4.3 Contar a quantidade de imóveis com as quantidades de quartos

zero = [0]
selecao = dados_residenciais['Quartos'].isin(zero)
selecao1 = (dados_residenciais['Tipo'] == 'Quitinete') & (
    dados_residenciais['Quartos'] == 0)
selecao2 = (dados_residenciais['Tipo'] == 'Quitinete') & (
    dados_residenciais['Quartos'] > 0)
mensagem = f'''
Há {dados_residenciais[selecao].shape[0]} imóveis residenciais sem quartos,  
sendo {dados_residenciais[selecao1].shape[0]} quitinetes. Ao mesmo tempo, há 
{dados_residenciais[selecao2].shape[0]} quitinetes marcados com 1 quarto ou 
mais.
'''
print(mensagem)

classes = [0, 2, 4, 6, 100]
quartos = pd.cut(dados_residenciais.Quartos, classes)
quartos = pd.cut(dados_residenciais.Quartos, classes, include_lowest=True)
labels = ['Até 2 quartos:', '3 e 4 quartos:',
          '5 e 6  quartos:', '7 quartos ou mais:']
quartos = pd.cut(dados_residenciais.Quartos, classes,
                 labels=labels, include_lowest=True)
print(pd.value_counts(quartos))

# 4.4 Calcular do valor médio do aluguel por bairro

print(f"Há {dados_residenciais['Bairro'].drop_duplicates().shape[0]} bairros.")
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

# 4.5 Remover os outliers
# 4.5.1 Remover os outliers para todos os imóveis residenciais

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


# 4.5.1 Remover os outliers por tipo de imóvel residencial
# 4.6 Recalcular dos valores estatísticos descritivos do aluguel
