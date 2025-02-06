import logging
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer as BaseHTTPServer

from rich.console import Console
from rich.logging import RichHandler

# Configure Rich logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

logger = logging.getLogger("parrot")
console = Console()


class RequestHandler(BaseHTTPRequestHandler):
    def _handle_request(self):
        logger.info("=== New Request 🦜===")
        logger.info(f"[bold blue]Method:[/bold blue] {self.command}")
        logger.info(f"[bold blue]Path:[/bold blue] {self.path}")
        logger.info("[bold blue]Headers:[/bold blue]")
        console.print(dict(self.headers), style="dark_green")
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            body = self.rfile.read(content_length).decode("utf-8")
            logger.info("[bold blue]Body:[/bold blue]")
            console.print(body, style="yellow")
        # Send a basic response
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Request received")

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
