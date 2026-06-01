import pandas as pd
import json
import joblib
import os
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

os.makedirs("reports", exist_ok=True)

model = joblib.load("models/model.pkl")
test = pd.read_csv("data/processed/test_split.csv")
y_test = test["is_fraud"]
X_test = test.drop(columns=["is_fraud"])

preds = model.predict(X_test)

report = {
    "accuracy": round(accuracy_score(y_test, preds), 4),
    "f1_score": round(f1_score(y_test, preds, zero_division=0), 4),
    "precision": round(precision_score(y_test, preds, zero_division=0), 4),
    "recall": round(recall_score(y_test, preds, zero_division=0), 4),
    "test_samples": len(y_test),
}

with open("reports/evaluation.json", "w") as f:
    json.dump(report, f, indent=2)

print(f"Evaluation: {report}")
