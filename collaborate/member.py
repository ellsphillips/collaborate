from abc import ABC, abstractmethod


class Member(ABC):
    @abstractmethod
    def previous_matches(self) -> None:
        pass

    @abstractmethod
    def profile(self) -> None:
        pass