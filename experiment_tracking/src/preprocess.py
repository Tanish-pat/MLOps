"""
    Preprocess the data and save it to CSV files.
    This script connects to a MongoDB database, retrieves the training data, preprocesses it, and saves the features and target variable to CSV files.
"""

import pandas as pd
import os
from data_warehouse_connect import connect_mongo

db = connect_mongo()
if db is None:
    raise Exception("Database connection failed.")
try:
    train_collection = db["train"]
    data = pd.DataFrame(list(train_collection.find())).copy()
    if "Loan_ID" in data.columns:
        data.drop(columns=["Loan_ID"], inplace=True)
    data["LoanAmount"] = data["LoanAmount"].fillna(data["LoanAmount"].median())
    data["Loan_Amount_Term"] = data["Loan_Amount_Term"].fillna(data["Loan_Amount_Term"].median())
    data["Credit_History"] = data["Credit_History"].fillna(data["Credit_History"].mode()[0])
    categorical_cols = ["Gender", "Married", "Dependents", "Education", "Self_Employed", "Property_Area"]
    data = pd.get_dummies(data, columns=categorical_cols, drop_first=False)
    if "Loan_Status" in data.columns:
        data["Loan_Status"] = data["Loan_Status"].map({"Y": 1, "N": 0})

    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    X = data.drop(columns=["_id", "_hash", "Loan_Status"], errors="ignore")
    y = data["Loan_Status"] if "Loan_Status" in data.columns else None

    X.to_csv(f"{output_dir}/X.csv", index=False)
    if y is not None:
        y.to_csv(f"{output_dir}/y.csv", index=False)

except Exception as e:
    raise