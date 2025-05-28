import requests
import pandas as pd
from datetime import datetime

# Example known timestamp
timestamp = pd.to_datetime(datetime.utcnow()).value // 10**9
response = requests.post('http://localhost:5000/predict', json={'timestamp': timestamp})
print("Test Prediction:", response.json())
