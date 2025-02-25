import joblib
import pandas as pd
import logging
import os
from fastapi import FastAPI

# Get the absolute path of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load Model using absolute paths
model = joblib.load(os.path.join(BASE_DIR, "../models/loan_approval_model.pkl"))

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Loan Approval Model is Running!"}

@app.post("/predict/")
def predict(data: dict):
    # Convert input data to DataFrame
    df = pd.DataFrame([data])

    # Make prediction
    prediction = model.predict(df)
    return {"loan_approval": int(prediction[0])}
