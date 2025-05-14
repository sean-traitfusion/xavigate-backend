FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY . .

# Expose port
EXPOSE 8015

# Ensure imports from /app
ENV PYTHONPATH=/app

# Launch the chat service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8015"]