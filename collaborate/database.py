from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class Database:
    """Member database manager"""

    file_path: Path

    def load(self) -> dict:
        with open(self.file_path) as f:
            data = json.load(f)
            
        return data
        
    def save(self, data: dict):
        with open("data/test.json", "w") as write_file:
            json.dump(data, write_file, indent=2)
