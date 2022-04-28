"""
CarPricePrediction.ipynb
Arquivo para realizar a predição de preços dos carros
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error

## Funções
def knn_train_test(train_col, target_col, dataframe, k_values):
    """
    Testing and training a K-Neighbors model

    Args:
    train_col: list of string. The name columns that will be used to train the model
    target_col: string. The name of the feature to predict
    dataframe: dataframe. Pandas structure containing the data
    k_values: list of ints. List of number of neighbors that will be considered when applying KNN.
    """
    np.random.seed(1)

    # Randomize order of rows in data frame.
    shuffled_index = np.random.permutation(dataframe.index)
    rand_df = dataframe.reindex(shuffled_index)

    # Divide number of rows in half and round.
    last_train_row = int(len(rand_df) / 2)

    # Select the first half and set as training set. Select the second half and set as test set.
    train_df = rand_df.iloc[0:last_train_row]
    test_df = rand_df.iloc[last_train_row:]

    k_rmses = {}

    for k in k_values:
        # Fit model using k nearest neighbors.
        knn = KNeighborsRegressor(n_neighbors=k)
        knn.fit(train_df[train_col], train_df[target_col])

        # Make predictions using model.
        predicted_labels = knn.predict(test_df[train_col])

        # Calculate and return RMSE.
        mse = mean_squared_error(test_df[target_col], predicted_labels)
        rmse = np.sqrt(mse)
        k_rmses[k] = rmse

    return k_rmses

pd.options.display.max_columns = 99

## Introduction
# Dataset reading
cols = ['symboling', 'normalized-losses', 'make', 'fuel-type', 'aspiration', 'num-of-doors',
'body-style', 'drive-wheels', 'engine-location', 'wheel-base', 'length', 'width', 'height',
'curb-weight', 'engine-type', 'num-of-cylinders', 'engine-size', 'fuel-system', 'bore', 'stroke',
'compression-rate', 'horsepower', 'peak-rpm', 'city-mpg', 'highway-mpg', 'price']
cars = pd.read_csv('imports-85.data', names=cols)

# Selecting continuous values
continuous_values_cols = ['normalized-losses', 'wheel-base', 'length', 'width', 'height',
'curb-weight', 'engine-size', 'bore', 'stroke', 'compression-rate', 'horsepower', 'peak-rpm',
'city-mpg', 'highway-mpg', 'price']
numeric_cars = cars[continuous_values_cols]


## Data cleaning
# Missing values
numeric_cars = numeric_cars.replace('?', np.nan)
numeric_cars = numeric_cars.astype('float')
numeric_cars = numeric_cars.dropna(subset=['price'])
numeric_cars.isnull().sum()
numeric_cars = numeric_cars.fillna(numeric_cars.mean())

# Normalization
price_col = numeric_cars['price']
numeric_cars = (numeric_cars - numeric_cars.min())/(numeric_cars.max() - numeric_cars.min())
numeric_cars['price'] = price_col


## Models
# Univariate

# Testing each train column with k = 5
rmse_results = {}
train_cols = numeric_cars.columns.drop('price')
k_neighbors = [5]

# For each column train a model, return RMSE value and add to the dictionary `rmse_results`
for col in train_cols:
    rmse_val = knn_train_test([col], 'price', numeric_cars, k_neighbors)
    rmse_results[col] = rmse_val[k_neighbors[0]]

# Create a Series object from the dictionary so we can easily view the results, sort, etc
rmse_results_series = pd.Series(rmse_results)
print("RMSE Results considering Univariate model and k = 5")
print(rmse_results_series.sort_values())
print()


# Testing with each train column and different values of k_neighbors
k_rmse_results = {}
k_neighbors = [1,3,5,7,9]

for col in train_cols:
    rmse_val = knn_train_test([col], 'price', numeric_cars, k_neighbors)
    k_rmse_results[col] = rmse_val

# Plotting results (univariate)
for _,v in k_rmse_results.items():
    x = list(v.keys())
    y = list(v.values())

    plt.plot(x,y)
    plt.xlabel('k value')
    plt.ylabel('RMSE')
plt.savefig('./images/univariate.png')

# Multivariate
# Compute average RMSE across different `k` values for each feature.
feature_avg_rmse = {}
for k_n,v in k_rmse_results.items():
    avg_rmse = np.mean(list(v.values()))
    feature_avg_rmse[k_n] = avg_rmse

series_avg_rmse = pd.Series(feature_avg_rmse)
sorted_series_avg_rmse = series_avg_rmse.sort_values()
print("Average RMSE Results considering Univariate model and k = [1,3,5,7,9]")
print(sorted_series_avg_rmse)
print()

sorted_features = sorted_series_avg_rmse.index

# Testing with 2 to 7 best features
k_rmse_results = {}
k_neighbors = [5]

for nr_best_feats in range(2,7):
    k_rmse_results[f'{nr_best_feats} best features'] = knn_train_test(
        sorted_features[:nr_best_feats],
        'price',
        numeric_cars,
        k_neighbors
    )

print("RMSE Results considering Multivariate model and k = 5")
print(k_rmse_results)
print()

## Hyperparameter tuning
k_rmse_results = {}
k_neighbors = list(range(1,25))

for nr_best_feats in range(2,6):
    k_rmse_results[f'{nr_best_feats} best features'] = knn_train_test(
        sorted_features[:nr_best_feats],
        'price',
        numeric_cars,
        k_neighbors
    )

print("RMSE Results considering Multivariate model and k = [1,3,5,7,9]")
print(k_rmse_results)
print()

plt.clf()
for k_n,v in k_rmse_results.items():
    x = list(v.keys())
    y = list(v.values())
    plt.plot(x,y, label=f'{k_n}')

plt.xlabel('k value')
plt.ylabel('RMSE')
plt.legend()
plt.savefig('./images/multivariate.png')
