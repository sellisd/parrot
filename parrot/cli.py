import click
from rich.console import Console
import requests
from . import parrot

console = Console()

@click.group()
def cli():
    """Parrot - A tool for HTTP request/response handling."""
    pass

@cli.command()
@click.option('--port', default=8080, help='Port to run the server on')
def serve(port):
    """Start the HTTP echo server."""
    server_address = ("", port)
    httpd = parrot.HTTPServer(server_address, parrot.RequestHandler)
    console.print(f"Server running on [bold blue]http://localhost:{port}[/bold blue] 🦜")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        console.print("\nShutting down server...")
        httpd.server_close()

@cli.command()
@click.argument('method', type=click.Choice(['get', 'post', 'put', 'delete'], case_sensitive=False))
@click.argument('url')
@click.option('--data', '-d', help='Data to send with the request')
@click.option('--headers', '-h', multiple=True, help='Headers in format key:value')
def request(method, url, data, headers):
    """Make HTTP requests and display responses."""
    headers_dict = {}
    for header in headers or []:
        key, value = header.split(':', 1)
        headers_dict[key.strip()] = value.strip()

    try:
        response = getattr(requests, method.lower())(
            url,
            data=data,
            headers=headers_dict
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

if __name__ == '__main__':
    cli()
