import random
from abc import ABC, abstractmethod
from typing import List

from .member import Member


class MatchingStrategy(ABC):
    
    @abstractmethod
    def create_matches(self, members: List[Member]) -> List[Member]:
        """Returns an ordered list of member pairs."""

class FFAMatchingStrategy(MatchingStrategy):
    """Free-for-all matching"""
    
    def create_matches(self, members: List[Member]) -> List[Member]:
        return [pair for pair in self.reduce_pairs(members)]

    def reduce_pairs(self, members: List[Member]):
        while len(members) > 0:
            pair = random.sample(members, 2)
            yield pair
            members = [e for e in members if e not in pair]

class XDMatchingStrategy(MatchingStrategy):
    """Cross-divisional matching"""
    
    def create_matches(self, members: List[Member]) -> List[Member]:
        pass

class BlackHoleMatchingStrategy(MatchingStrategy):
    """Cross-divisional matching"""
    
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
            if self.members.count(m) > 1]
        )

        print(
            "\n".join([
                f"Removed {len(duplicates)} duplicates from " \
                    f"list of {len(self.members)} members:",
                *sorted([str(dup) for dup in duplicates])
            ])
        )

        return sorted(list(set(self.members)))

    def match_members(self, matching_strategy: MatchingStrategy) -> None:
        return  matching_strategy.create_matches(self.members)
