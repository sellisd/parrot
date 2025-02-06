import json
from http.client import HTTPConnection
from threading import Thread
import threading
import requests
import logging

import pytest

from parrot.parrot import HTTPServer, RequestHandler

logger = logging.getLogger(__name__)

@pytest.fixture
def server():
    """Start a test server in a separate thread."""
    server = HTTPServer(("", 0), RequestHandler)  # Port 0 lets OS choose free port
    server_thread = Thread(target=server.serve_forever)
    server_thread.daemon = True  # Thread will be terminated when main thread ends
    server_thread.start()
    logger.debug("Server started on port %s", server.server_port)
    yield server
    server.shutdown()
    server.server_close()
    logger.debug("Server shutdown")

class TestHTTPServer:
    @pytest.fixture(autouse=True)
    def setup_server(self):
        """Setup test server before each test method"""
        self.server = HTTPServer(('0.0.0.0', 0), RequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.port = self.server.server_port
        logger.debug("Server started on port %s", self.port)
        yield
        self.server.shutdown()
        self.server.server_close()
        logger.debug("Server shutdown")

    def test_get_request(self):
        """Test GET request with complete response validation"""
        response = requests.get(
            f'http://localhost:{self.port}/test',
            timeout=5
        )
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'

    def test_post_request(self):
        """Test POST request with body."""
        conn = HTTPConnection(f"localhost:{self.port}")
        data = json.dumps({"test": "data"})
        headers = {"Content-Type": "application/json"}

        conn.request("POST", "/test", body=data, headers=headers)
        response = conn.getresponse()

        assert response.status == 200
        assert response.getheader("Content-type") == "application/json"
