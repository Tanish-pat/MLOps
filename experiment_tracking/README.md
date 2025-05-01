
---

## Project Structure

```
./
├── data/
│   ├── X.csv
│   └── y.csv
├── docker-compose.yml
├── Dockerfile
├── k8s/
│   ├── inference-deployment.yaml
│   └── inference-service.yaml
├── mlruns/
│   ├── 0/
│   └── 259875385046221396/
├── model/
│   ├── model.csv
│   └── scaler.csv
├── README.md
├── requirements/
│   ├── stage_1.txt
│   ├── stage_2.txt
│   └── stage_3.txt
├── requirements.txt
├── runner.txt
├── src/
│   ├── config.py
│   ├── data_warehouse_connect.py
│   ├── inference.py
│   ├── preprocess.py
│   ├── __pycache__/
│   └── train.py
└── steps.txt
```

## Pipeline Stages

1. **Preprocessing (`stage1`)**
   - Reads raw data, processes them and outputs `X.csv` and `y.csv` in `data/`.

2. **Training (`stage2`)**
   - Trains a model using the preprocessed data and stores artifacts in `model/`.

3. **Inference (`stage3`)**
   - Flask-based API to serve predictions using the trained model.

## Usage

### Local Development (Docker Compose)

To run the full pipeline locally:

```bash
docker-compose up --build -d
docker push <DOCKER USERNAME>/experiment_tracking-preprocess:latest
docker push <DOCKER USERNAME>/experiment_tracking-train:latest
docker push <DOCKER USERNAME>/experiment_tracking-inference:latest
dokcer image prune -f
```



---

# **Kubernetes Deployment — Inference Only**

## **1. Apply Kubernetes Manifests**

Deploy the inference service by applying the respective Kubernetes YAML configuration files:

```bash
kubectl apply -f k8s/inference-deployment.yaml
kubectl apply -f k8s/inference-service.yaml
```

## **2. Access the Inference Service**

Once deployed, the service can be accessed via the following command:

```bash
curl http://$(minikube ip):30007
```

Alternatively, you may directly use the cluster IP if known:

```bash
curl http://192.168.58.2:30007
```

## **3. Test the Inference Endpoint**

Send a sample inference request using the following `curl` command. Ensure the payload is a valid JSON array of input feature dictionaries:

```bash
curl -X POST "<% minikube ip>/predict" \
     -H "Content-Type: application/json" \
     -d '[
  {
    "ApplicantIncome": 5000,
    "CoapplicantIncome": 0.0,
    "Credit_History": 1.0,
    "LoanAmount": 150.0,
    "Loan_Amount_Term": 360.0,
    "Gender_Female": 0.0,
    "Gender_Male": 1.0,
    "Married_No": 1.0,
    "Married_Yes": 0.0,
    "Dependents_0": 1.0,
    "Dependents_1": 0.0,
    "Dependents_2": 0.0,
    "Dependents_3+": 0.0,
    "Education_Graduate": 1.0,
    "Education_Not Graduate": 0.0,
    "Self_Employed_No": 1.0,
    "Self_Employed_Yes": 0.0,
    "Property_Area_Rural": 0.0,
    "Property_Area_Semiurban": 1.0,
    "Property_Area_Urban": 0.0
  }
]'
```

---