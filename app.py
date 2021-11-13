import os
import pathlib
from pandas import read_csv

from collaborate.service import CollaborateService
from collaborate.match import (
    BlackHoleMatchingStrategy,
    FFAMatchingStrategy,
    XDMatchingStrategy
)

# Config
AUTHOR = "elliott.phillips@ons.gov.uk"
DATA_DIR = pathlib.Path("data/")
MEMBERS_DATA = DATA_DIR / "members.csv"
PREVIOUS_MATCHES = DATA_DIR / "previous_matches.csv"


def main():
    # Create a service provider
    service = CollaborateService()

    # Load datasets
    members_data = read_csv(MEMBERS_DATA)
    previous_matches = read_csv(PREVIOUS_MATCHES)

    # Register members
    service.register_members(members_data)

    all_members = service.get_all_members()
    
    print(service.get_id(AUTHOR))
        
    print(service.get_member(email=AUTHOR))

    #

    import json

    members_dict = {}

    members_dict["members"] = [
        {
            "name": member.name,
            "email": member.email,
            "division": member.division.name,
        }
        for member in all_members
    ]
    

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    main()
