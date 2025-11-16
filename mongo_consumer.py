from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# -------------------------
# CONFIGURATION
# -------------------------
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'weather_topic'
MONGO_URI = 'mongodb+srv://Patrickcruz:Patrickcruz19@groceryinventorysystem.4owod4l.mongodb.net/?appName=GroceryInventorySystem'
DB_NAME = 'weather_db'
COLLECTION_NAME = 'weather_data'

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Kafka consumer
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    enable_auto_commit=True
)

print("Consumer started, saving data to MongoDB...")

for message in consumer:
    data = message.value
    collection.insert_one(data)
    print("Saved to MongoDB:", data)
