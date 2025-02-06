FROM python:3.11-slim as builder

WORKDIR /app

# Copy only the files needed for installation
COPY pyproject.toml ./
COPY parrot/ ./parrot/

# Install build dependencies and build the package
RUN pip install --no-cache-dir build && \
    python -m build

# Start fresh with a clean image
FROM python:3.11-slim

WORKDIR /app

# Copy the built package from the builder stage
COPY --from=builder /app/dist/*.whl .

# Install the package
RUN pip install --no-cache-dir *.whl && \
    rm *.whl

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=8080
ENV LOG_FORMAT=json
ENV LOG_LEVEL=INFO

# Expose the port
EXPOSE 8080

# Run the server
CMD ["parrot", "serve"]
