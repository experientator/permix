FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY *.py ./
COPY requirements.txt ./
COPY data.db ./

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set environment variables
ENV DISPLAY=host.docker.internal:0
ENV PYTHONPATH=/app

# Run the application
CMD ["python", "main.py"]