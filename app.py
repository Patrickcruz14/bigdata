"""
Streaming Data Dashboard
STUDENT PROJECT: Big Data Streaming Dashboard
Modified to fetch historical data from MongoDB
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime, timedelta
from pymongo import MongoClient
from streamlit_autorefresh import st_autorefresh

# Page configuration
st.set_page_config(
    page_title="Streaming Data Dashboard",
    page_icon="\U0001f4ca",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Sidebar Configuration ----------
def setup_sidebar():
    st.sidebar.title("Dashboard Controls")
    st.sidebar.subheader("MongoDB Configuration")
    st.sidebar.text("Using your MongoDB connection for historical data")
    
    return {
        "mongodb_uri": "mongodb+srv://Patrickcruz:Patrickcruz19@groceryinventorysystem.4owod4l.mongodb.net/?appName=GroceryInventorySystem",
        "database": "test",       # replace with your DB name
        "collection": "sensor_data"  # replace with your collection name
    }

# ---------- Sample Data for Real-time ----------
def generate_sample_data():
    current_time = datetime.now()
    times = [current_time - timedelta(minutes=i) for i in range(100, 0, -1)]
    sample_data = pd.DataFrame({
        'timestamp': times,
        'value': [100 + i * 0.5 + (i % 10) for i in range(100)],
        'metric_type': ['temperature'] * 100,
        'sensor_id': ['sensor_1'] * 100
    })
    return sample_data

# ---------- Historical Data from MongoDB ----------
def query_historical_data(time_range="1h", metrics=None, config=None):
    try:
        client = MongoClient(config["mongodb_uri"])
        db = client.get_database(config["database"])
        collection = db.get_collection(config["collection"])

        query = {}
        if metrics:
            query["metric_type"] = {"$in": metrics}

        data = list(collection.find(query))
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df

    except Exception as e:
        st.error(f"Error fetching historical data: {e}")
        return pd.DataFrame()

# ---------- Real-time Streaming View ----------
def display_real_time_view(refresh_interval):
    st.header("\U0001f4c8 Real-time Streaming Dashboard")
    
    # Auto-refresh info
    st.info(f"Auto-refresh every {refresh_interval} seconds")
    
    # Fetch sample data
    with st.spinner("Fetching real-time data..."):
        real_time_data = generate_sample_data()
    
    # Metrics
    if not real_time_data.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Records Received", len(real_time_data))
        with col2:
            st.metric("Latest Value", f"{real_time_data['value'].iloc[-1]:.2f}")
        with col3:
            st.metric("Data Range", f"{real_time_data['timestamp'].min().strftime('%H:%M')} - {real_time_data['timestamp'].max().strftime('%H:%M')}")

        # Real-time chart
        fig = px.line(
            real_time_data,
            x='timestamp',
            y='value',
            title=f"Real-time Data Stream (Last {len(real_time_data)} records)",
            labels={'value': 'Sensor Value', 'timestamp': 'Time'},
            template='plotly_white'
        )
        st.plotly_chart(fig, width='stretch')

        # Raw data table
        with st.expander("\U0001f4cb View Raw Data"):
            st.dataframe(real_time_data.sort_values('timestamp', ascending=False), height=300)

# ---------- Historical Data View ----------
def display_historical_view(config):
    st.header("\U0001f4ca Historical Data Analysis")

    st.subheader("Data Filters")
    col1, col2 = st.columns(2)
    with col1:
        metric_type = st.selectbox(
            "Metric Type",
            ["temperature", "humidity", "pressure", "all"]
        )
    with col2:
        aggregation = st.selectbox(
            "Aggregation",
            ["raw", "hourly", "daily"]
        )

    metrics = [metric_type] if metric_type != "all" else None
    historical_data = query_historical_data(metrics=metrics, config=config)

    if not historical_data.empty:
        st.subheader("Historical Data Table")
        st.dataframe(historical_data, hide_index=True)

        st.subheader("Historical Trends")
        fig = px.line(
            historical_data,
            x='timestamp',
            y='value',
            title="Historical Trend"
        )
        st.plotly_chart(fig, width='stretch')

        st.subheader("Data Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Records", len(historical_data))
            st.metric("Date Range", f"{historical_data['timestamp'].min().strftime('%Y-%m-%d')} to {historical_data['timestamp'].max().strftime('%Y-%m-%d')}")
        with col2:
            st.metric("Average Value", f"{historical_data['value'].mean():.2f}")
            st.metric("Data Variability", f"{historical_data['value'].std():.2f}")
    else:
        st.warning("No historical data available")

# ---------- Main App ----------
def main():
    st.title("\U0001f680 Streaming Data Dashboard")

    config = setup_sidebar()

    # Auto-refresh control
    refresh_interval = st.sidebar.slider(
        "Refresh Interval (seconds)",
        min_value=5,
        max_value=60,
        value=15
    )
    st_autorefresh(interval=refresh_interval * 1000, key="auto_refresh")

    # Tabs for views
    tab1, tab2 = st.tabs(["\U0001f4c8 Real-time Streaming", "\U0001f4ca Historical Data"])

    with tab1:
        display_real_time_view(refresh_interval)

    with tab2:
        display_historical_view(config)

if __name__ == "__main__":
    main()
