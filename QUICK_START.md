Streamlit Dashboard Quick Reference Guide

Table of Contents

1 Three Second Quick Start

2 Feature Navigation

3 Page Descriptions

4 Data Sources

5 Troubleshooting

Three Second Quick Start

Linux and Mac

cd workspaces DSCI441 Project Xirui Ruoyan

bash run dashboard sh

Windows

cd workspaces DSCI441 Project Xirui Ruoyan

run dashboard bat

Manual Start

streamlit run app streamlit app py

The browser will open automatically

http localhost 8501

Feature Navigation

Sidebar Menu

Select the page you want to view from the left sidebar

Model Performance View the comparison of three models

Sales Forecast View prediction results across multiple dimensions

Prediction Analysis Analyze prediction errors in detail

Time Series View time series forecast curves

Page Descriptions

Page 1 Model Performance

Features

Real time model performance comparison cards

Bar charts for key metrics such as RMSE and R squared

Model performance radar chart for multidimensional comparison

Interactive Operations

Switch between validation set and test set

Hover to view detailed metrics

Key Metrics

MAE Mean Absolute Error

RMSE Root Mean Square Error

R squared Coefficient of determination Higher is better

MAPE Mean Absolute Percentage Error

Page 2 Sales Forecast

Features

Prediction comparison by product using a bar chart

Prediction by category platform and location

Characteristics

Displays actual sales volume versus predictions from three models

Supports interactive drill down analysis

Clear visual hierarchy

Page 3 Prediction Analysis

Features

Prediction error distribution histogram

Error percentage distribution

Actual versus predicted scatter plots for three models

Characteristics

Errors are color coded Green means accurate and red means large deviation

An ideal prediction line is added as a reference

Supports mouse hover to view product names

Use Cases

Identify products with good prediction performance

Find problematic products with high errors

Evaluate overall model accuracy

Page 4 Time Series

Features

Configurable multidimensional filters

Product Name multi select

Product Category multi select

Sales Platform multi select

Time series curve showing actual values versus predicted values

Detailed time series charts expanded by product

Characteristics

Dynamic data aggregation

Supports flexible filter combinations

Clearly shows seasonal patterns

Data Sources

Component Source

Original Data notebooks Supplement Sales Strong Correlation csv

Feature Engineering Executed in real time when the application starts

Model Training Automatically trained when the application starts The first run is slower

Model Cache Cached by Streamlit st cache resource

Troubleshooting

Problem ModuleNotFoundError No module named streamlit

Solution

pip install r requirements txt

Problem The application starts slowly

Reason

The first startup needs to train all models

Solution

Wait for the training to finish The application will be faster after the data is cached

Problem File not found error

Check

Make sure you are in the correct directory

pwd

Expected output

workspaces DSCI441 Project Xirui Ruoyan

Check the data file

ls notebooks Supplement Sales Strong Correlation csv

Problem Charts are not displayed

Solutions

1 Refresh the browser

2 Clear the browser cache

3 Check the network connection Plotly needs to render the charts

Performance Optimization Recommendations

1 First run requires two to five minutes to train models depending on the data size

2 Later runs load in milliseconds because caching is enabled

3 For large datasets use filters on the Time Series page to reduce the data volume

Main Feature Summary

Feature Description

Three ML Models Linear Regression Random Forest LightGBM

Four Dashboard Pages Performance Forecast Analysis Time Series

Multidimensional Analysis Product Category Platform Location

Interactive Visualization Plotly dynamic charts

Automatic Caching Fast loading and response

English Interface Complete English interface

Related Files

DSCI441 Project Xirui Ruoyan

app streamlit app py Main application

requirements txt Dependency list

run dashboard sh Linux and Mac startup script

run dashboard bat Windows startup script

DASHBOARD README md Complete documentation

QUICK START md This file

notebooks

code ipynb Complete analysis code

Supplement Sales Strong Correlation csv Data file

Use Cases

Use Case 1 Evaluate Models

1 Open the application

2 Go to the Model Performance page

3 Switch between validation set and test set for comparison

4 View the radar chart to understand the strengths and weaknesses of each model

Use Case 2 View Prediction for a Specific Product

1 Go to the Time Series page

2 Select only Product A in the multi select box

3 Observe its time series forecast curve

4 Identify seasonal patterns

Use Case 3 Analyze Prediction Errors

1 Go to the Prediction Analysis page

2 Check the red points in the scatter plot High error

3 Identify which products or locations need improvement

Frequently Asked Questions

Q Can the model update automatically

A Not currently You need to modify the data file and restart the application

Q Can data or charts be exported

A Plotly charts can be exported as PNG from the top right menu Tables can be copied

Q Does it support real time updates

A The current version supports updates by periodic restart You can consider integrating a real time data source

Q Do all models have to be displayed

A You can comment out unnecessary models in the code

Enjoy using the dashboard
