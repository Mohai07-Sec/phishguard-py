import json
import csv
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import requests
from phishguard.cli import main


# === CSV TO JSON ===
def test_csv_to_json_success(tmp_path):
    csv_file = tmp_path / "data.csv"
    json_file = tmp_path / "out.json"
    csv_file.write_text("name,age\nAlice,30\nBob,25\n")

    main(["csv-to-json", str(csv_file), str(json_file)])

    data = json.loads(json_file.read_text())
    assert data[0]["name"] == "Alice"
    assert data[1]["age"] == "25"


def test_csv_to_json_file_not_found(caplog):
    with caplog.at_level("ERROR"):
        result = main(["csv-to-json", "missing.csv"])
    assert result == "[]"   # ✅ handler returns "[]" on error
    assert "No such file or directory" in caplog.text




# === JSON PRETTY ===
import json
from phishguard.cli import main

def test_json_pretty_valid(tmp_path):
    json_file = tmp_path / "data.json"
    json_file.write_text(json.dumps({"key": "value"}))

    result = main(["json-pretty", str(json_file)])   # ✅ returns a string
    assert '"key": "value"' in result

def test_json_pretty_invalid(tmp_path, caplog):
    bad_json = tmp_path / "bad.json"
    bad_json.write_text("{not valid json}")

    with caplog.at_level("ERROR"):
        result = main(["json-pretty", str(bad_json)])
    assert result == "{}"
    assert "Invalid JSON" in caplog.text



# === REGEX GREP ===
def test_regex_grep_match(tmp_path):
    text_file = tmp_path / "log.txt"
    text_file.write_text("error: something broke\ninfo: all good\n")

    result = main(["regex-grep", "error", str(text_file)])
    assert any("error:" in line for line in result)




def test_regex_grep_no_match(tmp_path, capsys):
    text_file = tmp_path / "log.txt"
    text_file.write_text("only info here\n")

    main(["regex-grep", "warning", str(text_file)])
    out, _ = capsys.readouterr()
    assert out.strip() == ""


def test_regex_grep_invalid_regex(tmp_path, caplog):
    text_file = tmp_path / "log.txt"
    text_file.write_text("hello\n")

    with caplog.at_level("ERROR"):
        result = main(["regex-grep", "*", str(text_file)])  # '*' is invalid regex
    assert result == []                                    # handler returns empty list
    assert "Invalid regex" in caplog.text



# === HTTP GET ===
def test_http_get_success(tmp_path):
    out_file = tmp_path / "page.html"
    fake_response = MagicMock()
    fake_response.content = b"Hello"
    fake_response.raise_for_status = MagicMock()

    with patch("requests.get", return_value=fake_response):
        main(["http-get", "http://example.com", str(out_file)])

    assert out_file.exists()
    assert b"Hello" in out_file.read_bytes()


def test_http_get_server_error(tmp_path, caplog):
    out_file = tmp_path / "page.html"
    fake_response = MagicMock()
    fake_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 error")

    with patch("requests.get", return_value=fake_response):
        with caplog.at_level("ERROR"):
            result = main(["http-get", "http://example.com", str(out_file)])
    assert result is None
    assert "HTTP GET failed" in caplog.text



# === HELP ===
def test_cli_help(capsys):
    with pytest.raises(SystemExit):
        main(["--help"])
    out, _ = capsys.readouterr()
    assert "usage" in out.lower()

def test_csv_to_json_success(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("name,age\nAlice,30\nBob,25\n")

    result = main(["csv-to-json", str(csv_file)])   # ✅ only one argument
    data = json.loads(result)
    assert data[0]["name"] == "Alice"
    assert data[1]["age"] == "25"

def test_cli_no_args(capsys):
    result = main([])
    out, _ = capsys.readouterr()
    assert "usage:" in out or result is None

import pytest

def test_cli_unknown_command():
    # argparse should exit with code 2 if the subcommand is invalid
    with pytest.raises(SystemExit) as e:
        main(["not-a-command"])
    assert e.value.code == 2


def test_cli_help(capsys):
    import sys
    from pytest import raises
    with raises(SystemExit):  # argparse exits on --help
        main(["--help"])

def test_regex_grep_no_match(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello world\n")
    result = main(["regex-grep", "error", str(file)])
    assert result == []
