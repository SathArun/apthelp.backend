#!/bin/bash
set -e

PORT=${PORT:-80}
export PORT


# Render nginx config from template
envsubst '${PORT}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Start supervisord which will start nginx, uvicorn and streamlit
exec /usr/bin/supervisord -n
