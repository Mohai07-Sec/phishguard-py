import requests
import logging

def handle_http_get(args):
    try:
        for attempt in range(args.retries):
            try:
                resp = requests.get(args.url, timeout=args.timeout)
                resp.raise_for_status()
                with open(args.outfile, "wb") as f:
                    f.write(resp.content)
                logging.info(f"Saved {args.url} -> {args.outfile}")
                return str(args.outfile)
            except requests.exceptions.Timeout:
                logging.warning(f"Timeout, retrying {attempt+1}/{args.retries}...")
        logging.error("All retries failed due to timeout")
        return None
    except Exception as e:
        logging.error(f"HTTP GET failed: {e}")
        return None
