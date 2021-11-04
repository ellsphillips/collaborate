from .member import Member

class Matcher:
    """
    """

    def __init__(self) -> None:
        pass

    def remove_duplicates(self, member_list: list[Member]) -> None:
        if len(member_list) == len(set(member_list)):
            return member_list
        
        duplicates = set([m for m in member_list if member_list.count(m) > 1])
        print(
            "\n".join([
                f"Removed {len(duplicates)} duplicates from " \
                    f"list of {len(member_list)} members:",
                *sorted([str(dup) for dup in duplicates])
            ])
        )