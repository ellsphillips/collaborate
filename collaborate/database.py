from dataclasses import dataclass, field
from pathlib import Path
import json


@dataclass
class Database:
    """Member database manager"""

    file_path: Path
    __data: dict = field(default_factory=dict)

    @property
    def data(self) -> str:
        return self.__data

    @data.setter
    def data(self, db_obj: dict) -> None:
        self.__data = db_obj

    def load(self) -> dict:
        with open(self.file_path) as f:
            data = json.load(f)

        self.data = data
            
        return data
        
    def save(self, data: dict):
        with open("data/test.json", "w") as write_file:
            json.dump(data, write_file, indent=2)
