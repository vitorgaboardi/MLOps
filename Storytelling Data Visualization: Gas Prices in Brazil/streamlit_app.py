"""
Author: Vitor Gaboardi dos Santos
Date: May 2022
Dashboard comparing gas prices in Brazil using Streamlit.
"""

from datetime import timedelta
import logging
import pandas as pd
import streamlit as st
import altair as alt
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

def select_presidents(dataframe):
    """
    Creates a new column representing the president.

    Args:
    data_frame: pandas dataFrame. Any valid string path of the csv.
    """
    if dataframe['DATA'].year < 2011:
        return 'Lula'
    elif dataframe['DATA'].year < 2016 or (dataframe['DATA'].year <= 2016 and dataframe['DATA'].month < 9):
        return 'Dilma'
    elif (dataframe['DATA'].year <= 2016 and dataframe['DATA'].month >= 9) or dataframe['DATA'].year < 2019:
        return 'Temer'
    else:
        return 'Bolsonaro'

# Define the base time-series chart.
def get_chart(data):
    """
    Creates a chart structure to be build at Streamlit.

    Args:
    data: pandas dataFrame. Any valid string path of the csv.
    """
    hover = alt.selection_single(
        fields=["DATA"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="")
        .mark_line()
        .encode(
            x="DATA",
            y="PRECO",
            color="PRESIDENTE",
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="DATA",
            y="PRECO",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("DATA", title="Data"),
                alt.Tooltip("PRECO", title="Preço (R$)"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()


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

# adding president column
gas_prices_rn['PRESIDENTE'] = gas_prices_rn.apply(select_presidents, axis=1)

# getting chart
chart = get_chart(gas_prices_rn)

# title
st.subheader('Gasto para encher o tanque aumenta em 102.2% desde o governo Lula!')
st.text('Preço médio da gasolina comum no Estado do Rio Grande do Norte:')

# plotting chart
st.altair_chart(
    (chart).interactive(),
    use_container_width=True
)
