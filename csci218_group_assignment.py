# -*- coding: utf-8 -*-
"""Csci218_Group_Assignment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RUXYuAcwlg4_5UING6K4knmfPRynrm8L

##Regression

Importing/Combining Dataset
"""

import pandas as pd

# Load the dataset
red_wine = pd.read_csv('winequality-red.csv', delimiter=';')
white_wine = pd.read_csv('winequality-white.csv', delimiter=';')

# Combine both datasets if needed
red_wine['type'] = 'red'
white_wine['type'] = 'white'
wine_data = pd.concat([red_wine, white_wine], ignore_index=True)

"""Exploring the Dataset"""

import seaborn as sns
import matplotlib.pyplot as plt

# Check for missing values
print(wine_data.isnull().sum())

# Summary statistics
print(wine_data.describe())

# Encode the 'type' column into numeric values
wine_data_encoded = pd.get_dummies(wine_data, columns=['type'], drop_first=True)

# Compute the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(wine_data_encoded.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Distribution of target variable
sns.histplot(wine_data['quality'], bins=10, kde=True)
plt.title('Distribution of Wine Quality')
plt.show()

"""Data Pre-Processing"""

from sklearn.model_selection import train_test_split

# Encode categorical variable (if combined)
wine_data = pd.get_dummies(wine_data, columns=['type'], drop_first=True)

# Split into features and target
X = wine_data.drop('quality', axis=1)
y = wine_data['quality']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

"""Feature Scaling"""

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

"""Random Forest Regression"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Initialize the model
model = RandomForestRegressor(random_state=42)

# Train the model
model.fit(X_train_scaled, y_train)

# Make predictions
y_pred = model.predict(X_test_scaled)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'MSE: {mse}, R2: {r2}')

"""Linear Regression"""

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Initialize the model
linear_model = LinearRegression()

# Train the model
linear_model.fit(X_train_scaled, y_train)

# Make predictions
y_pred_linear = linear_model.predict(X_test_scaled)

# Evaluate the model
mse_linear = mean_squared_error(y_test, y_pred_linear)
r2_linear = r2_score(y_test, y_pred_linear)
print(f'Linear Regression - MSE: {mse_linear}, R2: {r2_linear}')

"""Gradient Boosting"""

from sklearn.ensemble import GradientBoostingRegressor

# Initialize the model
gb_model = GradientBoostingRegressor(random_state=42)

# Train the model
gb_model.fit(X_train_scaled, y_train)

# Make predictions
y_pred_gb = gb_model.predict(X_test_scaled)

# Evaluate the model
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)
print(f'Gradient Boosting - MSE: {mse_gb}, R2: {r2_gb}')

"""Comparing Results"""

# Create a DataFrame to compare results
results = pd.DataFrame({
    'Model': ['Random Forest', 'Gradient Boosting', 'Linear Regression'],
    'MSE': [mse, mse_gb, mse_linear],
    'R2': [r2, r2_gb, r2_linear]
})

# Display the results
print(results)

"""Visualising Results"""

# Plotting the results
fig, ax = plt.subplots(1, 2, figsize=(16, 6))

# MSE Comparison
sns.barplot(x='Model', y='MSE', data=results, ax=ax[0])
ax[0].set_title('Model Comparison - MSE')
ax[0].tick_params(axis='x', rotation=45)

# R2 Comparison
sns.barplot(x='Model', y='R2', data=results, ax=ax[1])
ax[1].set_title('Model Comparison - R2')
ax[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

"""RandomForestRegressor Hyperparameter Tuning"""

from sklearn.model_selection import GridSearchCV

# Define the parameter grid for Random Forest
param_grid_rf = {
    'n_estimators': [50, 100],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2],
    'bootstrap': [True, False]
}

# Initialize GridSearchCV for Random Forest
grid_search_rf = GridSearchCV(estimator=RandomForestRegressor(random_state=42),
                              param_grid=param_grid_rf,
                              cv=3,
                              n_jobs=-1,
                              scoring='r2',
                              verbose=2)

# Fit GridSearchCV
grid_search_rf.fit(X_train_scaled, y_train)

# Best parameters and best score
print(f"Best parameters for Random Forest: {grid_search_rf.best_params_}")
print(f"Best R2 score for Random Forest: {grid_search_rf.best_score_}")

# Predict using the best model
y_pred_rf_tuned = grid_search_rf.predict(X_test_scaled)

# Evaluate the tuned Random Forest model
mse_rf_tuned = mean_squared_error(y_test, y_pred_rf_tuned)
r2_rf_tuned = r2_score(y_test, y_pred_rf_tuned)
print(f'Tuned Random Forest - MSE: {mse_rf_tuned}, R2: {r2_rf_tuned}')

"""GradientBoostingRegressor Hyperparameter Tuning"""

# Define the parameter grid for Gradient Boosting
param_grid_gb = {
    'n_estimators': [50, 100],
    'learning_rate': [0.01, 0.1],
    'max_depth': [3, 5],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}

# Initialize GridSearchCV for Gradient Boosting
grid_search_gb = GridSearchCV(estimator=GradientBoostingRegressor(random_state=42),
                              param_grid=param_grid_gb,
                              cv=3,
                              n_jobs=-1,
                              scoring='r2',
                              verbose=2)

# Fit GridSearchCV
grid_search_gb.fit(X_train_scaled, y_train)

# Best parameters and best score
print(f"Best parameters for Gradient Boosting: {grid_search_gb.best_params_}")
print(f"Best R2 score for Gradient Boosting: {grid_search_gb.best_score_}")

# Predict using the best model
y_pred_gb_tuned = grid_search_gb.predict(X_test_scaled)

# Evaluate the tuned Gradient Boosting model
mse_gb_tuned = mean_squared_error(y_test, y_pred_gb_tuned)
r2_gb_tuned = r2_score(y_test, y_pred_gb_tuned)
print(f'Tuned Gradient Boosting - MSE: {mse_gb_tuned}, R2: {r2_gb_tuned}')

"""Compare Results"""

# Create a DataFrame to compare results
results = pd.DataFrame({
    'Model': ['Random Forest', 'Tuned Random Forest', 'Gradient Boosting', 'Tuned Gradient Boosting', 'Linear Regression'],
    'MSE': [mse, mse_rf_tuned, mse_gb, mse_gb_tuned, mse_linear],
    'R2': [r2, r2_rf_tuned, r2_gb, r2_gb_tuned, r2_linear]
})

# Display the results
print(results)

"""Visualising Results"""

# Plotting the results
fig, ax = plt.subplots(1, 2, figsize=(16, 6))

# MSE Comparison
sns.barplot(x='Model', y='MSE', data=results, ax=ax[0])
ax[0].set_title('Model Comparison - MSE')
ax[0].tick_params(axis='x', rotation=45)

# R2 Comparison
sns.barplot(x='Model', y='R2', data=results, ax=ax[1])
ax[1].set_title('Model Comparison - R2')
ax[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()