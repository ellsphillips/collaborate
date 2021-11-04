import random
import string
from pandas import DataFrame

from .member import Member


def generate_id(length: int = 32):
    return "".join(random.choices(string.ascii_uppercase, k=length))

class CollaborateService:
    """
    """
    def __init__(self) -> None:
        self.member: dict[str, Member] = {}

    def create_matches() -> None:
        pass