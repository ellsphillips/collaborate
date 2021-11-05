import random
import string
from typing import List
from pandas import DataFrame

from .match import Matcher, MatchingStrategy
from .member import Division, Member


def generate_id(length: int = 16):
    return "".join(random.choices(string.ascii_uppercase, k=length))

class CollaborateService:
    """
    """
    def __init__(self) -> None:
        self.members: dict[str, Member] = {}

    def register_members(self, members_data: DataFrame) -> str:
        for row in range(len(members_data)):
            name, email, division = members_data.loc[row, :].values.tolist()
            member_id = generate_id()
            self.members[member_id] = Member(
                member_id, name, email, Division[division]
            )

    def get_member(self, member_id: str) -> Member:
        return self.members[member_id]

    def get_all_members(self) -> List[Member]:
        return list(self.members.values())

    def match(
        self,
        members: List[Member],
        strategy: MatchingStrategy
    ) -> list:
        matcher = Matcher(members)

        matcher.remove_duplicates()

        return matcher.match_members(strategy)
