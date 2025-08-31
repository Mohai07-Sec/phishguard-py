import json
import tempfile
from phishguard.cli import json_pretty

def test_json_pretty_print(capsys):
    data = {"hello": "world"}
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json") as tmp:
        json.dump(data, tmp)
        tmp_path = tmp.name

    json_pretty(tmp_path)
    captured = capsys.readouterr()

    assert '"hello": "world"' in captured.out
    assert captured.out.strip().startswith("{")
    assert captured.out.strip().endswith("}")

def test_json_pretty_invalid(tmp_path, caplog):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{not: valid}")
    from phishguard.cli import main
    with caplog.at_level("ERROR"):
        result = main(["json-pretty", str(bad_file)])
    assert "Invalid JSON" in caplog.text
