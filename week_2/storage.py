# file handle logic
import os
import tempfile
# command line parse logic
import argparse
# data store logic
import json

storage_path = os.path.join(tempfile.gettempdir(), "storage.data")
parser = argparse.ArgumentParser()
parser.add_argument("--key", help="provide key")
parser.add_argument("--value", help="provide value")
args = parser.parse_args()
answer = None
if args.key:
    storage_exists = os.path.exists(storage_path)
    data = {}
    if storage_exists:
        with open(storage_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass
    # Got both key and value from command line
    if args.value:
        with open(storage_path, "w") as f:
            data[args.key] = data.get(args.key, list())
            data[args.key].append(args.value)
            f.write(json.dumps(data))
    # Got only key from command line
    else:
        if args.key in data and data is not None:
            answer = ", ".join(data[args.key])
        print(answer)
