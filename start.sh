#!/bin/bash
# Streamlit start script for Render deployment

echo "========================================="
echo "   TRM NIRVANA - STREAMLIT STARTING"
echo "========================================="

# Start Streamlit app
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0