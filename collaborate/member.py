from dataclasses import dataclass, field
from enum import Enum, auto

from .utils import Colour


class Division(Enum):
    BST = auto()
    AME = auto()
    DSC = auto()
    PS = auto()
    EP = auto()


@dataclass(order=True, frozen=True, eq=True)
class Member:
    member_id: str = field(
        repr=True,
        compare=False,
        hash=False
    )
    name: str
    email: str
    division: Division

    def __str__(self) -> str:
        return (
            f"{Colour.PURPLE}{self.member_id}"
            f"{Colour.CYAN} Member: "
            f"{Colour.END}{self.division} \t"
            f"{Colour.YELLOW}{self.name} "
            f"{Colour.END}({self.email})"
        )
