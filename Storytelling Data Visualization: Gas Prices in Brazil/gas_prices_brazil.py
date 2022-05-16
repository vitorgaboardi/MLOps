"""
Author: Vitor Gaboardi dos Santos
Date: May 2022
Image construction comparing gas prices in Brazil.
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')


def read_data(path, sep=''):
    """
    Read a comma-separated values (csv) file and stores in a dataframe using pandas.

    Args:
    path: string. Any valid string path of the csv.
    sep: string. Delimiter to use.
    """
    data_frame = pd.read_csv(path, sep=sep)
    return data_frame

def columns_processing(data_frame,select_columns,rename_columns=''):
    """
    Select and rename columns from dataframe.

    Args:
    data_frame: pandas dataFrame. Any valid string path of the csv.
    select_columns: list of string. Delimiter to use.
    rename_columns: dict of strings. Key: old column name. Value: new columns names.
    """
    new_data_frame = data_frame[select_columns].copy()
    if rename_columns != '':
        new_data_frame.rename(columns=rename_columns, inplace=True)
    return new_data_frame

def rolling_mean(data_frame,target_column,num_samples):
    """
    Computes moving average considering the column *target_column* and *num_samples* last samples.

    Args:
    data_frame: pandas dataFrame. Any valid string path of the csv.
    select_columns: string. Column to compute the moving average.
    rename_columns: int. Number of samples to consider in the moving average.
    """
    moving_average_result = data_frame[target_column].rolling(num_samples).mean()
    return moving_average_result

# read csv file
dataframe = read_data('gas_prices_brazil.tsv', sep='\t')

# processing dataframe
gas_prices = columns_processing(
    dataframe,
    ['DATA INICIAL', 'ESTADO', 'PRODUTO', 'PREÇO MÉDIO REVENDA'],
    {'DATA INICIAL':'DATA', 'PREÇO MÉDIO REVENDA': 'PRECO'})
gas_prices_rn = gas_prices[
    (gas_prices['ESTADO'] == 'RIO GRANDE DO NORTE') & (gas_prices['PRODUTO'] == 'GASOLINA COMUM')
    ].drop(columns=['ESTADO','PRODUTO'])
gas_prices_rn['DATA'] = pd.to_datetime(gas_prices_rn['DATA'])
gas_prices_rn.reset_index(drop=True, inplace=True)
gas_prices_rn['MÉDIA MOVEL'] = rolling_mean(gas_prices_rn,'PRECO',4)

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
