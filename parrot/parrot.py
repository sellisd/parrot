import json
import logging
import time
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer as BaseHTTPServer
from typing import Dict, Any
from uuid import uuid4

from rich.console import Console
from rich.logging import RichHandler

from .config import config

# Start time for uptime calculation
START_TIME = time.time()
REQUEST_COUNT = 0

# Configure logging based on configuration
if config.log_format == "json":
    logging.basicConfig(
        level=config.log_level,
        format='{"timestamp":"%(asctime)s", "level":"%(levelname)s", "message":"%(message)s"}',
        datefmt="%Y-%m-%d %H:%M:%S",
    )
else:
    logging.basicConfig(
        level=config.log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )

logger = logging.getLogger("parrot")
console = Console()


class RequestHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"  # Set HTTP version

    def _log_request(self, request_id: str, data: Dict[str, Any]) -> None:
        """Log request details in the configured format."""
        if config.log_format == "json":
            log_data = {
                "request_id": request_id,
                "method": self.command,
                "path": self.path,
                "headers": dict(self.headers),
                **data,
            }
            logger.info(json.dumps(log_data))
        else:
            logger.info(f"=== New Request 🦜 (ID: {request_id}) ===")
            logger.info(f"[bold blue]Method:[/bold blue] {self.command}")
            logger.info(f"[bold blue]Path:[/bold blue] {self.path}")
            logger.info("[bold blue]Headers:[/bold blue]")
            console.print(dict(self.headers), style="dark_green")
            if data.get("body"):
                logger.info("[bold blue]Body:[/bold blue]")
                console.print(data["body"], style="yellow")

    def _handle_request(self):
        """Generic handler for all HTTP methods"""

        # Read body if present
        content_length = int(self.headers.get("Content-Length", 0))
        body = None
        if content_length > 0:
            body = self.rfile.read(content_length).decode("utf-8")

        # Create response data
        response = {
            "method": self.command,
            "path": self.path,
            "headers": dict(self.headers),
        }
        if body:
            response["body"] = body

        # Send response
        response_data = json.dumps(response).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_data)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(response_data)
        self.wfile.flush()

    def _handle_health_check(self):
        """Handle health check requests."""
        health_data = {
            "status": "healthy",
            "uptime": int(time.time() - START_TIME),
            "request_count": REQUEST_COUNT,
        }

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(health_data).encode())

    def do_GET(self):
        self._handle_request()

    def do_POST(self):
        self._handle_request()

    def do_PUT(self):
        self._handle_request()

    def do_DELETE(self):
        self._handle_request()


# Re-export HTTPServer for use in cli.py
HTTPServer = BaseHTTPServer
