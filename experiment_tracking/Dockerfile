# Use an official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy only the necessary files first (to optimize build caching)
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Run preprocessing and training scripts
RUN python src/preprocess.py && \
    python src/train.py

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "src.inference:app", "--host", "0.0.0.0", "--port", "8000"]
