import click
import requests
import signal
import sys
import time
from threading import Timer
from rich.console import Console

from . import parrot
from .config import config

console = Console()


@click.group()
def cli():
    """Parrot - A tool for HTTP request/response handling."""
    pass


@cli.command()
@click.option("--port", default=None, type=int, help="Port to run the server on (overrides PORT env var)")
@click.option("--host", default=None, help="Host to bind to (overrides HOST env var)")
@click.option("--log-format", type=click.Choice(["pretty", "json"]), default=None, 
              help="Logging format (overrides LOG_FORMAT env var)")
def serve(port, host, log_format):
    """Start the HTTP echo server."""
    if port is not None:
        config.port = port
    if host is not None:
        config.host = host
    if log_format is not None:
        config.log_format = log_format

    server_address = (config.host, config.port)
    httpd = parrot.HTTPServer(server_address, parrot.RequestHandler)
    console.print(
        f"Server running on [bold blue]http://localhost:{config.port}[/bold blue] 🦜"
    )

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        console.print("Server stopped")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}", style="red")
        sys.exit(1)


@cli.command()
@click.argument(
    "method", type=click.Choice(["get", "post", "put", "delete"], case_sensitive=False)
)
@click.argument("url")
@click.option("--data", "-d", help="Data to send with the request")
@click.option("--headers", "-h", multiple=True, help="Headers in format key:value")
def request(method, url, data, headers):
    """Make HTTP requests and display responses."""
    headers_dict = {}
    for header in headers or []:
        key, value = header.split(":", 1)
        headers_dict[key.strip()] = value.strip()

    try:
        response = getattr(requests, method.lower())(
            url, data=data, headers=headers_dict
        )

        console.print("\n=== Request Details 🦜===")
        console.print(f"[bold blue]Method:[/bold blue] {method.upper()}")
        console.print(f"[bold blue]URL:[/bold blue] {url}")
        if headers_dict:
            console.print("[bold blue]Headers:[/bold blue]")
            console.print(headers_dict, style="dark_green")
        if data:
            console.print("[bold blue]Body:[/bold blue]")
            console.print(data, style="yellow")

        console.print("\n=== Response Details 🦜===")
        console.print(f"[bold blue]Status:[/bold blue] {response.status_code}")
        console.print("[bold blue]Headers:[/bold blue]")
        console.print(dict(response.headers), style="dark_green")
        console.print("[bold blue]Body:[/bold blue]")
        try:
            console.print(response.json(), style="yellow")
        except ValueError:
            console.print(response.text, style="yellow")

    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise click.Abort()


@cli.command()
def version():
    """Show version information."""
    from importlib.metadata import version

    v = version("parrot")
    console.print(f"Parrot version: [bold blue]{v}[/bold blue] 🦜")


if __name__ == "__main__":
    cli()
