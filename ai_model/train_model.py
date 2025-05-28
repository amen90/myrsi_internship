import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Connect to the SQLite database
conn = sqlite3.connect('../mqtt_subscriber/dht_data.db')

# Read data from the 'readings' table into a pandas DataFrame
try:
    data = pd.read_sql_query("SELECT temp, hum FROM readings", conn)
except Exception as e:
    print(f"Error reading from the database: {e}")
    conn.close()
    exit(1)

# Close the connection
conn.close()

# Display the first few rows of the DataFrame to understand its structure
print(data.head())

# Separate the features (temperature) and target (humidity)
X = data[['temp']]
y_humidity = data['hum']
y_temperature = data['temp']

# Split the data into training and testing sets for humidity prediction
X_train_hum, X_test_hum, y_train_hum, y_test_hum = train_test_split(X, y_humidity, test_size=0.2, random_state=42)

# Split the data into training and testing sets for temperature prediction
X_train_temp, X_test_temp, y_train_temp, y_test_temp = train_test_split(X, y_temperature, test_size=0.2, random_state=42)

# Create and train a linear regression model for humidity prediction
model_hum = LinearRegression()

# Perform cross-validation for humidity prediction
cv_scores_hum = cross_val_score(model_hum, X_train_hum, y_train_hum, cv=5, scoring='neg_mean_squared_error')
print(f'Cross-validation MSE scores for humidity: {-cv_scores_hum}')
print(f'Mean Cross-validation MSE for humidity: {-cv_scores_hum.mean()}')

# Train the model for humidity prediction
model_hum.fit(X_train_hum, y_train_hum)

# Make predictions on the test set for humidity
y_pred_hum = model_hum.predict(X_test_hum)

# Evaluate the model for humidity prediction
mse_hum = mean_squared_error(y_test_hum, y_pred_hum)
r2_hum = r2_score(y_test_hum, y_pred_hum)
print(f'Mean Squared Error for humidity: {mse_hum}')
print(f'R² Score for humidity: {r2_hum}')

# Save the model for humidity prediction
joblib.dump(model_hum, 'dht_humidity_model.pkl')
print('Humidity model saved as dht_humidity_model.pkl')

# Create and train a linear regression model for temperature prediction
model_temp = LinearRegression()

# Perform cross-validation for temperature prediction
cv_scores_temp = cross_val_score(model_temp, X_train_temp, y_train_temp, cv=5, scoring='neg_mean_squared_error')
print(f'Cross-validation MSE scores for temperature: {-cv_scores_temp}')
print(f'Mean Cross-validation MSE for temperature: {-cv_scores_temp.mean()}')

# Train the model for temperature prediction
model_temp.fit(X_train_temp, y_train_temp)

# Make predictions on the test set for temperature
y_pred_temp = model_temp.predict(X_test_temp)

# Evaluate the model for temperature prediction
mse_temp = mean_squared_error(y_test_temp, y_pred_temp)
r2_temp = r2_score(y_test_temp, y_pred_temp)
print(f'Mean Squared Error for temperature: {mse_temp}')
print(f'R² Score for temperature: {r2_temp}')

# Save the model for temperature prediction
joblib.dump(model_temp, 'dht_temperature_model.pkl')
print('Temperature model saved as dht_temperature_model.pkl')
