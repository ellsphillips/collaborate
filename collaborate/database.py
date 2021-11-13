from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class Database:
    """Member database manager"""

    file_path: Path

    def load(self) -> json.JSONDecoder:
        with open(self.file_path) as f:
            data = json.load(f)
            
        print(type(data))
            
        return data
        
    def save():
        pass