# Use official Python image
FROM python:3.10  # Use Python 3.10 instead of 3.11


# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run migrations and start Django server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "stock_alerts.wsgi:application"]
