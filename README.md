# MLOps Pipeline for Loan Approval Prediction

This repository contains an end-to-end MLOps pipeline that automates the lifecycle of a machine learning system for predicting loan approval status. The workflow covers data extraction, transformation, loading (ETL), model training, inference via a Flask endpoint, and containerization and deployment using Docker, Docker Compose, and Kubernetes (Minikube).

## Table of Contents
- [MLOps Pipeline for Loan Approval Prediction](#mlops-pipeline-for-loan-approval-prediction)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Directory Structure](#directory-structure)
  - [Requirements](#requirements)
  - [Installation \& Setup](#installation--setup)
  - [Usage](#usage)
    - [ETL Pipeline](#etl-pipeline)
    - [Model Training](#model-training)
    - [Inference](#inference)
  - [Containerization \& Deployment](#containerization--deployment)
    - [Dockerization](#dockerization)
    - [Docker Compose](#docker-compose)
    - [Kubernetes Deployment](#kubernetes-deployment)
  - [Makefile Targets](#makefile-targets)
- [Final Notes](#final-notes)

## Overview

This project implements a modular, automated MLOps pipeline that:
- Extracts raw CSV data.
- Performs data cleaning, transformation, and one-hot encoding.
- Loads preprocessed data into MongoDB.
- Trains a logistic regression model with MLflow experiment tracking.
- Provides a Flask-based inference endpoint.
- Utilizes Docker multi-stage builds and Docker Compose for local orchestration.
- Deploys the inference service to a Kubernetes cluster via Minikube.

## Directory Structure

```bash
.
├── Dockerfile
├── docker-compose.yml
├── k8s
│   ├── inference-deployment.yaml
│   └── inference-service.yaml
├── Makefile
├── README.md
├── requirements
│   ├── stage_1.txt
│   ├── stage_2.txt
│   └── stage_3.txt
└── src
    ├── config.py
    ├── database.py
    ├── etl_pipeline.py
    ├── extract.py
    ├── inference.py
    ├── load.py
    ├── logger.py
    ├── preprocess.py
    ├── train.py
    └── transform.py
```

## Requirements

- Python 3.12 (or compatible version)
- MongoDB instance (local or remote)
- Docker and Docker Compose
- Minikube for local Kubernetes deployment
- MLflow, scikit-learn, Flask, pandas, and other dependencies (see requirements files)

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/your_repo.git
   cd your_repo
   ```

2. Install Python dependencies:
   ```bash
   make install
   ```

3. Set up required directories and environment variables:
   - Create a `.env` file with the required MongoDB URI (e.g., `MONGO_URI=<your_mongo_uri>`).
   - Run:
     ```bash
     make setup
     ```

## Usage

### ETL Pipeline

Run the ETL pipeline to extract, transform, and load data:
```bash
make preprocess
```

The preprocessing script (`src/preprocess.py`) connects to MongoDB, retrieves raw training data, cleans and encodes it, and saves the features (`X.csv`) and target labels (`y.csv`) to the `data` folder.

### Model Training

Train the logistic regression model using the preprocessed data:
```bash
make train
```

The training script (`src/train.py`) loads the CSV files, splits the data, scales the features, trains the model, evaluates accuracy, and logs parameters and artifacts via MLflow. Model coefficients and scaler parameters are saved in the `model` folder.

### Inference

Run the inference endpoint locally to serve predictions:
```bash
make inference
```

The inference script (`src/inference.py`) starts a Flask server on port 5000 that loads the model artifacts and scaler parameters to make predictions for incoming JSON requests.

## Containerization & Deployment

### Dockerization

The project uses a multi-stage `Dockerfile` to separate preprocessing, training, and inference stages:
- **Stage 1:** Preprocessing – Executes `src/preprocess.py`
- **Stage 2:** Training – Executes `src/train.py`
- **Stage 3:** Inference – Builds and runs the Flask-based inference server

### Docker Compose

For local orchestration, use Docker Compose:
```bash
docker-compose up --build -d
```
This builds and starts containers for preprocessing, training, and inference in sequence.

### Kubernetes Deployment

Deploy the inference service on a local Kubernetes cluster (Minikube):
```bash
kubectl apply -f k8s/inference-deployment.yaml
kubectl apply -f k8s/inference-service.yaml
```
This creates a deployment with a NodePort service (exposed on port 30007) to allow external access.

## Makefile Targets

Key targets provided in the Makefile:
- `make preprocess`: Run the ETL preprocessing step.
- `make train`: Run model training.
- `make inference`: Run the inference endpoint.
- `make all`: Run preprocessing and training sequentially.
- `make install`: Install dependencies.
- `make setup`: Create necessary directories.
- `make clean`: Remove generated files.


# Final Notes
This project serves as a comprehensive example of an MLOps pipeline, demonstrating best practices in data handling, model training, and deployment. It can be extended or modified to suit specific use cases or requirements. Feel free to contribute or raise issues for improvements or bugs.
