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

    def register_from_csv(self, members_data: DataFrame) -> None:
        for row in range(len(members_data)):
            name, email, division = members_data.loc[row, :].values.tolist()
            member_id = generate_id()
            self.members[member_id] = Member(
                member_id, name, email, Division[division]
            )
            
    def register_members(self, members_data: dict) -> None:
        for member in members_data["members"]:
            member_id = member["id"] if "id" in member else generate_id()
            
            self.members[member_id] = Member(
                member_id,
                member["name"],
                member["email"],
                Division[member["division"]]
            )
    
    def get_member(
        self,
        member_id: str = None,
        email: str = None
    ) -> Member:
        if member_id is not None:
            return self.members[member_id]
        
        if email is not None:
            return [m for m in self.members.values() if m.email == email][0]
        
        raise ValueError("Provide either a member's ID or email address.")
            
    def get_id(self, email: str) -> Member:
        return [m.member_id for m in self.members.values() if m.email == email][0]

    def get_all_members(self) -> List[Member]:
        return list(self.members.values())

    def match(
        self,
        members: List[Member],
        author: str,
        strategy: MatchingStrategy
    ) -> list:
        matcher = Matcher(members)

        matcher.ensure_even(
            self.get_member(email=author)
        )

        matcher.remove_duplicates()

        return matcher.match_members(strategy)
