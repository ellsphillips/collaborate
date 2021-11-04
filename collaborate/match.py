from .member import Member

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
