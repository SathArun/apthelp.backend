FROM python:3.11-slim-bookworm

# Install system deps and nginx
RUN apt-get update && apt-get install -y curl build-essential supervisor nginx gettext-base && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY backend backend
COPY frontend frontend
COPY healthcheck.py /app/ 
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY nginx.conf.template /etc/nginx/nginx.conf.template
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80

CMD ["/start.sh"]
