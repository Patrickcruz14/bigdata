# This file contains all required packages for both the Streamlit dashboard and Kafka producer
streamlit>=1.28.0  # Modern web framework for building data applications
streamlit-autorefresh
pandas>=2.0.0      # Data manipulation and analysis library
numpy>=1.24.0      # Numerical computing and array operations
plotly>=5.15.0     # Interactive plotting library for charts and graphs
kafka-python>=2.0.2  # Apache Kafka Python client for both producer and consumer
python-dateutil>=2.8.2  # Extended date/time utilities (used by pandas)

# Optional: Storage Systems (uncomment based on your chosen storage)
# pyarrow>=12.0.0      # Apache Arrow for HDFS integration
# pymongo>=4.5.0       # MongoDB driver for NoSQL storage

# Optional: Additional Data Science Libraries
# scipy>=1.10.0        # Scientific computing and advanced statistics
# scikit-learn>=1.3.0  # Machine learning algorithms
# matplotlib>=3.7.0    # Static, animated, and interactive visualizations

# Development & Testing
pytest>=7.4.0      # Testing framework for unit tests
black>=23.0.0      # Code formatter for consistent code style
flake8>=6.0.0      # Linter for code quality checks

# Note: Some packages may have additional system dependencies
# For Windows users, ensure you have Microsoft Visual C++ Build Tools installed
# For Linux/macOS, ensure you have build-essential/developer tools installed