# Stage 1: Preprocessing
FROM python:3.12-slim AS stage1
WORKDIR /app
RUN mkdir -p data model
COPY requirements/stage_1.txt ./
RUN pip install --no-cache-dir -r stage_1.txt
COPY src/ src/
RUN python src/preprocess.py

# Stage 2: Training
FROM python:3.12-slim AS stage2
WORKDIR /app
COPY requirements/stage_2.txt ./
RUN pip install --no-cache-dir -r stage_2.txt
COPY --from=stage1 /app/data/X.csv /app/data/y.csv /app/data/
COPY src/ src/
RUN python src/train.py

# Stage 3: Inference
FROM python:3.12-slim AS stage3
WORKDIR /app
RUN mkdir -p model
COPY requirements/stage_3.txt ./
RUN pip install --no-cache-dir -r stage_3.txt
COPY src/ src/
COPY --from=stage2 /app/model/model.csv /app/model/scaler.csv /app/model/
EXPOSE 5000
CMD ["python", "-m", "flask", "--app", "src.inference", "run", "--host=0.0.0.0", "--debug"]