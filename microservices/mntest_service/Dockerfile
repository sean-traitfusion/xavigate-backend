FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY . .

# Expose port
EXPOSE 8016

# Default environment path
ENV PYTHONPATH=/app

# Launch the MN Test service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8016"]