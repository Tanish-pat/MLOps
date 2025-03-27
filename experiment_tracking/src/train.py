import pandas as pd
import mlflow  # type: ignore
import mlflow.sklearn # type: ignore
import os
import pathlib
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from mlflow.models.signature import infer_signature # type: ignore
from logger import logger  # Import logger

# Define BASE_DIR dynamically
BASE_DIR = pathlib.Path(__file__).resolve().parent
ARTIFACT_DIR = BASE_DIR / "mlruns"

# Ensure the artifact directory exists
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

# Convert path to MLflow-compatible URI
mlflow_tracking_uri = ARTIFACT_DIR.as_uri()  # Converts to file://C:/Users/... format

# Set MLflow tracking URI
mlflow.set_tracking_uri(mlflow_tracking_uri)
logger.info(f"MLflow tracking URI set to: {mlflow_tracking_uri}")

# Load processed data
X = pd.read_csv("data/processed/X.csv")
y = pd.read_csv("data/processed/y.csv")
X = X.astype("float64")  # Avoid MLflow warning

logger.info(f"Data loaded: {X.shape[0]} rows, {X.shape[1]} features.")

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

logger.info(f"Data split: {X_train.shape[0]} training rows, {X_test.shape[0]} test rows.")

# Set MLflow tracking directory
mlflow.set_experiment("Loan_Approval_Experiment")

with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train.values.ravel())

    # Predictions & Metrics
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    # Log accuracy in MLflow
    mlflow.log_metric("accuracy", acc)

    # Log model with MLflow
    signature = infer_signature(X_train, model.predict(X_train))
    mlflow.sklearn.log_model(model, "random_forest_model", signature=signature, input_example=X_train.iloc[:1])

    # Save model locally
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/loan_approval_model.pkl")

    logger.info(f"Model trained with accuracy: {acc}")
    logger.info("Model saved at models/loan_approval_model.pkl")