import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timezone
from streamlit_autorefresh import st_autorefresh

# -------------------------
# CONFIGURATION
# -------------------------
MONGO_URI = 'mongodb+srv://Patrickcruz:Patrickcruz19@groceryinventorysystem.4owod4l.mongodb.net/?appName=GroceryInventorySystem'
DB_NAME = 'weather_db'
COLLECTION_NAME = 'weather_data'

st.set_page_config(
    page_title="Weather Monitoring System",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------
# MODERN DARK DESIGN CSS
# -------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; color: white; }
    body, .stApp { background-color: #0f111a; }
    #MainMenu, footer, header {visibility: hidden;}
    h1 { font-weight: 800 !important; font-size: 3rem !important; color: #ffffff !important; text-shadow: 2px 2px 6px rgba(0,0,0,0.5);}
    h2,h3 { color: #ffffff !important; font-weight: 700 !important; }
    .stMetric { background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border-radius: 20px; padding: 20px; border:1px solid rgba(255,255,255,0.2);}
    [data-testid="stMetricValue"] { color: #00ffc6 !important; font-size:2.5rem !important; font-weight:800 !important; }
    [data-testid="stMetricLabel"] { color: rgba(255,255,255,0.7); font-weight:600 !important; font-size:1rem !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border-radius:20px; padding:10px; }
    .stTabs [data-baseweb="tab"] { border-radius:15px; color:white; font-weight:600; padding:10px 30px; }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg,#ff6a00 0%,#ee0979 100%); color:white;}
    .stButton>button { background: linear-gradient(135deg,#ff6a00 0%,#ee0979 100%); color:white; border:none; border-radius:15px; padding:12px 30px; font-weight:600; transition: all 0.3s ease;}
    .stButton>button:hover { transform: scale(1.05); box-shadow:0 5px 20px rgba(255,106,0,0.4);}
    .stSelectbox > div > div { background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border-radius:15px; border:1px solid rgba(255,255,255,0.2); color:white;}
    div[data-testid="stDataFrame"] { background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border-radius:15px; padding:10px;}
    .stAlert { background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border-radius:15px; border:1px solid rgba(255,255,255,0.2);}
</style>
""", unsafe_allow_html=True)

# -------------------------
# MONGO CONNECTION
# -------------------------
@st.cache_resource
def get_mongo_client():
    return MongoClient(MONGO_URI)

client = get_mongo_client()
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# -------------------------
# DATA FUNCTIONS
# -------------------------
def parse_timestamp(ts):
    try:
        return pd.to_datetime(float(ts), unit='s')
    except:
        try:
            return pd.to_datetime(ts, utc=True)
        except:
            return pd.NaT

def fetch_latest_data():
    data = collection.find({}, {'_id': 0}).sort("timestamp", -1).limit(1)
    data_list = list(data)
    return data_list[0] if data_list else None

def fetch_recent_data(limit=100):
    data = collection.find({}, {'_id': 0}).sort("timestamp", -1).limit(limit)
    df = pd.DataFrame(list(data))
    if not df.empty and 'timestamp' in df.columns:
        df['timestamp'] = df['timestamp'].apply(parse_timestamp)
        df = df.dropna(subset=['timestamp'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df.sort_values('timestamp')
    return pd.DataFrame()

def fetch_recent_data_rolling(window=5, limit=100):
    df = fetch_recent_data(limit=limit)
    if df.empty:
        return df
    numeric_cols = ['temperature', 'humidity', 'pressure', 'wind_speed', 'cloudiness']
    for col in numeric_cols:
        if col in df.columns:
            df[f'{col}_avg'] = df[col].rolling(window=window, min_periods=1).mean()
    return df

def fetch_all_data():
    data = collection.find({}, {'_id': 0}).sort("timestamp", -1)
    df = pd.DataFrame(list(data))
    if not df.empty and 'timestamp' in df.columns:
        df['timestamp'] = df['timestamp'].apply(parse_timestamp)
        df = df.dropna(subset=['timestamp'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

# -------------------------
# DISPLAY FUNCTIONS
# -------------------------
def display_header():
    col1,col2 = st.columns([3,1])
    with col1:
        st.markdown("# 🌤️ Weather Monitoring System")
        st.markdown("### Real-time Data Streaming • Quezon City, Philippines")
    with col2:
        if st.button("📥 Export Data"):
            export_data()

def export_data():
    df = fetch_all_data()
    if not df.empty:
        csv = df.to_csv(index=False)
        st.download_button(label="📄 Download CSV", data=csv, file_name=f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", mime="text/csv")
        st.success("✅ Data ready for download!")
    else:
        st.error("❌ No data available to export")

def display_live_status():
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(0,255,198,0.1), rgba(0,255,198,0.2));
                padding:15px; border-radius:15px; border:1px solid rgba(0,255,198,0.3); margin-bottom:20px;'>
        <span style='color:#00ffc6; font-weight:600; font-size:1.1rem;'>
            🟢 Live • Data Streaming Active • Auto-refreshing every 15 seconds
        </span>
    </div>
    """, unsafe_allow_html=True)

def display_live_view():
    st.markdown("## 📊 Live Streaming Dashboard")
    display_live_status()
    
    latest = fetch_latest_data()
    recent_df = fetch_recent_data_rolling(window=5, limit=100)

    if latest:
        col1,col2,col3,col4 = st.columns(4)
        
        with col1:
            temp = latest.get('temperature', 'N/A')
            if temp != 'N/A' and not recent_df.empty:
                delta_temp = f"{(temp - recent_df['temperature_avg'].mean()):.1f}°C"
                st.metric("🌡️ Temperature", f"{temp:.1f}°C", delta=delta_temp)
            else:
                st.metric("🌡️ Temperature", "N/A")
                
        with col2:
            hum = latest.get('humidity', 'N/A')
            if hum != 'N/A' and not recent_df.empty:
                delta_hum = f"{(hum - recent_df['humidity_avg'].mean()):.0f}%"
                st.metric("💧 Humidity", f"{hum:.0f}%", delta=delta_hum)
            else:
                st.metric("💧 Humidity", "N/A")
                
        with col3:
            pres = latest.get('pressure', 'N/A')
            if pres != 'N/A' and not recent_df.empty:
                delta_pres = f"{(pres - recent_df['pressure_avg'].mean()):.0f}"
                st.metric("🔽 Pressure", f"{pres:.0f} hPa", delta=delta_pres)
            else:
                st.metric("🔽 Pressure", "N/A")
                
        with col4:
            ts = parse_timestamp(latest.get('timestamp'))
            if ts is not pd.NaT:
                now_utc = datetime.now(timezone.utc)
                if ts.tzinfo is not None:
                    now_utc = now_utc.astimezone(ts.tzinfo)
                diff = now_utc - ts
                st.metric("⏰ Last Update", f"{int(diff.total_seconds())}s ago", 
                          delta=ts.strftime('%H:%M:%S'))
            else:
                st.metric("⏰ Last Update", "N/A", delta="")

        st.markdown("<br>", unsafe_allow_html=True)

        # Temperature Trend Graph
        if not recent_df.empty and 'temperature_avg' in recent_df.columns:
            st.markdown("### 📈 Temperature Trend")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=recent_df['timestamp'], y=recent_df['temperature_avg'],
                                     mode='lines+markers', name='Temperature',
                                     line=dict(color='#ff6a00', width=3), marker=dict(size=6),
                                     fill='tozeroy', fillcolor='rgba(255,106,0,0.1)'))
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              font=dict(color='white'),
                              xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                              yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title='°C'),
                              height=400, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig)

def display_historical_view():
    st.markdown("## 📊 Historical Data Analysis")
    df = fetch_all_data()
    if not df.empty:
        st.metric("📊 Total Records", len(df))
        st.dataframe(df.sort_values('timestamp', ascending=False), width='stretch')
        
        if len(df) > 1:
            col1, col2 = st.columns(2)
            with col1:
                if 'temperature' in df.columns:
                    st.markdown("### 🌡️ Temperature Over Time")
                    fig_temp = px.line(df, x='timestamp', y='temperature', color_discrete_sequence=['#ff6a00'])
                    fig_temp.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                           font=dict(color='white'), showlegend=False)
                    st.plotly_chart(fig_temp)
            with col2:
                if 'humidity' in df.columns:
                    st.markdown("### 💧 Humidity Over Time")
                    fig_hum = px.line(df, x='timestamp', y='humidity', color_discrete_sequence=['#00ffc6'])
                    fig_hum.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                          font=dict(color='white'), showlegend=False)
                    st.plotly_chart(fig_hum)
    else:
        st.warning("No historical data available")

# -------------------------
# MAIN FUNCTION
# -------------------------
def main():
    # Auto-refresh every 15 seconds
    st_autorefresh(interval=15_000, key="live_refresh")
    
    display_header()
    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔴 Live Streaming", "📊 Historical Data"])
    with tab1: 
        display_live_view()
    with tab2: 
        display_historical_view()

if __name__ == "__main__":
    main()
