import re
import tempfile
from phishguard.cli import regex_grep

def test_regex_grep_matches(capsys, tmp_path):
    # Create a temporary log file
    log_file = tmp_path / "app.log"
    log_file.write_text("INFO: User login\nERROR: Disk full\nINFO: Shutdown\n", encoding="utf-8")

    # Run regex_grep
    regex_grep("ERROR", str(log_file))
    captured = capsys.readouterr()

    assert "ERROR: Disk full" in captured.out
    assert "INFO" not in captured.out


def test_regex_grep_no_matches(capsys, tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text("DEBUG: All good\nINFO: Running\n", encoding="utf-8")

    regex_grep("ERROR", str(log_file))
    captured = capsys.readouterr()

    assert captured.out.strip() == ""  # no output expected
