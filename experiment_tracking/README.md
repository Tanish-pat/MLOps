Since you are now supporting multiple models and allowing dynamic selection during training and deployment, you need to modify your Docker workflow accordingly. Here’s how:

---

### **New Docker Commands:**
#### **1. View Existing Containers (Same as Before)**
```sh
docker ps -a
```

#### **2. Remove All Containers (Same as Before)**
```sh
docker rm $(docker ps -aq)
```

#### **3. Build Different Model Images**
Instead of a single `loan_model` image, you now build different images for each model.

```sh
docker build --build-arg MODEL_TYPE=rfc -t loan_model_rfc .
docker build --build-arg MODEL_TYPE=svm -t loan_model_svm .
docker build --build-arg MODEL_TYPE=xgb -t loan_model_xgb .
```

#### **4. Run a Specific Model Container**
Each model has its own container, so you must choose which one to run.

- **Run the Random Forest (RFC) Model**
  ```sh
  docker run -p 8000:8000 loan_model_rfc
  ```

- **Run the SVM Model**
  ```sh
  docker run -p 8000:8000 loan_model_svm
  ```

- **Run the XGBoost Model**
  ```sh
  docker run -p 8000:8000 loan_model_xgb
  ```

---

### **Optional Enhancements**
If you want to keep just **one container and switch models dynamically**, you can:

1. **Build Only Once (No Hardcoded Model)**
   ```sh
   docker build -t loan_model_dynamic .
   ```

2. **Run the Container and Pass the Model Name as an Environment Variable**
   ```sh
   docker run -p 8000:8000 -e MODEL_TYPE="rfc" loan_model_dynamic
   ```

3. **Modify `train.py` and `inference.py` to Read `MODEL_TYPE` from Environment**
   ```python
   import os
   model_type = os.getenv("MODEL_TYPE", "rfc")  # Default to RFC
   ```

This way, you only need **one image** (`loan_model_dynamic`) and can switch models by setting `MODEL_TYPE` at runtime.

Would you like to go with separate images per model or a single image with dynamic selection?