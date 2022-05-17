"""
Author: Vitor Gaboardi dos Santos
Date: May 2022
Test File
"""

import pandas as pd
from pandas.api.types import is_numeric_dtype
from gas_prices_brazil import read_data, rolling_mean

def test_read_data():
    data = read_data("gas_prices_brazil.tsv", sep='\t')
    assert data is not None

def test_columns_data():
    data = read_data("gas_prices_brazil.tsv", sep='\t')
    assert len(data.columns) > 0

def test_has_data():
    data = read_data("gas_prices_brazil.tsv", sep='\t')
    assert len(data) > 0

def test_rolling_mean():
    data = read_data("gas_prices_brazil.tsv", sep='\t')
    moving_average_result = rolling_mean(data,'PREÇO MÉDIO REVENDA',4)
    assert is_numeric_dtype(moving_average_result) 
