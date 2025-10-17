# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y git && apt-get clean
# Install dependencies
COPY requirements.txt .
COPY .env .env
COPY entrypoint.sh /entrypoint.sh
COPY create_initial_user.py create_initial_user.py
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

RUN pip install gunicorn \
&& chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
