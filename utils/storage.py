import json
import os

def save_data(data, filename="data/cli.json"):
    with open(filename, "w", encoding="utf-8") as f:
        
        if data and hasattr(data[0], 'to_dict'):
            json.dump([item.to_dict() for item in data], f, indent=4)
        else:

            json.dump(data, f, indent=4)

def load_data(filename="data/cli.json"):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []