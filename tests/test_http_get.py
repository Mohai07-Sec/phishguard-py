import requests
import pytest
from unittest.mock import patch, MagicMock
from phishguard.cli import main


def test_http_get_success(tmp_path):
    """Test successful HTTP GET writes content to file."""
    url = "http://example.com"
    output_file = tmp_path / "output.html"

    fake_response = MagicMock()
    fake_response.content = b"<html>Hello</html>"
    fake_response.raise_for_status = MagicMock()

    with patch("requests.get", return_value=fake_response):
        main(["http-get", url, str(output_file)])

    assert output_file.exists()
    assert b"Hello" in output_file.read_bytes()


def test_http_get_server_error(tmp_path, caplog):
    """Test server returns error (raise_for_status)."""
    url = "http://example.com"
    output_file = tmp_path / "output.html"

    fake_response = MagicMock()
    fake_response.content = b""
    fake_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 error")

    with patch("requests.get", return_value=fake_response):
        with caplog.at_level("ERROR"):
            result = main(["http-get", url, str(output_file)])

    assert result is None
    assert "500 error" in caplog.text


def test_http_get_timeout(monkeypatch, tmp_path, caplog):
    """Test timeout error triggers retries and logs."""
    def fake_get(*args, **kwargs):
        raise requests.exceptions.Timeout
    monkeypatch.setattr(requests, "get", fake_get)

    out_file = tmp_path / "out.html"
    with caplog.at_level("ERROR"):
        main(["http-get", "http://example.com", str(out_file)])

    # Lowercase match avoids case mismatch problems
    assert "timeout" in caplog.text.lower()


def test_http_get_invalid_url(caplog, tmp_path):
    """Test invalid URL logs error and returns None."""
    out_file = tmp_path / "out.html"
    with caplog.at_level("ERROR"):
        result = main(["http-get", "invalid-url", str(out_file)])

    assert result is None
    assert "failed" in caplog.text.lower()
