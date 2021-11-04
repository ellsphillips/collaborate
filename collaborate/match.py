from abc import ABC, abstractmethod

from .member import Member

class MatchingStrategy(ABC):
    @abstractmethod
    def create_matches(self, members: list[Member]) -> list[Member]:
        """Returns an ordered list of member pairs."""

class FFAMatchingStrategy(MatchingStrategy):
    """Free-for-all matching"""
    def create_matches(self, members: list[Member]) -> list[Member]:
        return members

class XDMatchingStrategy(MatchingStrategy):
    """Cross-divisional matching"""
    def create_matches(self, members: list[Member]) -> list[Member]:
        return members

class Matcher:
    """
    """
    def __init__(self, members: list[Member]) -> None:
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
        matches = matching_strategy.create_matches(self.members)

