import json
import functools
from dataclasses import dataclass, field
from pathlib import Path
from numpy import array, savetxt
from typing import Callable, List

from collaborate.member import Member


ComposableFunction = Callable[[float], float]

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

    def do(*functions: ComposableFunction) -> ComposableFunction:
        return functools.reduce(
            lambda f, g: lambda x: g(f(x)),
            functions
        )

    def load(self) -> dict:
        with open(self.file_path) as f:
            data = json.load(f)

        self.data = data
            
        return data

    def output_table(self, out_file: Path) -> None:
        unique = set(
            tuple(sorted([
                member["email"],
                member["matches"][-1]
            ]))
            for member in self.__data["members"]
            if member["matches"]
        )

        savetxt(
            out_file,
            array(list(unique)),
            fmt="%s",
            delimiter=",",
            header="Match-1,Match-2",
            comments=""
        )
        
    def save(
        self,
        new_matches: List[List[Member]],
        output_table: Path
    ) -> None:
        self.update_member_histories(new_matches)
        self.output_table(output_table)

        with open(self.file_path, "w") as f:
            json.dump(self.__data, f, indent=2)
        
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

    def clear_member_histories(self) -> None:
        for record in self.__data["members"]:
            record["matches"] = []
