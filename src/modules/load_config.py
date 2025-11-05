import json

def load_config(path: str = 'config.json') -> dict:
    """Load and return the bot configuration from a JSON file."""
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"Configuration file '{path}' not found.")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON in '{path}': {e}")