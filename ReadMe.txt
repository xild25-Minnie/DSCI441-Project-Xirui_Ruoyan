# Supplement Sales Forecast Dashboard

This is your GitHub README. See the next section for details.

## Project Overview

This is a machine learning-based sales forecasting system that uses three different models (Linear Regression, Random Forest, and LightGBM) to predict supplement sales volume. The application provides an interactive Streamlit dashboard for viewing model performance and sales forecasts in real time.

## Quick Start

### Prerequisites
- Python 3.8 or later
- pip package manager

### Installation

1. Clone or download this repository:
   ```
   git clone https://github.com/xild25-Minnie/DSCI441-Project-Xirui_Ruoyan.git
   cd DSCI441-Project-Xirui_Ruoyan
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Running the Application

#### Option 1: Using Startup Scripts (Recommended)
- **Linux/Mac**: `bash run_dashboard.sh`
- **Windows**: `run_dashboard.bat`

#### Option 2: Manual Start
```
streamlit run app/streamlit_app.py
```

3. Open your browser and navigate to `http://localhost:8501` (should open automatically).

## Features

### 1. Model Performance Analysis
- Performance comparison of three models: Linear Regression, Random Forest, and LightGBM
- Key metrics display: MAE, RMSE, R², and MAPE
- Radar chart visualization of model performance
- Supports switching between validation and test sets

### 2. Sales Forecast Overview
- Sales forecast comparison by product
- Sales forecast by category, platform, and location
- Multi-model comparison display

### 3. Prediction Analysis
- Prediction error distribution analysis
- Error percentage analysis
- Actual vs. predicted scatter plots
- Prediction accuracy visualization with color coding

### 4. Time Series Forecasting
- Multidimensional filters (product, category, platform)
- Time series forecast curves
- Detailed time series analysis by product
- Comparison between actual and predicted values

## Project Structure

```
DSCI441-Project-Xirui_Ruoyan/
├── app/
│   └── streamlit_app.py          # Main application file
├── notebooks/
│   ├── code.ipynb                 # Complete analysis and model training code
│   └── Supplement_Sales_Strong_Correlation.csv  # Original data
├── src/
│   └── final_code.py              # Optional Python module
├── data/
│   ├── readme_data.txt            # Data documentation
│   └── Supplement_Sales_Weekly_Expanded.csv  # Expanded data
├── requirements.txt               # Project dependencies
├── run_dashboard.sh               # Linux/Mac startup script
├── run_dashboard.bat              # Windows startup script
├── QUICK_START.md                 # Quick reference guide
├── DASHBOARD_README.md            # Complete documentation
├── COMPLETION_SUMMARY.md          # Implementation summary
└── README.md                      # This file
```

## Data Description

### Original Data Columns
- **Date**: Sales date
- **Product Name**: Product name
- **Category**: Product category
- **Location**: Sales location
- **Platform**: Sales platform
- **Units Sold**: Sales volume (target variable)
- **Price**: Product price
- **Discount**: Discount applied
- **Units Returned**: Returned units
- **Revenue**: Revenue generated

### Feature Engineering
- Calendar features: year, month, quarter, weekofyear
- Lag features: units_sold_lag1, units_sold_lag2, units_sold_lag4, price_lag1, discount_lag1
- Rolling features: units_sold_rollmean_4, units_sold_rollstd_4
- Categorical features: Product Name, Category, Location, Platform

## Model Description

### 1. Linear Regression
- Baseline model
- Fast inference and easy to interpret
- Suitable for capturing linear relationships

### 2. Random Forest
- Ensemble learning method
- Can capture nonlinear relationships
- Requires parameter tuning to avoid overfitting

### 3. LightGBM
- Gradient boosting tree model
- Usually delivers the best performance
- Efficient and fast

## Key Metrics

| Metric | Meaning | Range |
|--------|---------|-------|
| MAE | Mean Absolute Error | Lower is better |
| RMSE | Root Mean Squared Error | Lower is better |
| R² | Coefficient of Determination | 0 to 1, higher is better |
| MAPE | Mean Absolute Percentage Error | Percentage, lower is better |

## Technology Stack

- **Framework**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn, LightGBM
- **Visualization**: Plotly
- **Statistics**: SciPy

## Usage Recommendations

1. **Model Selection**: Prioritize test set metrics. Models with higher R² and lower RMSE perform better.
2. **Data Exploration**: Use the Time Series page to observe seasonal patterns.
3. **Business Applications**: Use predictions for inventory planning and identify high-error combinations.

## Troubleshooting

### ModuleNotFoundError
```
pip install -r requirements.txt
```

### Slow Application Start
The first run trains all models. Subsequent runs will be faster due to caching.

### File Not Found Error
Ensure you're in the correct directory:
```
pwd
# Should output: .../DSCI441-Project-Xirui_Ruoyan
```

Check data file:
```
ls notebooks/Supplement_Sales_Strong_Correlation.csv
```

### Charts Not Displaying
1. Refresh the browser
2. Clear browser cache
3. Check network connection (Plotly needs internet for rendering)

## Dependencies

The following packages are required (see `requirements.txt`):

- pandas >= 1.3.0
- numpy >= 1.21.0
- matplotlib >= 3.4.0
- seaborn >= 0.11.0
- scipy >= 1.7.0
- scikit-learn >= 1.0.0
- lightgbm >= 3.3.0
- plotly >= 5.0.0
- streamlit >= 1.20.0

## Contributing

For questions or suggestions, refer to the code comments or the detailed analysis in `notebooks/code.ipynb`.

Last Updated: April 25, 2026