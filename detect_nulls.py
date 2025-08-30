import os

def scan_for_nulls(root_dir="."):
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith(".py"):
                path = os.path.join(dirpath, f)
                with open(path, "rb") as fh:
                    content = fh.read()
                    if b"\x00" in content:
                        print(f"Null byte found in {path}")

if __name__ == "__main__":
    scan_for_nulls(".")
