FROM python:3.11-slim

WORKDIR /app

# Install basic tools and curl for healthcheck
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy proyect's source code
COPY . .

RUN mkdir -p /app/storage

# Install proyect in dev mode
RUN pip install -e .

EXPOSE 3000