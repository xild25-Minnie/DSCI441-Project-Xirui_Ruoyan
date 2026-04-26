#!/bin/bash

# Supplement Sales Forecast Dashboard - Quick Start Script

echo "=================================="
echo "Supplement Sales Forecast Dashboard"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python --version
echo ""

# Check dependencies
echo "Checking dependencies..."
pip list | grep -E "(streamlit|plotly|pandas|scikit-learn|lightgbm)" || echo "Some dependencies are not installed"
echo ""

# Launch application
echo "Launching application..."
echo "Access URL: http://localhost:8501"
echo ""
echo "Opening browser..."

nohup python -m streamlit run app/streamlit_app.py --server.port 8501 > streamlit.log 2>&1 &
STREAMLIT_PID=$!

sleep 3
python3 -m webbrowser open "http://localhost:8501" 2>/dev/null || xdg-open "http://localhost:8501" 2>/dev/null || echo "Please open your browser manually: http://localhost:8501"

echo "Streamlit started with PID $STREAMLIT_PID"
echo "Press Ctrl+C to stop the application"
echo "=================================="

tail -f streamlit.log &
wait $STREAMLIT_PID