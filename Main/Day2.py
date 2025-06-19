import pandas as pd
import datetime as dt 


# Use the correct encoding
df = pd.read_csv("/Users/vivekkumar/Desktop/Superstore.csv", encoding='latin1')



# convert orde time to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])

#latest date in dateset
latest_date = df['Order Date'].max()

#group by customer
rfm = df.groupby('Customer ID').agg({
    'Order Date': lambda x: (latest_date - x.max()).days,
    'Order ID': 'nunique',
    'Sales': 'sum'
}).reset_index()

# Rename column name 
rfm.columns= ['Customer ID','Recency','Frequency','Monetary']

#Scoring
rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, labels=[1, 2, 3, 4])

# Combined RFM Score
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

print(rfm.head())

rfm.to_csv("Recency_Frequency_Monetary.csv",index= False)

print("i have just create a new file for export the rfm")



# Step 1: Create RFM score as a string like '444'
rfm['RFM_Score_Str'] = (
    rfm['R_Score'].astype(str) + 
    rfm['F_Score'].astype(str) + 
    rfm['M_Score'].astype(str)
)

# Step 2: Convert string like '444' to integer
rfm['RFM_Score_Num'] = rfm['RFM_Score_Str'].astype(int)

# Step 3: Apply segmentation
def rfm_segment(score):
    if score >= 444:
        return 'Champions'
    elif score >= 344:
        return 'Loyal Customers'
    elif score >= 244:
        return 'Potential Loyalist'
    elif score >= 200:
        return 'At Risk'
    else:
        return 'Lost'

rfm['Segment'] = rfm['RFM_Score_Num'].apply(rfm_segment)


#Pie Chart of Segments



import matplotlib.pyplot as plt

segment_counts = rfm['Segment'].value_counts()
colors = plt.get_cmap('Set3').colors  # colorful scheme

plt.figure(figsize=(7, 7))
plt.pie(segment_counts, labels=segment_counts.index, autopct='%1.1f%%', colors=colors)
plt.title('Customer Segments by RFM Score')
plt.tight_layout()

# Save chart to images folder

plt.show()


#RFM Heatmap (R x F)

import seaborn as sns
rfm_heatmap = rfm.groupby(['R_Score', 'F_Score']).size().reset_index(name='count')

rfm_pivot = rfm_heatmap.pivot(index='F_Score', columns='R_Score', values='count')

plt.figure(figsize=(8, 6))
sns.heatmap(rfm_pivot, annot=True, fmt='d', cmap='YlGnBu')
plt.title('RFM Heatmap: Frequency vs Recency')
plt.xlabel("Recency Score")
plt.ylabel("Frequency Score")

# Save chart to images folder
plt.show()
