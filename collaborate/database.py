from dataclasses import dataclass, field
from pathlib import Path
import json
from typing import List

from collaborate.member import Member


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
        
    def _buddy(
        self,
        pairs: List[List[Member]],
        email: str
    ) -> str:
        return ''.join([
            pair[1 - pair.index(member)].email
            for pair in pairs
            for member in pair
            if email in member.email
        ])

    def update_member_histories(
        self,
        new_matches: List[List[Member]]
    ) -> None:
        for record in self.__data["members"]:
            buddy = self._buddy(
                pairs=new_matches,
                email=record["email"]
            )

            if buddy:
                record["matches"].append(buddy)
            
        print(
            json.dumps(self.__data, indent=2)
        )
