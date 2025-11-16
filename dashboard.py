import streamlit as st
from pymongo import MongoClient
import pandas as pd
import time

# -------------------------
# CONFIGURATION
# -------------------------
MONGO_URI = 'mongodb+srv://Patrickcruz:Patrickcruz19@groceryinventorysystem.4owod4l.mongodb.net/?appName=GroceryInventorySystem'
DB_NAME = 'weather_db'
COLLECTION_NAME = 'weather_data'

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

st.title("Live Weather Dashboard - Quezon City")

# Refresh interval
REFRESH_INTERVAL = 15  # seconds

# Container to hold the data
data_placeholder = st.empty()

def parse_timestamp(ts):
    """Convert timestamps to pandas datetime, handling both Unix and ISO formats."""
    try:
        # If numeric, treat as Unix timestamp
        return pd.to_datetime(float(ts), unit='s')
    except:
        # Otherwise assume ISO 8601 string
        return pd.to_datetime(ts)

while True:
    # Fetch all data from MongoDB
    data_cursor = collection.find().sort("timestamp", -1)  # newest first
    data_list = list(data_cursor)
    
    if data_list:
        # Convert to DataFrame
        df = pd.DataFrame(data_list)
        # Parse timestamps safely
        df['timestamp'] = df['timestamp'].apply(parse_timestamp)
        
        with data_placeholder.container():
            st.subheader("Latest Weather Data")
            st.write(df.head(1))  # show the latest record
            
            st.subheader("History")
            st.dataframe(df)  # show all historical data
    else:
        with data_placeholder.container():
            st.write("No data available yet.")
    
    time.sleep(REFRESH_INTERVAL)
