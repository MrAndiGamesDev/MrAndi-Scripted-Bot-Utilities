import json
from pathlib import Path
from typing import Any, Dict

def load_config(path: str = 'config.json') -> Dict[str, Any]:
    """Load and return the bot configuration from a JSON file."""
    user = Path(path).expanduser()
    config_path = user.resolve()
    if not config_path.is_file():
        raise RuntimeError(f"Configuration file '{config_path}' not found.")
    try:
        with config_path.open(encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON in '{config_path}': {e}")