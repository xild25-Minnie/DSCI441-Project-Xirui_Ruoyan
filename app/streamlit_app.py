import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import sys
import os
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Supplement Sales Forecast Dashboard",
    #page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# STYLING
# ============================================================================
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .main-header {
        color: #1f77b4;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .section-header {
        color: #ff7f0e;
        font-size: 20px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD DATA AND MODELS (CACHED)
# ============================================================================
@st.cache_resource
def load_data_and_models():
    """Load data and trained models"""
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.pipeline import Pipeline
    from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import RandomForestRegressor
    from lightgbm import LGBMRegressor
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    import pickle
    
    # Load data
    data_path = os.path.join(os.path.dirname(__file__), '../notebooks/Supplement_Sales_Strong_Correlation.csv')
    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by=['Product Name', 'Date'])
    
    # Feature engineering
    def create_time_series_features(df):
        df['units_sold_lag1'] = df.groupby('Product Name')['Units Sold'].shift(1)
        df['units_sold_lag2'] = df.groupby('Product Name')['Units Sold'].shift(2)
        df['units_sold_lag4'] = df.groupby('Product Name')['Units Sold'].shift(4)
        
        df['price_lag1'] = df.groupby('Product Name')['Price'].shift(1)
        df['discount_lag1'] = df.groupby('Product Name')['Discount'].shift(1)
        
        df['units_sold_rollmean_4'] = df.groupby('Product Name')['Units Sold'].transform(
            lambda x: x.shift(1).rolling(window=4).mean()
        )
        df['units_sold_rollstd_4'] = df.groupby('Product Name')['Units Sold'].transform(
            lambda x: x.shift(1).rolling(window=4).std()
        )
        
        df['year'] = df['Date'].dt.year
        df['month'] = df['Date'].dt.month
        df['quarter'] = df['Date'].dt.quarter
        df['weekofyear'] = df['Date'].dt.isocalendar().week.astype(int)
        
        df = df.dropna().reset_index(drop=True)
        return df
    
    final_df = create_time_series_features(df)
    
    # Data split
    max_date = final_df['Date'].max()
    test_cutoff = max_date - pd.Timedelta(weeks=12)
    valid_cutoff = test_cutoff - pd.Timedelta(weeks=12)
    
    train_df = final_df[final_df['Date'] <= valid_cutoff].copy()
    valid_df = final_df[(final_df['Date'] > valid_cutoff) & (final_df['Date'] <= test_cutoff)].copy()
    test_df = final_df[final_df['Date'] > test_cutoff].copy()
    
    feature_cols = [
        "Product Name", "Category", "Location", "Platform",
        "Price", "Discount", "year", "month", "quarter", "weekofyear",
        "units_sold_lag1", "units_sold_lag2", "units_sold_lag4",
        "units_sold_rollmean_4", "units_sold_rollstd_4",
        "price_lag1", "discount_lag1"
    ]
    target_col = "Units Sold"
    
    X_train = train_df[feature_cols]
    y_train = train_df[target_col]
    X_valid = valid_df[feature_cols]
    y_valid = valid_df[target_col]
    X_test = test_df[feature_cols]
    y_test = test_df[target_col]
    
    # Preprocessor
    categorical_features = ["Product Name", "Category", "Location", "Platform"]
    numeric_features = [col for col in feature_cols if col not in categorical_features]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", StandardScaler(), numeric_features)
        ]
    )
    
    # Train models
    # Linear Regression
    linear_model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", LinearRegression())
    ])
    linear_model.fit(X_train, y_train)
    
    # Random Forest
    rf_model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1
        ))
    ])
    rf_model.fit(X_train, y_train)
    
    # LightGBM
    lgbm_model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", LGBMRegressor(
            n_estimators=100,
            learning_rate=0.05,
            max_depth=5,
            num_leaves=31,
            random_state=42,
            verbose=-1
        ))
    ])
    lgbm_model.fit(X_train, y_train)
    
    # Get predictions
    valid_pred_lr = linear_model.predict(X_valid)
    valid_pred_rf = rf_model.predict(X_valid)
    valid_pred_lgbm = lgbm_model.predict(X_valid)
    
    test_pred_lr = linear_model.predict(X_test)
    test_pred_rf = rf_model.predict(X_test)
    test_pred_lgbm = lgbm_model.predict(X_test)
    
    return {
        'final_df': final_df,
        'train_df': train_df,
        'valid_df': valid_df,
        'test_df': test_df,
        'X_valid': X_valid,
        'y_valid': y_valid,
        'X_test': X_test,
        'y_test': y_test,
        'valid_pred_lr': valid_pred_lr,
        'valid_pred_rf': valid_pred_rf,
        'valid_pred_lgbm': valid_pred_lgbm,
        'test_pred_lr': test_pred_lr,
        'test_pred_rf': test_pred_rf,
        'test_pred_lgbm': test_pred_lgbm,
        'feature_cols': feature_cols,
    }

# Load data
with st.spinner('Loading data and models...'):
    data = load_data_and_models()

# ============================================================================
# CALCULATE METRICS
# ============================================================================
def calculate_metrics(y_true, y_pred):
    """Calculate evaluation metrics"""
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    return {'MAE': mae, 'RMSE': rmse, 'R²': r2, 'MAPE': mape}

# Validation set metrics
valid_metrics_lr = calculate_metrics(data['y_valid'], data['valid_pred_lr'])
valid_metrics_rf = calculate_metrics(data['y_valid'], data['valid_pred_rf'])
valid_metrics_lgbm = calculate_metrics(data['y_valid'], data['valid_pred_lgbm'])

# Test set metrics
test_metrics_lr = calculate_metrics(data['y_test'], data['test_pred_lr'])
test_metrics_rf = calculate_metrics(data['y_test'], data['test_pred_rf'])
test_metrics_lgbm = calculate_metrics(data['y_test'], data['test_pred_lgbm'])

# ============================================================================
# HEADER
# ============================================================================
col1, col2 = st.columns([1, 3])
with col1:
    st.text("")
    st.text("")
    st.text("")
    st.markdown("**Supplement Sales**")
with col2:
    st.markdown("""
    <h1 style='color: #1f77b4; margin: 0;'>Sales Forecast Dashboard</h1>
    <p style='color: #666; margin: 0;'>Machine learning-based multi-model sales volume forecasting system</p>
    """, unsafe_allow_html=True)

st.divider()

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
with st.sidebar:
    st.markdown("### Navigation Menu")
    page = st.radio("Select page:", 
        options=["Model Performance", "Sales Forecast", "Prediction Analysis", "Time Series"],
        label_visibility="collapsed"
    )

# ============================================================================
# PAGE 1: MODEL PERFORMANCE
# ============================================================================
if page == "Model Performance":
    st.markdown("<h2 class='section-header'> Model Performance Comparison</h2>", unsafe_allow_html=True)
    
    # Select dataset
    dataset = st.radio("Select dataset:", options=["Validation Set", "Test Set"], horizontal=True)
    
    if dataset == "Validation Set":
        metrics_lr, metrics_rf, metrics_lgbm = valid_metrics_lr, valid_metrics_rf, valid_metrics_lgbm
    else:
        metrics_lr, metrics_rf, metrics_lgbm = test_metrics_lr, test_metrics_rf, test_metrics_lgbm
    
    # Create metrics comparison table
    metrics_table = pd.DataFrame({
        'Linear Regression': metrics_lr,
        'Random Forest': metrics_rf,
        'LightGBM': metrics_lgbm
    }).T
    
    # Color coding (lower is better)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Number of Models", "3")
    with col2:
        best_mae_model = metrics_table['MAE'].idxmin()
        st.metric("Best MAE", f"{metrics_table['MAE'].min():.2f}", f"({best_mae_model})")
    with col3:
        best_rmse_model = metrics_table['RMSE'].idxmin()
        st.metric("Best RMSE", f"{metrics_table['RMSE'].min():.2f}", f"({best_rmse_model})")
    with col4:
        best_r2_model = metrics_table['R²'].idxmax()
        st.metric("Best R²", f"{metrics_table['R²'].max():.4f}", f"({best_r2_model})")
    
    st.divider()
    
    # Detailed metrics table
    st.markdown("#### Detailed Model Metrics")
    st.dataframe(
        metrics_table.round(4),
        use_container_width=True,
        column_config={
            "MAE": st.column_config.NumberColumn(format="%.4f"),
            "RMSE": st.column_config.NumberColumn(format="%.4f"),
            "R²": st.column_config.NumberColumn(format="%.6f"),
            "MAPE": st.column_config.NumberColumn(format="%.2f%%"),
        }
    )
    
    st.divider()
    
    # Performance visualization
    col1, col2 = st.columns(2)
    
    with col1:
        # RMSE comparison
        fig_rmse = go.Figure(data=[
            go.Bar(
                x=['Linear Regression', 'Random Forest', 'LightGBM'],
                y=[metrics_lr['RMSE'], metrics_rf['RMSE'], metrics_lgbm['RMSE']],
                marker=dict(
                    color=['#1f77b4', '#ff7f0e', '#2ca02c'],
                    opacity=0.7
                ),
                text=[f"{metrics_lr['RMSE']:.2f}", f"{metrics_rf['RMSE']:.2f}", f"{metrics_lgbm['RMSE']:.2f}"],
                textposition='auto',
            )
        ])
        fig_rmse.update_layout(
            title="RMSE Comparison (Lower Is Better)",
            yaxis_title="RMSE",
            height=400,
            template="plotly_white",
            showlegend=False
        )
        st.plotly_chart(fig_rmse, use_container_width=True)
    
    with col2:
        # R² comparison
        fig_r2 = go.Figure(data=[
            go.Bar(
                x=['Linear Regression', 'Random Forest', 'LightGBM'],
                y=[metrics_lr['R²'], metrics_rf['R²'], metrics_lgbm['R²']],
                marker=dict(
                    color=['#1f77b4', '#ff7f0e', '#2ca02c'],
                    opacity=0.7
                ),
                text=[f"{metrics_lr['R²']:.4f}", f"{metrics_rf['R²']:.4f}", f"{metrics_lgbm['R²']:.4f}"],
                textposition='auto',
            )
        ])
        fig_r2.update_layout(
            title="R² Comparison (Higher Is Better)",
            yaxis_title="R² Score",
            height=400,
            template="plotly_white",
            showlegend=False
        )
        st.plotly_chart(fig_r2, use_container_width=True)
    
    st.divider()
    
    # Radar chart for all metrics
    st.markdown("#### Model Performance Radar Chart")
    
    # Normalize metrics for radar chart
    def normalize(val, min_val, max_val):
        if max_val == min_val:
            return 0.5
        return (val - min_val) / (max_val - min_val)
    
    metrics_names = ['MAE', 'RMSE', 'MAPE']
    
    lr_normalized = [
        1 - normalize(metrics_lr['MAE'], min(metrics_lr['MAE'], metrics_rf['MAE'], metrics_lgbm['MAE']), 
                                           max(metrics_lr['MAE'], metrics_rf['MAE'], metrics_lgbm['MAE'])),
        1 - normalize(metrics_lr['RMSE'], min(metrics_lr['RMSE'], metrics_rf['RMSE'], metrics_lgbm['RMSE']), 
                                             max(metrics_lr['RMSE'], metrics_rf['RMSE'], metrics_lgbm['RMSE'])),
        1 - normalize(metrics_lr['MAPE'], min(metrics_lr['MAPE'], metrics_rf['MAPE'], metrics_lgbm['MAPE']), 
                                             max(metrics_lr['MAPE'], metrics_rf['MAPE'], metrics_lgbm['MAPE'])),
        metrics_lr['R²']
    ]
    
    rf_normalized = [
        1 - normalize(metrics_rf['MAE'], min(metrics_lr['MAE'], metrics_rf['MAE'], metrics_lgbm['MAE']), 
                                            max(metrics_lr['MAE'], metrics_rf['MAE'], metrics_lgbm['MAE'])),
        1 - normalize(metrics_rf['RMSE'], min(metrics_lr['RMSE'], metrics_rf['RMSE'], metrics_lgbm['RMSE']), 
                                             max(metrics_lr['RMSE'], metrics_rf['RMSE'], metrics_lgbm['RMSE'])),
        1 - normalize(metrics_rf['MAPE'], min(metrics_lr['MAPE'], metrics_rf['MAPE'], metrics_lgbm['MAPE']), 
                                             max(metrics_lr['MAPE'], metrics_rf['MAPE'], metrics_lgbm['MAPE'])),
        metrics_rf['R²']
    ]
    
    lgbm_normalized = [
        1 - normalize(metrics_lgbm['MAE'], min(metrics_lr['MAE'], metrics_rf['MAE'], metrics_lgbm['MAE']), 
                                              max(metrics_lr['MAE'], metrics_rf['MAE'], metrics_lgbm['MAE'])),
        1 - normalize(metrics_lgbm['RMSE'], min(metrics_lr['RMSE'], metrics_rf['RMSE'], metrics_lgbm['RMSE']), 
                                               max(metrics_lr['RMSE'], metrics_rf['RMSE'], metrics_lgbm['RMSE'])),
        1 - normalize(metrics_lgbm['MAPE'], min(metrics_lr['MAPE'], metrics_rf['MAPE'], metrics_lgbm['MAPE']), 
                                               max(metrics_lr['MAPE'], metrics_rf['MAPE'], metrics_lgbm['MAPE'])),
        metrics_lgbm['R²']
    ]
    
    radar_metrics = ['MAE', 'RMSE', 'MAPE', 'R²']
    
    fig_radar = go.Figure(data=[
        go.Scatterpolar(
            r=lr_normalized,
            theta=radar_metrics,
            fill='toself',
            name='Linear Regression',
            marker=dict(color='#1f77b4')
        ),
        go.Scatterpolar(
            r=rf_normalized,
            theta=radar_metrics,
            fill='toself',
            name='Random Forest',
            marker=dict(color='#ff7f0e')
        ),
        go.Scatterpolar(
            r=lgbm_normalized,
            theta=radar_metrics,
            fill='toself',
            name='LightGBM',
            marker=dict(color='#2ca02c')
        )
    ])
    
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        height=500,
        template="plotly_white"
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# ============================================================================
# PAGE 2: SALES PREDICTION
# ============================================================================
elif page == "Sales Forecast":
    st.markdown("<h2 class='section-header'>Sales Forecast Overview</h2>", unsafe_allow_html=True)
    
    # Prediction comparison data
    test_data = data['test_df'].copy()
    test_data['Actual Sales Volume'] = data['y_test'].values
    test_data['Linear Regression'] = data['test_pred_lr']
    test_data['Random Forest'] = data['test_pred_rf']
    test_data['LightGBM'] = data['test_pred_lgbm']
    
    # Group statistics by product
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Number of Products", test_data['Product Name'].nunique())
    with col2:
        st.metric("Number of Locations", test_data['Location'].nunique())
    with col3:
        st.metric("Number of Platforms", test_data['Platform'].nunique())
    
    st.divider()
    
    # Sales forecast totals by product
    st.markdown("#### Sales Forecast by Product")
    
    product_actual = test_data.groupby('Product Name')['Actual Sales Volume'].sum().sort_values(ascending=False)
    product_lr = test_data.groupby('Product Name')['Linear Regression'].sum()
    product_rf = test_data.groupby('Product Name')['Random Forest'].sum()
    product_lgbm = test_data.groupby('Product Name')['LightGBM'].sum()
    
    fig_product = go.Figure(data=[
        go.Bar(name='Actual Sales Volume', x=product_actual.index, y=product_actual.values, marker=dict(color='#1f77b4')),
        go.Bar(name='Linear Regression', x=product_lr.index, y=product_lr.values, marker=dict(color='#d62728')),
        go.Bar(name='Random Forest', x=product_rf.index, y=product_rf.values, marker=dict(color='#ff7f0e')),
        go.Bar(name='LightGBM', x=product_lgbm.index, y=product_lgbm.values, marker=dict(color='#2ca02c')),
    ])
    
    fig_product.update_layout(
        barmode='group',
        height=400,
        template="plotly_white",
        xaxis_title="Product Name",
        yaxis_title="Sales Volume",
        hovermode='x unified'
    )
    st.plotly_chart(fig_product, use_container_width=True)
    
    st.divider()
    
    # Sales forecast by category
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Sales Forecast by Category")
        category_actual = test_data.groupby('Category')['Actual Sales Volume'].sum().sort_values(ascending=False)
        category_lgbm = test_data.groupby('Category')['LightGBM'].sum()
        
        fig_category = go.Figure(data=[
            go.Bar(name='Actual Sales Volume', x=category_actual.index, y=category_actual.values, marker=dict(color='#1f77b4')),
            go.Bar(name='LightGBM Forecast', x=category_lgbm.index, y=category_lgbm.values, marker=dict(color='#2ca02c')),
        ])
        
        fig_category.update_layout(
            barmode='group',
            height=400,
            template="plotly_white",
            xaxis_title="Category",
            yaxis_title="Sales Volume",
            hovermode='x unified'
        )
        st.plotly_chart(fig_category, use_container_width=True)
    
    with col2:
        st.markdown("#### Sales Forecast by Platform")
        platform_actual = test_data.groupby('Platform')['Actual Sales Volume'].sum().sort_values(ascending=False)
        platform_lgbm = test_data.groupby('Platform')['LightGBM'].sum()
        
        fig_platform = go.Figure(data=[
            go.Bar(name='Actual Sales Volume', x=platform_actual.index, y=platform_actual.values, marker=dict(color='#1f77b4')),
            go.Bar(name='LightGBM Forecast', x=platform_lgbm.index, y=platform_lgbm.values, marker=dict(color='#2ca02c')),
        ])
        
        fig_platform.update_layout(
            barmode='group',
            height=400,
            template="plotly_white",
            xaxis_title="Platform",
            yaxis_title="Sales Volume",
            hovermode='x unified'
        )
        st.plotly_chart(fig_platform, use_container_width=True)
    
    st.divider()
    
    # Sales forecast by location
    st.markdown("#### Sales Forecast by Location")
    location_actual = test_data.groupby('Location')['Actual Sales Volume'].sum().sort_values(ascending=False)
    location_lgbm = test_data.groupby('Location')['LightGBM'].sum()
    
    fig_location = go.Figure(data=[
        go.Bar(name='Actual Sales Volume', x=location_actual.index, y=location_actual.values, marker=dict(color='#1f77b4')),
        go.Bar(name='LightGBM Forecast', x=location_lgbm.index, y=location_lgbm.values, marker=dict(color='#2ca02c')),
    ])
    
    fig_location.update_layout(
        barmode='group',
        height=400,
        template="plotly_white",
        xaxis_title="Location",
        yaxis_title="Sales Volume",
        hovermode='x unified'
    )
    st.plotly_chart(fig_location, use_container_width=True)

# ============================================================================
# PAGE 3: PREDICTION ANALYSIS
# ============================================================================
elif page == "Prediction Analysis":
    st.markdown("<h2 class='section-header'>Detailed Prediction Analysis</h2>", unsafe_allow_html=True)
    
    # Build analysis data
    test_data = data['test_df'].copy()
    test_data['Actual Sales Volume'] = data['y_test'].values
    test_data['Linear Regression'] = data['test_pred_lr']
    test_data['Random Forest'] = data['test_pred_rf']
    test_data['LightGBM'] = data['test_pred_lgbm']
    test_data['LR_Error'] = test_data['Linear Regression'] - test_data['Actual Sales Volume']
    test_data['RF_Error'] = test_data['Random Forest'] - test_data['Actual Sales Volume']
    test_data['LGBM_Error'] = test_data['LightGBM'] - test_data['Actual Sales Volume']
    test_data['LR_Error_Percentage'] = (test_data['LR_Error'] / test_data['Actual Sales Volume']) * 100
    test_data['RF_Error_Percentage'] = (test_data['RF_Error'] / test_data['Actual Sales Volume']) * 100
    test_data['LGBM_Error_Percentage'] = (test_data['LGBM_Error'] / test_data['Actual Sales Volume']) * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Prediction Error Distribution - LightGBM")
        fig_error = go.Figure(data=[
            go.Histogram(
                x=test_data['LGBM_Error'],
                nbinsx=30,
                name='Prediction Error',
                marker=dict(color='#2ca02c', opacity=0.7),
            )
        ])
        fig_error.update_layout(
            height=400,
            template="plotly_white",
            xaxis_title="Error Value",
            yaxis_title="Frequency",
            showlegend=False
        )
        st.plotly_chart(fig_error, use_container_width=True)
    
    with col2:
        st.markdown("#### Prediction Error Percentage Distribution - LightGBM")
        fig_error_pct = go.Figure(data=[
            go.Histogram(
                x=test_data['LGBM_Error_Percentage'],
                nbinsx=30,
                name='Error Percentage',
                marker=dict(color='#ff7f0e', opacity=0.7),
            )
        ])
        fig_error_pct.update_layout(
            height=400,
            template="plotly_white",
            xaxis_title="Error Percentage (%)",
            yaxis_title="Frequency",
            showlegend=False
        )
        st.plotly_chart(fig_error_pct, use_container_width=True)
    
    st.divider()
    
    # Actual vs predicted scatter plot
    st.markdown("#### Actual Sales Volume vs Predicted Sales Volume")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig_scatter_lr = go.Figure(data=[
            go.Scatter(
                x=test_data['Actual Sales Volume'],
                y=test_data['Linear Regression'],
                mode='markers',
                marker=dict(color=test_data['LR_Error'], colorscale='RdYlGn_r', size=8, 
                           colorbar=dict(title="Error")),
                text=test_data['Product Name'],
                hovertemplate='<b>%{text}</b><br>Actual: %{x:.0f}<br>Predicted: %{y:.0f}<extra></extra>'
            )
        ])
        
        # Add ideal line
        max_val = max(test_data['Actual Sales Volume'].max(), test_data['Linear Regression'].max())
        fig_scatter_lr.add_trace(go.Scatter(
            x=[0, max_val], y=[0, max_val],
            mode='lines', name='Ideal Prediction',
            line=dict(dash='dash', color='gray')
        ))
        
        fig_scatter_lr.update_layout(
            height=400,
            template="plotly_white",
            xaxis_title="Actual Sales Volume",
            yaxis_title="Predicted Sales Volume",
            title_text="Linear Regression"
        )
        st.plotly_chart(fig_scatter_lr, use_container_width=True)
    
    with col2:
        fig_scatter_rf = go.Figure(data=[
            go.Scatter(
                x=test_data['Actual Sales Volume'],
                y=test_data['Random Forest'],
                mode='markers',
                marker=dict(color=test_data['RF_Error'], colorscale='RdYlGn_r', size=8,
                           colorbar=dict(title="Error")),
                text=test_data['Product Name'],
                hovertemplate='<b>%{text}</b><br>Actual: %{x:.0f}<br>Predicted: %{y:.0f}<extra></extra>'
            )
        ])
        
        max_val = max(test_data['Actual Sales Volume'].max(), test_data['Random Forest'].max())
        fig_scatter_rf.add_trace(go.Scatter(
            x=[0, max_val], y=[0, max_val],
            mode='lines', name='Ideal Prediction',
            line=dict(dash='dash', color='gray')
        ))
        
        fig_scatter_rf.update_layout(
            height=400,
            template="plotly_white",
            xaxis_title="Actual Sales Volume",
            yaxis_title="Predicted Sales Volume",
            title_text="Random Forest"
        )
        st.plotly_chart(fig_scatter_rf, use_container_width=True)
    
    with col3:
        fig_scatter_lgbm = go.Figure(data=[
            go.Scatter(
                x=test_data['Actual Sales Volume'],
                y=test_data['LightGBM'],
                mode='markers',
                marker=dict(color=test_data['LGBM_Error'], colorscale='RdYlGn_r', size=8,
                           colorbar=dict(title="Error")),
                text=test_data['Product Name'],
                hovertemplate='<b>%{text}</b><br>Actual: %{x:.0f}<br>Predicted: %{y:.0f}<extra></extra>'
            )
        ])
        
        max_val = max(test_data['Actual Sales Volume'].max(), test_data['LightGBM'].max())
        fig_scatter_lgbm.add_trace(go.Scatter(
            x=[0, max_val], y=[0, max_val],
            mode='lines', name='Ideal Prediction',
            line=dict(dash='dash', color='gray')
        ))
        
        fig_scatter_lgbm.update_layout(
            height=400,
            template="plotly_white",
            xaxis_title="Actual Sales Volume",
            yaxis_title="Predicted Sales Volume",
            title_text="LightGBM"
        )
        st.plotly_chart(fig_scatter_lgbm, use_container_width=True)

# ============================================================================
# PAGE 4: TIME SERIES
# ============================================================================
elif page == "Time Series":
    st.markdown("<h2 class='section-header'>Time Series Forecast Curve</h2>", unsafe_allow_html=True)
    
    # Merge actual and predicted data
    final_df = data['final_df'].copy()
    test_df = data['test_df'].copy()
    test_df['Actual Sales Volume'] = data['y_test'].values
    test_df['LightGBM'] = data['test_pred_lgbm']
    
    # Options
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        selected_products = st.multiselect(
            "Select Products",
            options=sorted(final_df['Product Name'].unique()),
            default=sorted(final_df['Product Name'].unique())[:3]
        )
    
    with col2:
        selected_categories = st.multiselect(
            "Select Categories",
            options=sorted(final_df['Category'].unique()),
            default=sorted(final_df['Category'].unique())[:2]
        )
    
    with col3:
        selected_platforms = st.multiselect(
            "Select Platforms",
            options=sorted(final_df['Platform'].unique()),
            default=sorted(final_df['Platform'].unique())
        )
    
    # Filter data
    filtered_test = test_df[
        (test_df['Product Name'].isin(selected_products)) &
        (test_df['Category'].isin(selected_categories)) &
        (test_df['Platform'].isin(selected_platforms))
    ].sort_values('Date')
    
    if len(filtered_test) > 0:
        # Aggregate by date
        ts_actual = filtered_test.groupby('Date')['Actual Sales Volume'].sum()
        ts_pred = filtered_test.groupby('Date')['LightGBM'].sum()
        
        fig_ts = go.Figure()
        
        fig_ts.add_trace(go.Scatter(
            x=ts_actual.index,
            y=ts_actual.values,
            mode='lines+markers',
            name='Actual Sales Volume',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=6)
        ))
        
        fig_ts.add_trace(go.Scatter(
            x=ts_pred.index,
            y=ts_pred.values,
            mode='lines+markers',
            name='LightGBM Forecast',
            line=dict(color='#2ca02c', width=2, dash='dash'),
            marker=dict(size=6)
        ))
        
        fig_ts.update_layout(
            height=500,
            template="plotly_white",
            xaxis_title="Date",
            yaxis_title="Sales Volume",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_ts, use_container_width=True)
        
        st.divider()
        
        # Time series by product
        st.markdown("#### Time Series Forecast by Product")
        
        for product in selected_products[:3]:  # Show up to 3 products
            product_test = filtered_test[filtered_test['Product Name'] == product].sort_values('Date')
            
            if len(product_test) > 0:
                ts_p_actual = product_test.groupby('Date')['Actual Sales Volume'].sum()
                ts_p_pred = product_test.groupby('Date')['LightGBM'].sum()
                
                fig_product_ts = go.Figure()
                
                fig_product_ts.add_trace(go.Scatter(
                    x=ts_p_actual.index,
                    y=ts_p_actual.values,
                    mode='lines+markers',
                    name='Actual Sales Volume',
                    line=dict(color='#1f77b4', width=2),
                    marker=dict(size=6)
                ))
                
                fig_product_ts.add_trace(go.Scatter(
                    x=ts_p_pred.index,
                    y=ts_p_pred.values,
                    mode='lines+markers',
                    name='Predicted Sales Volume',
                    line=dict(color='#2ca02c', width=2, dash='dash'),
                    marker=dict(size=6)
                ))
                
                fig_product_ts.update_layout(
                    height=350,
                    template="plotly_white",
                    xaxis_title="Date",
                    yaxis_title="Sales Volume",
                    title_text=f"Product: {product}",
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_product_ts, use_container_width=True)
    else:
        st.warning("No matching data found. Please adjust the filters.")

# ============================================================================
# FOOTER
# ============================================================================
st.divider()
st.markdown("""
<div style='text-align: center; color: #999; font-size: 12px; margin-top: 40px;'>
    <p> Supplement Sales Forecast Dashboard | Machine learning-based sales forecasting system</p>
    <p>Data updated: latest test set | Models: Linear Regression, Random Forest, LightGBM</p>
</div>
""", unsafe_allow_html=True)
