import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("phishguard")

import argparse
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def json_pretty(input_file: str) -> None:
    """Pretty-print a JSON file to stdout."""
    try:
        path = Path(input_file)
        data = json.loads(path.read_text(encoding="utf-8"))
        logger.info("Pretty-printed JSON file")
        print(json.dumps(data, indent=4, ensure_ascii=False))
    except Exception as e:
        logger.error(f"Failed to pretty print JSON: {e}")
        raise


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ops-toolkit",
        description="PhishGuard Operations Toolkit"
    )
    subparsers = parser.add_subparsers(dest="command")

    # json-pretty
    json_parser = subparsers.add_parser("json-pretty", help="Pretty print JSON file")
    json_parser.add_argument("input_file", help="Path to JSON file")

    args = parser.parse_args()

    if args.command == "json-pretty":
        json_pretty(args.input_file)
    else:
        parser.print_help()

import csv

def csv_to_json(input_file: str, output_file: str) -> None:
    """Convert a CSV file to JSON and save it."""
    try:
        with open(input_file, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)

        with open(output_file, "w", encoding="utf-8") as jsonfile:
            json.dump(data, jsonfile, indent=4, ensure_ascii=False)

        logger.info(f"Converted {input_file} -> {output_file}")
    except Exception as e:
        logger.error(f"Failed to convert CSV to JSON: {e}")
        raise


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ops-toolkit",
        description="PhishGuard Operations Toolkit"
    )
    subparsers = parser.add_subparsers(dest="command")

    # json-pretty
    json_parser = subparsers.add_parser("json-pretty", help="Pretty print JSON file")
    json_parser.add_argument("input_file", help="Path to JSON file")

    # csv-to-json
    csv_parser = subparsers.add_parser("csv-to-json", help="Convert CSV file to JSON")
    csv_parser.add_argument("input_file", help="Path to CSV file")
    csv_parser.add_argument("output_file", help="Path to output JSON file")

    args = parser.parse_args()

    if args.command == "json-pretty":
        json_pretty(args.input_file)
    elif args.command == "csv-to-json":
        csv_to_json(args.input_file, args.output_file)
    else:
        parser.print_help()

import re

def regex_grep(pattern: str, input_file: str) -> None:
    logger.info(f"Searching for pattern '{pattern}' in {input_file}")
    """Search for regex pattern in a file and print matching lines."""
    try:
        regex = re.compile(pattern)
        with open(input_file, "r", encoding="utf-8") as f:
            for line in f:
                if regex.search(line):
                    print(line.strip())
    except Exception as e:
        logger.error(f"Failed to grep with pattern '{pattern}': {e}")
        raise

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ops-toolkit",
        description="PhishGuard Operations Toolkit"
    )
    subparsers = parser.add_subparsers(dest="command")

    # json-pretty
    json_parser = subparsers.add_parser("json-pretty", help="Pretty print JSON file")
    json_parser.add_argument("input_file", help="Path to JSON file")

    # csv-to-json
    csv_parser = subparsers.add_parser("csv-to-json", help="Convert CSV file to JSON")
    csv_parser.add_argument("input_file", help="Path to CSV file")
    csv_parser.add_argument("output_file", help="Path to output JSON file")

    # regex-grep
    grep_parser = subparsers.add_parser("regex-grep", help="Search file with regex")
    grep_parser.add_argument("pattern", help="Regex pattern")
    grep_parser.add_argument("input_file", help="Path to file")

    args = parser.parse_args()

    if args.command == "json-pretty":
        json_pretty(args.input_file)
    elif args.command == "csv-to-json":
        csv_to_json(args.input_file, args.output_file)
    elif args.command == "regex-grep":
        regex_grep(args.pattern, args.input_file)
    else:
        parser.print_help()

import requests
from requests.exceptions import RequestException

def http_get(url: str, output_file: str, retries: int = 3, timeout: int = 5) -> None:
    """Download content from URL and save to file with retries and timeout."""
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            with open(output_file, "wb") as f:
                f.write(response.content)
            logger.info(f"Downloaded {url} -> {output_file}")
            return
        except RequestException as e:
            logger.warning(f"Attempt {attempt} failed: {e}")
            if attempt == retries:
                logger.error(f"Failed to fetch {url} after {retries} attempts")
                raise

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ops-toolkit",
        description="PhishGuard Operations Toolkit"
    )
    subparsers = parser.add_subparsers(dest="command")

    # json-pretty
    json_parser = subparsers.add_parser("json-pretty", help="Pretty print JSON file")
    json_parser.add_argument("input_file", help="Path to JSON file")

    # csv-to-json
    csv_parser = subparsers.add_parser("csv-to-json", help="Convert CSV file to JSON")
    csv_parser.add_argument("input_file", help="Path to CSV file")
    csv_parser.add_argument("output_file", help="Path to output JSON file")

    # regex-grep
    grep_parser = subparsers.add_parser("regex-grep", help="Search file with regex")
    grep_parser.add_argument("pattern", help="Regex pattern")
    grep_parser.add_argument("input_file", help="Path to file")

    # http-get
    get_parser = subparsers.add_parser("http-get", help="Download a URL to a file")
    get_parser.add_argument("url", help="URL to fetch")
    get_parser.add_argument("output_file", help="Path to save response")

    args = parser.parse_args()

    if args.command == "json-pretty":
        json_pretty(args.input_file)
    elif args.command == "csv-to-json":
        csv_to_json(args.input_file, args.output_file)
    elif args.command == "regex-grep":
        regex_grep(args.pattern, args.input_file)
    elif args.command == "http-get":
        http_get(args.url, args.output_file)
    else:
        parser.print_help()




