import csv
import json
import logging

def handle_csv_to_json(args):
    try:
        with open(args.file, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)
        return json.dumps(data, indent=2)
    except Exception as e:
        logging.error(f"CSV to JSON failed: {e}")
        return "[]"
