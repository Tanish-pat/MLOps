import pandas as pd
import numpy as np
import joblib
import os
from data_warehouse_connect import connect_mongo
from logger import logger  # Import logger

# Connect to the database
db = connect_mongo()
if db is None:
    logger.error("Database connection failed. Exiting preprocessing.")
    raise Exception("Database connection failed.")

# Fetch data
train_collection = db["train"]
data = pd.DataFrame(list(train_collection.find())).copy()
logger.info(f"Data fetched from MongoDB: {data.shape[0]} rows, {data.shape[1]} columns.")

# Drop Loan_ID
if "Loan_ID" in data.columns:
    data.drop(columns=["Loan_ID"], inplace=True)

# Handle missing values safely
data.loc[:, "LoanAmount"] = data["LoanAmount"].fillna(data["LoanAmount"].median())
data.loc[:, "Loan_Amount_Term"] = data["Loan_Amount_Term"].fillna(data["Loan_Amount_Term"].median())
data.loc[:, "Credit_History"] = data["Credit_History"].fillna(data["Credit_History"].mode()[0])
logger.info("Missing values handled.")

# Encode categorical variables
from sklearn.preprocessing import OneHotEncoder
categorical_cols = ["Gender", "Married", "Dependents", "Education", "Self_Employed", "Property_Area"]
encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

encoded_features = encoder.fit_transform(data[categorical_cols])
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_cols))
logger.info("Categorical variables encoded.")

# Final preprocessing
data.drop(columns=categorical_cols, inplace=True)
data = pd.concat([data, encoded_df], axis=1)

# Convert Loan_Status to numerical
if "Loan_Status" in data.columns:
    data.loc[:, "Loan_Status"] = data["Loan_Status"].map({"Y": 1, "N": 0})

# Save processed data
output_dir = "data/processed"
os.makedirs(output_dir, exist_ok=True)
X = data.drop(columns=["_id", "_hash", "Loan_Status"], errors="ignore")
y = data["Loan_Status"]

X.to_csv(f"{output_dir}/X.csv", index=False)
y.to_csv(f"{output_dir}/y.csv", index=False)
logger.info("Preprocessing complete. Processed data saved successfully!")