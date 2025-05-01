"""
    Inference script for the model.
    This script loads the model and scaler parameters, and provides an endpoint for making predictions.
"""

from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

model_data = pd.read_csv("model/model.csv")
scaler_data = pd.read_csv("model/scaler.csv")

intercept = model_data.loc[model_data["Feature"] == "Intercept", "Coefficient"].values[0]
coefficients = model_data.loc[model_data["Feature"] != "Intercept"].set_index("Feature")["Coefficient"]

scaler_mean = scaler_data.set_index("Feature")["Mean"]
scaler_var = scaler_data.set_index("Feature")["Var"]

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if isinstance(data, dict):
        data = [data]
    df = pd.DataFrame(data)
    df.rename(columns={"Dependents_3_plus": "Dependents_3+", "Education_Not_Graduate": "Education_Not Graduate"}, inplace=True)
    df = df[coefficients.index]
    df = (df - scaler_mean) / scaler_var.pow(0.5)
    linear_output = df.mul(coefficients).sum(axis=1) + intercept
    predictions = (linear_output > 0).astype(int).tolist()
    return jsonify(predictions)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)