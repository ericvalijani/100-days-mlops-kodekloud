import pandas as pd
import os

os.makedirs("data/processed", exist_ok=True)
df = pd.read_csv("data/raw/data.csv")
df = df.drop_duplicates().dropna()
df.to_csv("data/processed/clean.csv", index=False)
print(f"Preprocessed: {len(df)} clean rows")