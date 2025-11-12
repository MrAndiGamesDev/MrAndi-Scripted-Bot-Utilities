import json
from pathlib import Path
from typing import Any, Dict, Optional

class JsonLoader:
    def __init__(self, path: str = 'config.json') -> None:
        self.path: Optional[str, Path] = path
        self.config: Optional[Dict[str, Any]] = self.load()
        
    def load(self) -> Dict[str, Any]:
        """Load and return the bot configuration from a JSON file."""
        if self.path is None:
            raise ValueError("Config path is not set.")
        user = Path(self.path).expanduser()
        config_path = user.resolve()
        if not config_path.is_file():
            raise RuntimeError(f"Configuration file '{config_path}' not found.")
        try:
            with config_path.open(encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON in '{config_path}': {e}")