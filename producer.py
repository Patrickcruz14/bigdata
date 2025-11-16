import json
import time
from datetime import datetime
import requests
from kafka import KafkaProducer

# -------------------------
# CONFIGURATION
# -------------------------
KAFKA_BROKER = 'localhost:9092'  # Kafka broker
TOPIC = 'weather_topic'          # Kafka topic
CITY = "Quezon City"
API_KEY = "35034f2ecfa458f14d42d46218eaeb36"  # Replace with your API key
API_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print(f"Producer started, streaming weather data for {CITY}...")

while True:
    try:
        response = requests.get(API_URL)
        data = response.json()
        
        message = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "temperature": data['main']['temp'],
            "humidity": data['main']['humidity'],
            "pressure": data['main']['pressure'],
            "city": CITY
        }

        producer.send(TOPIC, value=message)
        producer.flush()
        print("Sent:", message)

    except Exception as e:
        print("API Error:", e)
    
    time.sleep(15)  # send every 15 seconds
