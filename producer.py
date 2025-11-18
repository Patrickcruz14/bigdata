import json
import time
from datetime import datetime
import random
import requests
from kafka import KafkaProducer
from kafka.errors import KafkaError

# -------------------------
# CONFIGURATION
# -------------------------
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'weather-data'
CITY = "Quezon City"
API_KEY = "35034f2ecfa458f14d42d46218eaeb36"
API_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# Create Kafka producer
try:
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        acks='all',
        retries=3,
        max_in_flight_requests_per_connection=1
    )
    print(f"✅ Kafka Producer connected to {KAFKA_BROKER}")
    print(f"📡 Streaming weather data for {CITY} to topic '{TOPIC}'")
    print(f"⏱️  Sending data every 15 seconds...\n")
except KafkaError as e:
    print(f"❌ Failed to connect to Kafka: {e}")
    exit(1)

message_count = 0

while True:
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Add small random noise to simulate variation
        temp_noise = random.uniform(-0.5, 0.5)
        feels_like_noise = random.uniform(-0.5, 0.5)

        message = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "temperature": round(data['main']['temp'] + temp_noise, 2),
            "feels_like": round(data['main']['feels_like'] + feels_like_noise, 2),
            "humidity": data['main']['humidity'],
            "pressure": data['main']['pressure'],
            "wind_speed": round(data['wind']['speed'] * 3.6, 2),
            "wind_direction": data['wind'].get('deg', 0),
            "visibility": data.get('visibility', 10000) / 1000,
            "condition": data['weather'][0]['main'],
            "description": data['weather'][0]['description'],
            "location": CITY,
            "country": data['sys']['country'],
            "sunrise": datetime.fromtimestamp(data['sys']['sunrise']).isoformat() + "Z",
            "sunset": datetime.fromtimestamp(data['sys']['sunset']).isoformat() + "Z",
            "cloudiness": data['clouds']['all']
        }

        future = producer.send(TOPIC, value=message)

        try:
            record_metadata = future.get(timeout=10)
            message_count += 1
            print(f"📤 Message #{message_count} sent: Temp {message['temperature']}°C")
        except KafkaError as e:
            print(f"❌ Failed to send message: {e}\n")

    except requests.exceptions.RequestException as e:
        print(f"🌐 API Request Error: {e}\n")
    except KeyError as e:
        print(f"📊 Data parsing error - missing key: {e}\n")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}\n")

    time.sleep(15)
