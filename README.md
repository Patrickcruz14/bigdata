# 🚀 Streaming Data Dashboard: Project Guide

This project requires building a big data streaming dashboard using **Kafka** and **Streamlit**, featuring separate real-time and historical data views.

## 🎯 Architecture & Components

A **dual-pipeline** architecture separates live streaming from long-term storage and analysis.

| Pipeline | Flow | Output |
| :--- | :--- | :--- |
| **Real-time** | Kafka $\rightarrow$ Streamlit (Live Consumer) | `📈 Real-time Streaming View` |
| **Historical** | Kafka $\rightarrow$ **HDFS OR MongoDB** $\rightarrow$ Streamlit (Query) | `📊 Historical Data View` |

### Mandatory Components
* Kafka Producer/Consumer.
* **HDFS or MongoDB** integration.
* Two-page Streamlit dashboard with charts.
* Robust error handling.

---

## 💻 Technical Implementation Tasks

### 1. Data Producer (`producer.py`)
Create a Kafka Producer that fetches real data from an **existing Application Programming Interface (API)** (e.g., a public weather API, stock market API, etc.).

**Required Data Schema Fields:**
* `timestamp` (ISO format)
* `value` (Numeric)
* `metric_type` (String)
* `sensor_id` (String)

### 2. Dashboard (`app.py`)
Implement the Streamlit logic:
* `consume_kafka_data()`: Real-time processing.
* `query_historical_data()`: Data retrieval from storage.
* Create interactive widgets (filters, time-range selector) for the Historical View.

### 3. Storage Integration
Implement data writing and querying for **ONE** of the following: **HDFS** or **MongoDB**.

---

## 🏃‍♂️ Setup & Execution

### Prerequisites
Python 3.8+, Apache Kafka, HDFS **OR** MongoDB.

### Setup
1. **Setup environment**
    - Download miniconda
    - Create your python environment
    ```bash
    conda create -n bigdata python=3.10.13
    ```
2.  **Clone Repo & Install:**
    ```bash
    git clone [REPO_URL]
    conda activate bigdata
    pip install -r requirements.txt
    ```
3.  **Configure:** Set up Kafka and your chosen Storage System.
4.  **Optional Environment File (`.env`):** Use for connection details.

### Execution
1.  **Start Kafka Broker** (and Controller).
2.  **Start Producer:**
    ```bash
    python producer.py
    ```
3.  **Launch Dashboard:**
    ```bash
    streamlit run app.py
    ```

---

## 📦 Deliverables
Submit the following files:
* `app.py`
* `producer.py`
* `requirements.txt`
* `README.md`