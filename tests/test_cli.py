import pytest
from click.testing import CliRunner
from parrot.cli import cli

@pytest.fixture
def runner():
    return CliRunner()

def test_cli_help_output(runner):
    """Test that CLI help shows all commands."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    # Verify all commands are listed
    assert "serve" in result.output
    assert "request" in result.output
    assert "version" in result.output

def test_version_command(runner):
    """Test version command output."""
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert "Parrot version:" in result.output

def test_request_command_basic(runner, mocker):
    """Test basic GET request functionality."""
    # Mock requests.get to avoid actual HTTP calls
    mock_response = mocker.patch("requests.get")
    mock_response.return_value.status_code = 200
    mock_response.return_value.headers = {"Content-Type": "application/json"}
    mock_response.return_value.json.return_value = {"status": "ok"}

    result = runner.invoke(cli, ["request", "get", "http://example.com"])
    assert result.exit_code == 0
    assert result.output.count("Content-Type") == 1  # Only in response headers
    assert "{'status': 'ok'}" in result.output
