"""
gas_prices_brazil.py
Arquivo para realizar a construção de uma imagem comparando o preço da gasolina em diferentes
governos brasileiros
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

# read csv file
dataframe = pd.read_csv('gas_prices_brazil.tsv', sep='\t')

# processing dataframe
gas_prices = dataframe[['DATA INICIAL', 'ESTADO', 'PRODUTO', 'PREÇO MÉDIO REVENDA']].copy()
gas_prices.rename(columns={'DATA INICIAL':'DATA', 'PREÇO MÉDIO REVENDA': 'PRECO'}, inplace=True)
gas_prices_rn = gas_prices[
    (gas_prices['ESTADO'] == 'RIO GRANDE DO NORTE') & (gas_prices['PRODUTO'] == 'GASOLINA COMUM')
    ].drop(columns=['ESTADO','PRODUTO'])
gas_prices_rn['DATA'] = pd.to_datetime(gas_prices_rn['DATA'])
gas_prices_rn.reset_index(drop=True, inplace=True)
gas_prices_rn['MÉDIA MOVEL'] = gas_prices_rn['PRECO'].rolling(4).mean()

# separating data by president
lula = gas_prices_rn.copy()[gas_prices_rn['DATA'].dt.year < 2011]
dilma = gas_prices_rn.copy()[
    (gas_prices_rn['DATA'].dt.year >= 2011) &
    ((gas_prices_rn['DATA'].dt.year < 2017) & (gas_prices_rn['DATA'].dt.month < 9))]
temer = gas_prices_rn.copy()[
    ((gas_prices_rn['DATA'].dt.year >= 2016) & (gas_prices_rn['DATA'].dt.month >= 9)) &
    (gas_prices_rn['DATA'].dt.year < 2019)]
bolsonaro = gas_prices_rn.copy()[gas_prices_rn['DATA'].dt.year >= 2019]

# saving figure
plt.figure(figsize=(15, 6))
plt.plot(lula['DATA'], lula['MÉDIA MOVEL'],color='#FF0000',label="Lula")
plt.plot(dilma['DATA'], dilma['MÉDIA MOVEL'],color='#4169e1',label='Dilma')
plt.plot(temer['DATA'], temer['MÉDIA MOVEL'],color='#008000',label='Temer')
plt.plot(bolsonaro['DATA'], bolsonaro['MÉDIA MOVEL'],color='#8b5742',label='Bolsonaro')
plt.grid(alpha=0.5)
plt.ylim(1.9,6.5)
plt.legend()
plt.title("Preço médio da gasolina no Estado do Rio Grande do Norte",fontsize=20,weight='bold')

plt.savefig('./images/gas_prices_brazil.png')
