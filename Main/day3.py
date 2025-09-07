import pandas as pd
import numpy as np
import datetime as dt
from sklearn.preprocessing import StandardScaler
from mlxtend.frequent_patterns import apriori, association_rules

# ===============================
# Load Dataset
# ===============================
# Use absolute or correct relative path
df = pd.read_csv("Data/cleaned_Superstore.csv")

# ===============================
# Data Quality Checks
# ===============================
print("=== Data Quality Checks ===")
print("Missing Values:\n", df.isnull().sum())
print("Duplicate Rows:", df.duplicated().sum())
df.drop_duplicates(inplace=True)
print("Data Types:\n", df.dtypes)

# ===============================
# Outlier Detection and Handling
# ===============================
def handle_outliers(dataframe, column):
    Q1 = dataframe[column].quantile(0.25)
    Q3 = dataframe[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Cap outliers
    dataframe[column] = np.where(dataframe[column] < lower_bound, lower_bound, dataframe[column])
    dataframe[column] = np.where(dataframe[column] > upper_bound, upper_bound, dataframe[column])
    return dataframe

for col in ['Sales', 'Profit', 'Discount']:
    df = handle_outliers(df, col)

print("\nOutliers handled for Sales, Profit, and Discount.")

# ===============================
# Normalization/Standardization
# ===============================
numerical_features = ['Sales', 'Profit', 'Discount']
scaler = StandardScaler()
df[numerical_features] = scaler.fit_transform(df[numerical_features])

print("\nNumerical features normalized.")

# ===============================
# Customer Lifetime Value (CLV)
# ===============================
clv = df.groupby('Customer ID')['Profit'].sum().reset_index()
clv.rename(columns={'Profit': 'Customer Lifetime Value'}, inplace=True)
print("\nCustomer Lifetime Value:\n", clv.head())

# ===============================
# Churn Prediction Features
# ===============================
df['Order Date'] = pd.to_datetime(df['Order Date'])
snapshot_date = df['Order Date'].max() + pd.DateOffset(days=1)

# Recency
recency = df.groupby('Customer ID')['Order Date'].max().reset_index()
recency['Recency'] = (snapshot_date - recency['Order Date']).dt.days
recency.drop('Order Date', axis=1, inplace=True)

# Frequency
frequency = df.groupby('Customer ID')['Order ID'].nunique().reset_index()
frequency.rename(columns={'Order ID': 'Frequency'}, inplace=True)

# Avg Order Frequency
customer_order_dates = df.groupby('Customer ID')['Order Date'].apply(list).reset_index()
customer_order_dates['Order Dates Sorted'] = customer_order_dates['Order Date'].apply(sorted)

def avg_order_frequency(dates):
    if len(dates) < 2:
        return np.nan
    diffs = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
    return np.mean(diffs)

customer_order_dates['Avg Order Frequency'] = customer_order_dates['Order Dates Sorted'].apply(avg_order_frequency)

# Merge churn features
churn_features = pd.merge(recency, frequency, on='Customer ID')
churn_features = pd.merge(churn_features, customer_order_dates[['Customer ID', 'Avg Order Frequency']], on='Customer ID')

print("\nChurn Prediction Features:\n", churn_features.head())

# ===============================
# Product-Level Insights
# ===============================
print("\n=== Product-Level Insights ===")

best_selling_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
print("\nTop 10 Best-Selling Products:\n", best_selling_products)

best_selling_subcategories = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(10)
print("\nTop 10 Best-Selling Sub-Categories:\n", best_selling_subcategories)

product_profit_discount = df.groupby('Product Name').agg({'Profit': 'sum', 'Discount': 'mean'}).sort_values(by='Profit', ascending=False)
print("\nProduct Profitability and Discount Sensitivity:\n", product_profit_discount.head())

product_turnover = df.groupby('Product Name')['Order ID'].nunique().sort_values(ascending=False)
print("\nProduct Turnover (based on sales frequency):\n", product_turnover.head())

# ===============================
# Trend Analysis
# ===============================
print("\n=== Trend Analysis ===")
df['YearMonth'] = df['Order Date'].dt.to_period('M')

monthly_sales = df.groupby('YearMonth')['Sales'].sum()
print("\nMonthly Sales Growth Trend:\n", monthly_sales)

df['Month'] = df['Order Date'].dt.month
monthly_orders = df.groupby('Month')['Order ID'].nunique()
print("\nMonthly Order Seasonality:\n", monthly_orders)

# Cohort Analysis
def get_month(x): return dt.datetime(x.year, x.month, 1)
df['OrderMonth'] = df['Order Date'].apply(get_month)
df['CohortMonth'] = df.groupby('Customer ID')['OrderMonth'].transform('min')

def get_date_int(df, column):
    year = df[column].dt.year
    month = df[column].dt.month
    day = df[column].dt.day
    return year, month, day

invoice_year, invoice_month, _ = get_date_int(df, 'OrderMonth')
cohort_year, cohort_month, _ = get_date_int(df, 'CohortMonth')

df['CohortIndex'] = (invoice_year - cohort_year) * 12 + (invoice_month - cohort_month) + 1

# ===============================
# Regional Analysis
# ===============================
print("\n=== Regional Analysis ===")

region_performance = df.groupby('Region')[['Sales', 'Profit']].sum().sort_values(by='Sales', ascending=False)
print("\nRegion-wise Performance (Sales & Profit):\n", region_performance)

low_profit_regions = region_performance[region_performance['Profit'] < 0]
print("\nLow-Performing Regions (Negative Profit):\n", low_profit_regions)

# ===============================
# Basket/Association Analysis
# ===============================
print("\n=== Basket/Association Analysis ===")

basket = df.groupby(['Order ID', 'Sub-Category'])['Quantity'].sum().unstack().reset_index().fillna(0).set_index('Order ID')

def encode_units(x):
    return 1 if x >= 1 else 0

basket_sets = basket.map(encode_units)

frequent_itemsets = apriori(basket_sets, min_support=0.01, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
print("\nAssociation Rules:\n", rules.head())
