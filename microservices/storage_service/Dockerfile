FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment variables
ENV PYTHONPATH=/app

ENTRYPOINT ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port 8011"]