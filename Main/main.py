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

import matplotlib.pyplot as mlt
import seaborn as sns


# Sales & Profit Summary
print("Total Sales: ", df['Sales'].sum())
print("Total Profit: ", df['Profit'].sum())

# Total order also
print("Total order : ",df['Order ID'].nunique())

# Sales by Category and Sub-Category
