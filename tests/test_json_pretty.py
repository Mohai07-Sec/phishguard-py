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
