FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy and make start script executable
COPY start.sh .
RUN chmod +x start.sh

# Default port (Railway will override via PORT env var)
ENV PORT=8000
EXPOSE 8000

# Run via start script
ENTRYPOINT ["./start.sh"]
