FROM python:3.11-slim-bookworm

# Install system deps
RUN apt-get update && apt-get install -y curl build-essential supervisor && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY backend backend
COPY frontend frontend
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8080

CMD ["/usr/bin/supervisord"]
