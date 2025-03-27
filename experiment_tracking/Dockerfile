# Use an official Python image as base
FROM python:3.10-slim AS base

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first to leverage Docker's caching
COPY requirements.txt ./

# Create a virtual environment & install dependencies inside it
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Set the virtual environment as default
ENV PATH="/opt/venv/bin:$PATH"

# Now copy the rest of the project
COPY . .

# Use a volume for storing processed data & models outside the container
VOLUME ["/app/data", "/app/models"]

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "src.inference:app", "--host", "0.0.0.0", "--port", "8000"]
