import random
import string
from typing import List
from pandas import DataFrame

from .match import Matcher, MatchingStrategy
from .member import Division, Member


def generate_id(length: int = 16):
    return "".join(random.choices(string.ascii_uppercase, k=length))

class CollaborateService:
    """Monthly Collaborate service provider"""
    
    def __init__(self) -> None:
        self.members: dict[str, Member] = {}

    def register_members(self, members_data: DataFrame) -> str:
        for row in range(len(members_data)):
            name, email, division = members_data.loc[row, :].values.tolist()
            member_id = generate_id()
            self.members[member_id] = Member(
                member_id, name, email, Division[division]
            )

    # Amalgmate get methods into concise request method
    
    def get_member(
        self,
        member_id: str = None,
        email: str = None
    ) -> Member:
        if all(arg is None for arg in (member_id, email)):
            raise ValueError("Provide either a member's ID or email address.")
        
        if member_id is not None:
            return self.members[member_id]
        
        if email is not None:
            return [m for m in self.members.values() if m.email == email][0]
            
    def get_id(self, email: str) -> Member:
        return [m.member_id for m in self.members.values() if m.email == email][0]

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
