"""
    Train a logistic regression model to predict loan approval status.
    This script uses MLflow for experiment tracking and saves the model and scaler parameters.
"""

import os
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Set MLflow experiment
mlflow.set_experiment("Loan_Approval_Experiment")

with mlflow.start_run():
    X = pd.read_csv("data/X.csv")
    y = pd.read_csv("data/y.csv")["Loan_Status"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    model = LogisticRegression(max_iter=100000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")

    mlflow.log_param("max_iter", 1000)
    mlflow.log_metric("accuracy", accuracy)

    mlflow.sklearn.log_model(model, "logistic_regression_model")

    model_dir = "model"
    os.makedirs(model_dir, exist_ok=True)

    # Save model coefficients
    coefficients = pd.DataFrame({
        "Feature": ["Intercept"] + X.columns.tolist(),
        "Coefficient": [model.intercept_[0]] + model.coef_[0].tolist()
    })
    coefficients.to_csv(f"{model_dir}/model.csv", index=False)

    # Save scaler parameters
    scaler_params = pd.DataFrame({
        "Feature": X.columns,
        "Mean": scaler.mean_,
        "Var": scaler.var_
    })
    scaler_params.to_csv(f"{model_dir}/scaler.csv", index=False)

    print("Model training complete. Model and parameters saved in /model folder.")
