import tempfile
import os
import pytest
from phishguard.cli import http_get

# We will mock requests so tests don't hit real internet
import requests
from unittest.mock import patch, MagicMock


def test_http_get_success(tmp_path):
    url = "http://example.com"
    output_file = tmp_path / "output.html"

    fake_response = MagicMock()
    fake_response.content = b"<html>Hello</html>"
    fake_response.raise_for_status = MagicMock()

    with patch("requests.get", return_value=fake_response):
        http_get(url, str(output_file), retries=1)

    # Verify file was written
    assert output_file.exists()
    assert b"Hello" in output_file.read_bytes()


def test_http_get_failure(tmp_path):
    url = "http://bad-url.com"
    output_file = tmp_path / "output.html"

    with patch("requests.get", side_effect=requests.exceptions.RequestException("boom")):
        with pytest.raises(requests.exceptions.RequestException):
            http_get(url, str(output_file), retries=2)


import pytest
from phishguard.cli import http_get
import requests
from unittest.mock import patch, MagicMock


def test_http_get_success(tmp_path):
    url = "http://example.com"
    output_file = tmp_path / "output.html"

    fake_response = MagicMock()
    fake_response.content = b"<html>Hello</html>"
    fake_response.raise_for_status = MagicMock()

    with patch("requests.get", return_value=fake_response):
        http_get(url, str(output_file), retries=1)

    assert output_file.exists()
    assert b"Hello" in output_file.read_bytes()


def test_http_get_failure(tmp_path):
    url = "http://bad-url.com"
    output_file = tmp_path / "output.html"

    with patch("requests.get", side_effect=requests.exceptions.RequestException("boom")):
        with pytest.raises(requests.exceptions.RequestException):
            http_get(url, str(output_file), retries=2)
