import csv
import json
import tempfile
from phishguard.cli import csv_to_json

def test_csv_to_json(tmp_path):
    # Create a temporary CSV
    csv_file = tmp_path / "input.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "age"])
        writer.writeheader()
        writer.writerow({"name": "MoHay", "age": "22"})
        writer.writerow({"name": "Alice", "age": "30"})

    # Path for output JSON
    json_file = tmp_path / "output.json"

    # Run converter
    csv_to_json(str(csv_file), str(json_file))

    # Validate JSON content
    with open(json_file, encoding="utf-8") as f:
        data = json.load(f)

    assert isinstance(data, list)
    assert data[0]["name"] == "MoHay"
    assert data[1]["age"] == "30"
