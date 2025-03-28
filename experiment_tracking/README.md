Your setup consists of a FastAPI-based loan approval API containerized using Docker, orchestrated with Docker Compose, and fronted by Nginx for load balancing. Below is a detailed breakdown of what happens at each step.

---

## **Step 1: `docker build -t loan-approval-api .`**
This command builds the Docker image for your FastAPI service. Let's break it down:

### **1.1 Base Image Selection**
```dockerfile
FROM python:3.10-slim AS base
```
- Uses `python:3.10-slim`, a lightweight Python image optimized for production.
- "Slim" images contain only essential dependencies, reducing attack surface and image size.

### **1.2 Setting Up Work Directory**
```dockerfile
WORKDIR /app
```
- The working directory inside the container is set to `/app`, ensuring all following commands execute within this directory.

### **1.3 Copying Requirements File and Installing Dependencies**
```dockerfile
COPY requirements.txt ./
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt
```
- `COPY requirements.txt ./` copies the `requirements.txt` file.
- `python -m venv /opt/venv` creates a virtual environment in `/opt/venv`.
- `/opt/venv/bin/pip install --no-cache-dir -r requirements.txt` installs dependencies inside this virtual environment.
- Using a virtual environment prevents conflicts with system packages.

### **1.4 Setting Virtual Environment as Default**
```dockerfile
ENV PATH="/opt/venv/bin:$PATH"
```
- Ensures that when commands are run inside the container, they automatically use the virtual environment's Python and pip.

### **1.5 Copying the Remaining Project Files**
```dockerfile
COPY . .
```
- Copies the entire application source code into the container.

### **1.6 Defining Volumes**
```dockerfile
VOLUME ["/app/data", "/app/models"]
```
- These directories are mapped as Docker volumes to persist processed data and models outside the container.

### **1.7 Exposing the Application Port**
```dockerfile
EXPOSE 8000
```
- The container listens on port `8000` for incoming traffic.

### **1.8 Defining the Start Command**
```dockerfile
CMD ["uvicorn", "src.inference:app", "--host", "0.0.0.0", "--port", "8000"]
```
- Starts the FastAPI application using Uvicorn.
- `--host 0.0.0.0` ensures the app is accessible from outside the container.
- `--port 8000` binds it to port 8000.

### **1.9 Image is Built**
- Docker runs all the above instructions, resulting in an image tagged as `loan-approval-api`.

---

## **Step 2: `docker-compose up --build -d`**
This command:
1. **Builds the services defined in `docker-compose.yml`.**
2. **Creates and starts the containers in detached mode (`-d`).**

### **2.1 Loan API Service (`loan-api`)**
```yaml
services:
  loan-api:
    build: .
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    deploy:
      replicas: 3
    networks:
      - loan-net
    expose:
      - "8000"
```
- `build: .` instructs Docker to use the `Dockerfile` to create the `loan-api` container.
- `volumes:` maps the `./data` and `./models` directories from the host machine to persist data.
- `deploy.replicas: 3` creates **three replicas** of the `loan-api` service, ensuring redundancy and load balancing.
- `networks:` connects the container to `loan-net`, a Docker network for inter-container communication.
- `expose: 8000` allows the service to listen on port `8000` **internally**, without exposing it directly to the host.

### **2.2 Nginx Load Balancer**
```yaml
  nginx:
    image: nginx:latest
    ports:
      - "8000:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - loan-api
    networks:
      - loan-net
```
- Uses `nginx:latest` as the image.
- `ports: - "8000:80"` forwards traffic from **port 8000 (host machine)** to **port 80 (Nginx inside the container)**.
- `volumes:` mounts `nginx.conf` inside the container as **read-only** (`ro`).
- `depends_on: loan-api` ensures Nginx starts **after** the FastAPI containers are running.
- Connected to `loan-net` so it can route requests to `loan-api` replicas.

### **2.3 Network Configuration**
```yaml
networks:
  loan-net:
    driver: bridge
```
- Defines `loan-net`, a **bridge network**, allowing containers to communicate internally.

---

## **Nginx Load Balancing Configuration**
```nginx
http {
    upstream loan_api_cluster {
        least_conn;
        server loan-api:8000;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://loan_api_cluster;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
```
- `upstream loan_api_cluster` defines a load-balancing cluster of `loan-api` containers.
- `least_conn;` ensures traffic is sent to the **least busy** container.
- `server { listen 80; }` makes Nginx listen on port **80** inside the container.
- `proxy_pass http://loan_api_cluster;` forwards requests to `loan-api` replicas.

---

## **Final Execution Flow**
1. **Docker Compose builds the `loan-api` image** and starts **3 instances** of the API.
2. **Nginx starts** and reads `nginx.conf`, setting up load balancing.
3. **Nginx listens on port 8000 (host machine)** and forwards requests to `loan-api` containers.
4. **Incoming requests are routed to the least-busy FastAPI container**, ensuring balanced load.

---

## **Expected Outcome**
- Running `docker ps` should show:
  - 3 running `loan-api` containers.
  - 1 running `nginx` container.
- Navigating to `http://localhost:8000/` should route requests to `loan-api` instances.
- If one `loan-api` container crashes, Nginx will automatically distribute requests among the remaining ones.

---

## **Potential Issues & Fixes**
1. **Port Conflict (`Bind for 0.0.0.0:8000 failed`)**
   - Another process may be using port `8000`.
   - Fix: Change `ports:` in `docker-compose.yml` (`- "8080:80"` instead of `8000:80`).

2. **Nginx Not Routing Requests (`502 Bad Gateway`)**
   - The `loan-api` service might not be running.
   - Fix: Run `docker-compose logs loan-api` and check errors.

3. **Changes to Code Not Reflected**
   - Docker caches layers, so updates may not apply.
   - Fix: Run `docker-compose up --build -d` to force a rebuild.

---

## **Conclusion**
Your setup efficiently:
- **Builds a Python-based FastAPI application in Docker.**
- **Deploys it as a scalable service with three replicas.**
- **Uses Nginx to load balance traffic across API instances.**
- **Ensures persistent storage for data and models.**

This architecture is **robust** and **scalable**, making it suitable for production deployment. 🚀