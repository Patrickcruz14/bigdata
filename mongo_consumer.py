from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# -------------------------
# CONFIGURATION
# -------------------------
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'weather-data'
MONGO_URI = 'mongodb+srv://Patrickcruz:Patrickcruz19@groceryinventorysystem.4owod4l.mongodb.net/?appName=GroceryInventorySystem'
DB_NAME = 'weather_db'
COLLECTION_NAME = 'weather_data'

print("🔧 Starting MongoDB Consumer...")

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    client.admin.command('ping')
    print(f"✅ MongoDB connected! Initial documents: {collection.count_documents({})}")

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest',
        enable_auto_commit=True
    )
    print("✅ Kafka Consumer connected!\nWaiting for messages...\n")
except Exception as e:
    print(f"❌ Initialization failed: {e}")
    exit(1)

for message in consumer:
    data = message.value
    collection.insert_one(data)
    print(f"💾 Saved: {data['timestamp']} | Temp: {data['temperature']}°C | Total: {collection.count_documents({})}")
