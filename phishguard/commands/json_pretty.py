import json
import logging

def handle_json_pretty(args):
    try:
        with open(args.file, "r") as f:
            data = json.load(f)
        return json.dumps(data, indent=2)
    except Exception as e:
        logging.error(f"Invalid JSON: {e}")
        return "{}"
