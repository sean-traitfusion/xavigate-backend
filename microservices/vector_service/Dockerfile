FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y git build-essential
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY . .

# Default environment variable for module path
ENV PYTHONPATH=/app

# Launch the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8017"]
