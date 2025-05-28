from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
from flask_mqtt import Mqtt
import json

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)

# Load models
temperature_model = joblib.load('ai_model/dht_temperature_model.pkl')
humidity_model = joblib.load('ai_model/dht_humidity_model.pkl')

data_storage = {
    'timestamps': [],
    'temperatures': [],
    'humidities': []
}

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('sensor/data')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = json.loads(message.payload.decode())
    update_data_storage(data['timestamp'], data['temperature'], data['humidity'])

def update_data_storage(timestamp, temperature, humidity):
    data_storage['timestamps'].append(timestamp)
    data_storage['temperatures'].append(temperature)
    data_storage['humidities'].append(humidity)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data_storage)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    temp = data['temp']
    temp_array = np.array([[temp]])
    
    # Make predictions
    humidity_pred = humidity_model.predict(temp_array)
    temperature_pred = temperature_model.predict(temp_array)
    
    # Print predictions to the terminal
    print(f"Predicted Humidity: {humidity_pred[0]}")
    print(f"Predicted Temperature: {temperature_pred[0]}")
    
    # Return predictions as JSON response
    return jsonify({
        'predicted_humidity': humidity_pred[0],
        'predicted_temperature': temperature_pred[0]
    })

@app.route('/led', methods=['POST'])
def led():
    data = request.get_json()
    state = data['state']
    # Logic to control the LED would go here
    return jsonify({'status': 'success', 'state': state})

@app.route('/update_data', methods=['POST'])
def update_data():
    data = request.get_json()
    timestamp = data['timestamp']
    temperature = data['temperature']
    humidity = data['humidity']
    
    update_data_storage(timestamp, temperature, humidity)
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
