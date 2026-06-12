import json
import os


def save_data(data, filename="data/cli.json"):
    """Save data to JSON file. Works with both dicts and objects."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    if data and hasattr(data[0], 'to_dict'):
        data = [item.to_dict() for item in data]

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_data(filename="data/cli.json"):
    """Load data from JSON file."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []
