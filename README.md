# Parrot 🦜

A command line tool for HTTP request/response handling. Features an HTTP echo server and a request client with rich output formatting.

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for fast Python package installation and environment management.

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows

# Install dependencies and package
uv pip install .
```

### Benefits of using uv:
- Significantly faster installation times
- Built-in virtual environment management
- Reliable dependency resolution
- Binary wheels support for improved performance

## Usage

Parrot provides three main commands:

### 1. Starting the Echo Server

```bash
# Start server on default port 8080
parrot serve

# Start server on custom port
parrot serve --port 3000
```

The echo server will display details of any HTTP requests it receives, including:
- Method
- Path
- Headers
- Body (if present)

### 2. Making HTTP Requests

```bash
# GET request
parrot request get http://example.com

# POST request with data
parrot request post http://api.example.com/data -d '{"key": "value"}'

# Request with custom headers
parrot request get http://api.example.com -h "Authorization:Bearer token" -h "Accept:application/json"
```

The request command will display both the request and response details with colored formatting.

### 3. Version Information

```bash
parrot version
```

## Features

- HTTP echo server for debugging requests
- Rich terminal output with colors and formatting
- Support for GET, POST, PUT, DELETE methods
- Custom headers and request body support
- Version tracking

## License

MIT License
