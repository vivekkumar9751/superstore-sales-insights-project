import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:Vivek%40124@localhost/superstore_data")

try:
    conn = engine.connect()
    print("Connection successful ✅")
    conn.close()
except Exception as e:
    print("Connection failed ❌", e)


# Load CSV into Pandas
df = pd.read_csv("Data/cleaned_Superstore.csv")

# Connect to MySQL (replace credentials)
engine = create_engine("mysql+mysqlconnector://root:Vivek%40124@localhost/superstore_data")

# Export DataFrame to MySQL (creates table automatically if not exists)
df.to_sql("cleaned_Superstore", engine, if_exists="replace", index=False)

df = pd.read_csv("Data/Recency_Frequency_Monetary.csv")
engine = create_engine("mysql+mysqlconnector://root:Vivek%40124@localhost/superstore_data")
df.to_sql("Recency_Frequency_Monetary", engine, if_exists="replace", index=False)
print("Data exported to MySQL successfully.")