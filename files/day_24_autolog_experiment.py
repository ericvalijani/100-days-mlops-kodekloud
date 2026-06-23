"""
MLflow autologging — two TODO blocks activate MLflow's automatic
capture of parameters, metrics, and the trained model for the
`model.fit(...)` call below.

The dataset and the model here are synthetic. A LogisticRegression
fitted on a deterministic four-row XOR-like array stands in for a
real training step so that autologging has a valid sklearn fit()
call to instrument. No real ML workflow takes place; the focus of
the lab is autolog configuration, not model quality.

Both TODO blocks must be completed BEFORE `model.fit(...)` runs —
autolog hooks sklearn at call time, and the active experiment
scopes where the autologged run lands.
"""
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression

mlflow.set_tracking_uri("http://localhost:5000")

mlflow.set_experiment('autolog-demo')
mlflow.autolog()

# Synthetic four-row XOR-like array. Not a real ML dataset — just
# a deterministic toy to give sklearn.fit() something to execute.
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([0, 0, 1, 1])

model = LogisticRegression(C=1.0, max_iter=100, random_state=42)
model.fit(X, y)

print("Autolog run complete — check the MLflow UI")
