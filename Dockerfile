FROM python:3.12-slim

# Prevents Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port (documentation only)
EXPOSE 8000

# Run with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
