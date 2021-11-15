import random
from abc import ABC, abstractmethod
from typing import List

from .member import Member
from .utils import Colour


class MatchingStrategy(ABC):
    
    @abstractmethod
    def create_matches(self, members: List[Member]) -> List[Member]:
        """Returns an ordered list of member pairs."""

class FFAMatchingStrategy(MatchingStrategy):
    """Free-for-all matching"""
    
    def create_matches(self, members: List[Member]) -> List[Member]:
        return [pair for pair in self.reduce_pairs(members)]

    def reduce_pairs(self, members: List[Member]) -> None:
        while not len(members) < 2:
            pair = random.sample(members, 2)
            yield pair
            members = [e for e in members if e not in pair]

class XDMatchingStrategy(MatchingStrategy):
    """Cross-divisional matching"""
    
    def create_matches(
        self,
        members: List[Member],
        threshold: int = 3
    ) -> List[Member]:
        return [pair for pair in self.reduce_pairs(members, threshold)]
    
    # TODO: Build XDMatch pair reducer
    def reduce_pairs(
        self,
        members: List[Member],
        threshold: int
    ) -> None:
        while not len(members) < 2:
            first = random.choice(members)
            members.remove(first)

            punt = None
            for _ in range(threshold):
                punt = random.choice(members)
                if first.division.name != punt.division.name:
                    members.remove(punt)
                    break

            second = punt if punt is not None else random.sample(members, 1)[0]

            yield [first, second]
        
class BlackHoleMatchingStrategy(MatchingStrategy):
    """Chuck it in the bin"""
    
    def create_matches(self, members: List[Member]) -> List[Member]:
        print("Not running Collaborate this month!")
        return []

class Matcher:
    """Matching behaviour and preparation controller"""

    def __init__(self, members: List[Member]) -> None:
        self.members = members

    def remove_duplicates(self) -> None:
        if len(self.members) == len(set(self.members)):
            return self.members
        
        duplicates = set([
            m for m in self.members
            if self.members.count(m) > 1
        ])

        print(
            f"Removed {len(duplicates)} duplicates from " \
                f"list of {len(self.members)} members:",
            *sorted([str(dup) for dup in duplicates]),
            "\n",
            sep="\n"
        )

        self.members = sorted(set(self.members))

    def ensure_even(self, author: Member) -> None:
        if len(self.members) % 2 != 0:
            self.members.remove(author)

    def match_members(self, matching_strategy: MatchingStrategy) -> None:
        matches = matching_strategy.create_matches(self.members)
        
        print(
            "Matching members with"
            f"{Colour.CYAN}{matching_strategy.__class__.__name__}{Colour.END}",
            "-"*50,
            *[
                "\t->\t".join([
                    first.division.name + "\t" + first.email,
                    second.division.name + "\t" + second.email
                ]) for first, second in matches
            ],
            "\n",
            sep="\n"
        )
        
        return matches
    
    def print(self) -> None:
        print(*[m.name for m in self.members], sep="\n")
