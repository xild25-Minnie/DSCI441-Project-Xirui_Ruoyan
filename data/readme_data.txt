# Data README for Supplement_Sales_Weekly_Expanded.csv

## Description
The dataset used in this project is the Supplement Sales Data from Kaggle, published by Zahid Mughal. It contains weekly sales records for health and wellness supplements from January 2020 to April 2025.
## Data Structure
The dataset contains the following columns:

- **Date**: Date of the sales record in YYYY-MM-DD format (string)
- **Product Name**: Name of the supplement product (string, e.g., "Whey Protein", "Vitamin C")
- **Category**: Product category (string, e.g., "Protein", "Vitamin", "Omega", "Performance", "Amino Acid", "Mineral", "Digestive", "Herbal", "Sleep Aid", "Fat Burner", "Hydration")
- **Units Sold**: Number of units sold in that week (integer)
- **Price**: Unit price of the product (float)
- **Revenue**: Total revenue generated (calculated as Units Sold * Price, adjusted for discounts) (float)
- **Discount**: Discount applied as a decimal (float, e.g., 0.05 for 5% discount)
- **Units Returned**: Number of units returned (integer)
- **Location**: Sales location (string, e.g., "UK", "Canada", "USA")
- **Platform**: Sales platform (string, e.g., "Amazon", "Walmart", "iHerb")
- **Month**: Month number (integer, 1-12)

## Sample Data
Date,Product Name,Category,Units Sold,Price,Revenue,Discount,Units Returned,Location,Platform,Month
2021-01-04,Whey Protein,Protein,139,22.37,2953.69,0.05,1,UK,Amazon,1
2021-01-04,Vitamin C,Vitamin,78,34.88,2720.43,0.0,1,UK,Amazon,1
2021-01-04,Fish Oil,Omega,70,31.75,2222.57,0.0,1,Canada,Amazon,1

## How to Obtain the Data
The data is derived from the M5 Forecasting - Accuracy competition dataset available on Kaggle. To obtain and generate this dataset:

Visit the Kaggle competition page: https://www.kaggle.com/datasets/zahidmughal2343/supplement-sales-data/data

## Where to Place the Data
Place the `Supplement_Sales_Weekly_Expanded.csv` file in the `data/` folder of this project repository. The file should be located at `data/Supplement_Sales_Weekly_Expanded.csv` relative to the project root.

## Notes
The dataset covers multiple supplement categories, such as protein, vitamins, omega, and amino acids. It also includes different e-commerce platforms and regions. The key variables include date, product information, product category, platform, location, price, discount rate, returns, and weekly units sold.
