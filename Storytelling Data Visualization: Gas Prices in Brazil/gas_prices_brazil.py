"""
Author: Vitor Gaboardi dos Santos
Date: May 2022
Image construction comparing gas prices in Brazil.
"""

from datetime import timedelta
import logging
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

logging.basicConfig(
    filename='./logging.log',
    level=logging.INFO,
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def read_data(path, sep=''):
    """
    Read a comma-separated values (csv) file and stores in a dataframe using pandas.

    Args:
    path: string. Any valid string path of the csv.
    sep: string. Delimiter to use.
    """
    try:
        data_frame = pd.read_csv(path, sep=sep)
        assert data_frame is not None
        assert len(data_frame.columns) > 0
        logging.info('Dataframe lido corretamente')
    except ValueError:
        logging.error('Caminho do arquivo ou tipo do objeto inválido: %s',type(path))
    except FileNotFoundError:
        logging.error('O seguinte caminho ou diretório não existe: %s',path)
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
    target_column: string. Column to compute the moving average.
    num_samples: int. Number of samples to consider in the moving average.
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

# creating figure
# plots
fig, ax1 = plt.subplots(nrows=1, ncols=1,figsize=(15,6))
plt.plot(lula['DATA'], lula['MÉDIA MOVEL'],color='#FF0000',label="Lula")
plt.plot(dilma['DATA'], dilma['MÉDIA MOVEL'],color='#4169e1',label='Dilma')
plt.plot(temer['DATA'], temer['MÉDIA MOVEL'],color='#008000',label='Temer')
plt.plot(bolsonaro['DATA'], bolsonaro['MÉDIA MOVEL'],color='#8b5742',label='Bolsonaro')
plt.grid(alpha=0.5)
plt.ylim(1.9,6.5)

# background and legend configuration
ax1.set_facecolor('white')
ax1.legend(loc='upper left', bbox_to_anchor=(0.01, 0.52, 0.5, 0.5), facecolor='white')
ax1.tick_params(bottom=0, left=0)
ax1.set_yticks([2.0, 3, 4, 5, 6])
fig.patch.set_facecolor('white')
fig.patch.set_bounds(10,10,10,10)
for location in ['left', 'right', 'top', 'bottom']:
    ax1.spines[location].set_visible(False)

# title and subtitle
ax1.text(0, 1.09,
	'Gasto para encher o tanque aumenta em 102.2% desde o governo Lula *',
	size=20, weight='bold',transform=ax1.transAxes)
ax1.text(0, 1.03,
	'Preço médio da gasolina comum no Estado do Rio Grande do Norte',
	size=18,transform=ax1.transAxes)

# gas price bar
BAR_SIZE = 300
dataset = [lula,dilma,temer,bolsonaro]
y_constant = [0.5,0,0.25,0.1]

price = [round(data['PRECO'].iloc[-1]*45,2) for data in dataset]
proportion = [round(price/(bolsonaro['PRECO'].iloc[-1]*45), 2) for price in price]

y_pos = [round(data['MÉDIA MOVEL'].max()+constant,2) for data, constant in zip(dataset,y_constant)]
x_min = [data['DATA'].iloc[int(len(data)/2)]-timedelta(BAR_SIZE) for data in dataset]
x_max1 = [data['DATA'].iloc[int(len(data)/2)]+timedelta(BAR_SIZE) for data in dataset]
x_max2 = [x + timedelta(2*BAR_SIZE*p) for x, p in zip(x_min,proportion)]
x_txt_pos = [0.18,0.52,0.73,0.85]
y_txt_pos = [0.32,0.465,0.71,0.90]

for y,xmin,xmax1,xmax2,xtxt,ytxt,price in zip(y_pos,x_min,x_max1,x_max2,x_txt_pos,y_txt_pos,price):
    ax1.hlines(y,xmin,xmax1,linewidth=10,color='black',alpha=0.3)
    ax1.hlines(y,xmin,xmax2,linewidth=10,color='black')
    ax1.text(xtxt,ytxt,'R$ '+str(price),transform=ax1.transAxes)

# copyright
ax1.text(0, -0.15,
	'* Considerou-se um carro com 45 litros' + ' '*125 + 'Criado por Vitor G. Santos',
	color = '#f0f0f0', backgroundcolor = '#4d4d4d',size=13,transform=ax1.transAxes)

plt.savefig('./images/gas_prices_brazil.png')
