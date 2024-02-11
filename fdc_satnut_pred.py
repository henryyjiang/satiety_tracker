import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from xgboost import XGBRegressor

df = pd.read_csv("fdc-satnut.csv")
df = df.drop(['serving_size', 'Closest_Match', 'Food_y', 'alcohol', 'theobromine', 'lucopene'], axis=1)
df = df.iloc[:, 1:]


# Extract numeric values and remove units
def remove_units_and_convert(column):
    column = column.astype(str)
    values = column.str.extract(r'(\d+\.?\d*)').astype(float)
    return values


# Apply the function to each column and overwrite the original columns
for column in df.select_dtypes('object').iloc[:, 2:].columns:
    df[column] = remove_units_and_convert(df[column])

'''
Feature Selection
'''

X = df.iloc[:, 4:]
y = df['Satiety Index']

model = xgb.XGBRegressor(objective='reg:squarederror', seed=42)

# Train the model
model.fit(X, y)

# Get feature importances
feature_importances = model.feature_importances_

# Create a DataFrame to display feature importances
feature_importance_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance': feature_importances
})

# Sort features by importance
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

X1 = df[list(feature_importance_df.iloc[:23, 0])]

X_train, X_test, y_train, y_test = train_test_split(X1, y, test_size=0.1, random_state=42)

# Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns)

X_test_scaled = scaler.transform(X_test)
X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns)

# Making the model

'''

# Hyperparameter tuning

xgb_model = XGBRegressor()

# Define the hyperparameter distributions for random search
param_dist = {
    'n_estimators': randint(100, 1000),  # Random integer values between 100 and 1000
    'max_depth': randint(3, 10),  # Random integer values between 3 and 10
    'learning_rate': uniform(0.01, 0.3),  # Random float values between 0.01 and 0.3
    'gamma': uniform(0, 0.5),  # Random float values between 0 and 0.5
    'subsample': uniform(0.5, 0.5),  # Random float values between 0.5 and 1.0
    'colsample_bytree': uniform(0.5, 0.5), # Random float values between 0.5 and 1.0

}

# Perform random search with cross-validation
random_search = RandomizedSearchCV(estimator=xgb_model, param_distributions=param_dist, n_iter = 100, cv = 4, scoring='r2', random_state=42)
random_search.fit(X_train, y_train)

# Print the best hyperparameters found
print("Best Hyperparameters:", random_search.best_params_)

# Evaluate the best model on the test set
best_model = random_search.best_estimator_
print(best_model)
r2_score = best_model.score(X_test, y_test)
print("R2 Score on Test Set:", r2_score)

'''
model = xgb.XGBRegressor(objective='reg:squarederror', seed=42, colsample_bytree=0.6654490124263246,
                         gamma=0.03177917514301182, learning_rate=0.10329469651469865, max_depth=7, n_estimators=198,
                         subsample=0.7956488938538635)

model.fit(X_train_scaled, y_train)
y_test_pred = model.predict(X_test_scaled)
y_train_pred = model.predict(X_test_scaled)
r2 = r2_score(y_test, y_test_pred)  # Greater than 0.6
print(r2)
mse = mean_squared_error(y_test, y_test_pred)
mae = mean_absolute_error(y_test, y_test_pred)