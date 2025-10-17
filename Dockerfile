# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y git && apt-get clean
# Install dependencies
COPY requirements.txt .
COPY .env .env
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

RUN pip install gunicorn

CMD ["gunicorn", "run:app", "--bind", "0.0.0.0:8080"]

