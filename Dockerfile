FROM python:3.13-slim

WORKDIR /app

# Copy only the files needed for installation
COPY pyproject.toml ./
COPY parrot/ ./parrot/
COPY tests/ ./tests/

# Install the package directly
RUN pip install --no-cache-dir .

# Set environment variables
ENV HOST=0.0.0.0 \
    PORT=8080 \
    LOG_FORMAT=json \
    LOG_LEVEL=INFO

# Expose the port
EXPOSE 8080

# Run the server
CMD ["parrot", "serve"]
