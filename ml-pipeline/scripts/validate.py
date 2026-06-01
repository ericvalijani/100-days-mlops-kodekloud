import pandas as pd
import json
import os

os.makedirs("reports", exist_ok=True)
df = pd.read_csv("data/raw/data.csv")

report = {
    "rows": len(df),
    "columns": list(df.columns),
    "null_counts": {k: int(v) for k, v in df.isnull().sum().to_dict().items()},
    "duplicates": int(df.duplicated().sum()),
    "valid": bool(len(df) > 0 and df.isnull().sum().sum() == 0),
}

with open("reports/validation.json", "w") as f:
    json.dump(report, f, indent=2)

print(f"Validation: {report['rows']} rows, valid={report['valid']}")
