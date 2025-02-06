import json
from http.client import HTTPConnection
from threading import Thread

import pytest

from parrot.parrot import HTTPServer, RequestHandler


@pytest.fixture
def server():
    """Start a test server in a separate thread."""
    server = HTTPServer(("", 0), RequestHandler)  # Port 0 lets OS choose free port
    server_thread = Thread(target=server.serve_forever)
    server_thread.daemon = True  # Thread will be terminated when main thread ends
    server_thread.start()
    yield server
    server.shutdown()
    server.server_close()


def test_server_get_request(server):
    """Test basic GET request handling."""
    conn = HTTPConnection(f"localhost:{server.server_port}")
    conn.request("GET", "/test")
    response = conn.getresponse()

    assert response.status == 200
    assert response.getheader("Content-type") == "text/plain"
    assert response.read() == b"Request received"


def test_server_post_request(server):
    """Test POST request with body."""
    conn = HTTPConnection(f"localhost:{server.server_port}")
    data = json.dumps({"test": "data"})
    headers = {"Content-Type": "application/json"}

    conn.request("POST", "/test", body=data, headers=headers)
    response = conn.getresponse()

    assert response.status == 200
    assert response.getheader("Content-type") == "text/plain"
    assert response.read() == b"Request received"
