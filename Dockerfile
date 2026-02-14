FROM python:3.12.5-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p static/img/news

# Expose port (Railway will provide PORT env var)
EXPOSE 8000

# Start the application
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:8000"]
