import pandas as pd
import yaml
import json
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

os.makedirs("models", exist_ok=True)

with open("params.yaml") as f:
    params = yaml.safe_load(f)

df = pd.read_csv("data/processed/clean.csv")
X = df.drop(columns=["is_fraud", "transaction_id", "merchant"])
X = pd.get_dummies(X, columns=["category"])
y = df["is_fraud"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=params["test_size"], random_state=params["random_seed"]
)

model = RandomForestClassifier(
    n_estimators=params["n_estimators"],
    max_depth=params["max_depth"],
    random_state=params["random_seed"],
)
model.fit(X_train, y_train)

preds = model.predict(X_test)
metrics = {
    "accuracy": round(accuracy_score(y_test, preds), 4),
    "f1_score": round(f1_score(y_test, preds, zero_division=0), 4),
}

joblib.dump(model, "models/model.pkl")
with open("metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

# Save test data for evaluation stage
X_test_df = X_test.copy()
X_test_df["is_fraud"] = y_test.values
X_test_df.to_csv("data/processed/test_split.csv", index=False)

print(f"Trained: {metrics}")
