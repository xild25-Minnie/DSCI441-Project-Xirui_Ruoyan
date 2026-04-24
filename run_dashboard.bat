@echo off
REM Supplement Sales Forecast Dashboard - Windows Quick Start Script

echo ==================================
echo Supplement Sales Forecast Dashboard
echo ==================================
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Launch application
echo Launching application...
echo Access URL: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo ==================================
echo.

streamlit run app/streamlit_app.py

pause