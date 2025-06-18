print("hello")

import pandas as pd

# Use the correct encoding
df = pd.read_csv("/Users/vivekkumar/Desktop/Superstore.csv", encoding='latin1')

print(df.head())

# rows and columns
print("count of rows and colmns ")
print(df.shape)

# data type
print("data type of all columns")
print(df.dtypes)

# missing and null values
print("missing and null values")
print(df.isnull().sum())

# by checking the column data type time to change the data type 
#Convert Order Date and Ship Date to datetime
print("convering the order and ship date to datetime")
df['Order Date'] = pd.to_datetime(df["Order Date"])
df['Ship Date'] = pd.to_datetime(df["Ship Date"])

print(df.dtypes)
#Create New Date Columns (Month, Year)
#This helps in time-based analysis later.
print("creating two column order month and year")
df["Order Month"] = df["Order Date"].dt.month
df["Order Year"] = df["Order Date"].dt.year
print(df.dtypes)

# check the data
print(df)

# now check the duplicate rows
# Count of duplicate rows

duplicate_count = df.duplicated().sum()
print(f"Total duplicate rows: {duplicate_count}")

# export the clean data set
print("exporting cleaned data with out duplicate rows")
df.to_csv("cleaned_Superstore.csv",index= False)
print(df)

# NOW MOVING TO EDA
# IMPORTING LIBRARIES

import matplotlib.pyplot as plt
import seaborn as sns


#Total KPIs – How big is the business?


# Sales & Profit Summary
print("Total Sales: ", df['Sales'].sum())
print("Total Profit: ", df['Profit'].sum())

# Total order also
print("Total order : ",df['Order ID'].nunique())
#

# Sales by Category and Sub-Category
# here we are finding the highest and lowest category sales by grouping the two 
print("Sales per subcategory")
category_sales = df.groupby('Category')['Sales'].sum().sort_values()
category_sales.plot(kind="bar", color='steelblue', title='Sales by Category')
plt.ylabel("Total Sales")     # Changed from xlabel to ylabel (as categories are on x-axis)
plt.xlabel("Category")
plt.xticks(rotation=0)       # Optional: rotates x-axis labels for better readability
plt.tight_layout() 
plt.show()
# Sales by sub-category 
# here we also plot a graph for sales and sub-cat

# Group by 'Sub-Category', sum 'Sales', and sort values
subCategory_sales = df.groupby('Sub-Category')['Sales'].sum().sort_values()

# Plot bar chart
subCategory_sales.plot(kind="bar", color='steelblue', title='Sales by Sub-category')

# Add axis labels
plt.ylabel("Total Sales")
plt.xlabel("Sub-Category")

# Rotate x-axis labels
plt.xticks(rotation=45)

# Adjust layout and display the plot
plt.tight_layout()
plt.show()


#Region-Wise Profit vs Sales
region_sales = df.groupby('Region')['Profit','Sales'].sum().sort_values()
region_sales.plot(kind="bar",title='sales per region')
plt.ylabel("total sales")
plt.xlabel("region")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()