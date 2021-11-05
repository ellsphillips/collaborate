import pathlib
import pandas as pd
import os

from collaborate.match import FFAMatchingStrategy
from collaborate.service import CollaborateService


# Config
AUTHOR = "elliott.phillips@ons.gov.uk"
DATA_DIR = pathlib.Path("data/")
MEMBERS_DATA = DATA_DIR / "members.csv"
PREVIOUS_MATCHES = DATA_DIR / "previous_matches.csv"


def main():
    # create a IOT service
    service = CollaborateService()

    # Load datasets
    members_data = pd.read_csv(MEMBERS_DATA)
    previous_matches = pd.read_csv(PREVIOUS_MATCHES)

    # Register members
    service.register_members(members_data)

    all_members = service.get_all_members()

    print(*all_members, sep='\n')

    print(
        *service.match(
            all_members,
            FFAMatchingStrategy()
        ),
        sep="\n"
    )


if __name__ =="__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    main()