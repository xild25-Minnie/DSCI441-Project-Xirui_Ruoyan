Supplement Sales Forecast Dashboard

Project Overview

This is a machine learning based sales forecasting system that uses three different models Linear Regression Random Forest and LightGBM to predict supplement sales volume. The application provides an interactive Streamlit dashboard for viewing model performance and sales forecasts in real time.

Core Features

1 Model Performance Analysis

Performance comparison of three models Linear Regression Random Forest and LightGBM

Key metrics display MAE RMSE R squared and MAPE

Radar chart visualization of model performance

Supports switching between validation set and test set

2 Sales Forecast Overview

Sales forecast comparison by product

Sales forecast by category

Sales forecast by platform

Sales forecast by location

Multi model comparison display

3 Prediction Analysis

Prediction error distribution analysis

Error percentage analysis

Actual versus predicted scatter plot

Prediction accuracy visualization

4 Time Series Forecasting

Users can filter by product category and platform

Time series forecast curve display

Detailed time series analysis by product

Comparison between actual sales volume and predicted values

Quick Start

1 Install Dependencies

Enter the project directory

cd workspaces DSCI441 Project Xirui Ruoyan

Install all dependencies

pip install r requirements txt

2 Run the Application

Run from the project root directory

streamlit run app streamlit app py

3 Access the Application

After the application starts it will automatically open in the browser. If it does not open automatically visit

http localhost 8501

Project Structure

DSCI441 Project Xirui Ruoyan

app

streamlit app py main application file

notebooks

code ipynb complete analysis and model training code

Supplement Sales Strong Correlation csv original data

src

final code py optional Python module

data

raw

Supplement Sales Weekly Expanded csv original expanded data

requirements txt project dependencies

README md this file

Data Description

Original Data Columns

Date sales date

Product Name product name

Category product category

Location sales location

Platform sales platform

Units Sold sales volume target variable

Price product price

Discount discount

Units Returned returned units

Revenue revenue

Feature Engineering

Features used in the application include

Calendar features year month quarter weekofyear

Lag features units sold lag1 units sold lag2 units sold lag4 price lag1 discount lag1

Rolling features units sold rollmean 4 units sold rollstd 4

Categorical features Product Name Category Location Platform

Model Description

1 Linear Regression

Linear regression baseline model

Fast inference and easy to interpret

Suitable for capturing linear relationships

2 Random Forest

Ensemble learning method

Can capture nonlinear relationships

Requires parameter tuning to avoid overfitting

3 LightGBM

Gradient boosting tree model

Usually delivers the best performance

Efficient and fast

Key Metrics Description

Metric Meaning Range

MAE Mean Absolute Error lower is better

RMSE Root Mean Squared Error lower is better

R squared Coefficient of Determination from 0 to 1 higher is better

MAPE Mean Absolute Percentage Error percentage lower is better

Usage Recommendations

1 Model Selection

Prioritize test set metrics

Models with higher R squared and lower RMSE perform better

LightGBM usually has the best performance

2 Data Exploration

Use the Time Series page to observe seasonal patterns

Use filters to customize the analysis scope

Use scatter plots to evaluate individual prediction quality

3 Business Applications

Use prediction results for inventory planning

Identify product and platform combinations with high errors

Monitor changes in model performance

Technology Stack

Framework Streamlit

Data Processing Pandas NumPy

Machine Learning Scikit learn LightGBM

Visualization Plotly

Statistics SciPy Scikit learn

Frequently Asked Questions

Q Why does the application start slowly

A During the first run the application needs to train all models. After that the models are cached and the application will run much faster.

Q How do I update the data

A Modify the notebooks Supplement Sales Strong Correlation csv file and then rerun the application.

Q How do I customize model parameters

A Modify the model parameters in the load data and models function inside streamlit app py.

Improvement Directions

Add prediction confidence intervals

Support custom model parameter tuning

Add feature importance analysis

Support exporting prediction reports as PDF

Support real time data updates and model retraining

Contact

For questions or suggestions please refer to the comments in the code or the detailed analysis in the Jupyter notebook.

Last Updated April 24 2026

Data Scope Includes complete time series and multidimensional categories
