import os
import pandas as pd

os.makedirs("data/raw", exist_ok=True)
# Ingest: validate the raw data file exists and is readable

df = pd.read_csv("data/raw/data.csv")
print(f"Data ingested successfully: {len(df)} rows, {len(df.columns)} columns")
