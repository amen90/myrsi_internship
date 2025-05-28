import paho.mqtt.client as mqtt
import sqlite3
import json
import requests

# Database setup
def init_db():
    conn = sqlite3.connect('dht_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        temp REAL,
        hum REAL
    )
    ''')
    conn.commit()
    conn.close()
    print("Database and table created successfully")

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker successfully")
        client.subscribe("esp32/dht")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    data = json.loads(payload)
    # Ensure data is a dictionary
    if isinstance(data, dict):
        # Use get method to safely access the 'temp' key
        temp = data.get('temp', default_value)
    else:
        # Handle the case where data is not a dictionary
        temp = default_value
    
    # Replace default_value with an appropriate default value
    default_value = None  # or any other value that makes sense in your context
    hum = data['hum']
    save_to_db(temp, hum)
    predict(data)


# Save readings to database
def save_to_db(temp, hum):
    conn = sqlite3.connect('dht_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO readings (temp, hum) VALUES (?, ?)", (temp, hum))
    conn.commit()
    conn.close()
    print("Data stored successfully")

# Make predictions by sending a request to the Flask prediction service
def predict(data):
    try:
        response = requests.post('http://localhost:5000/predict', json=data)
        if response.status_code == 200:
            predictions = response.json()
            print(f"Predicted humidity: {predictions['predicted_humidity']}")
            print(f"Predicted temperature: {predictions['predicted_temperature']}")
        else:
            print(f"Error in prediction response: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error making predictions: {e}")

# Main execution
if __name__ == "__main__":
    init_db()
    
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    
    broker = "broker.hivemq.com"
    print(f"Connecting to broker at {broker}...")
    mqtt_client.connect(broker, 1883, 60)
    
    mqtt_client.loop_forever()
