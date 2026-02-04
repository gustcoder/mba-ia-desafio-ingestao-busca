# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /src

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file if it exists
COPY requirements.txt* ./

# Default .env in image (used when no volume mount overrides /src)
COPY .env.example .env

# Install Python dependencies
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Copy application code
COPY . .

# Entrypoint: ensure .env exists from .env.example at runtime (e.g. when using volume mount)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Default command (can be overridden in docker-compose)
CMD ["python", "--version"]

