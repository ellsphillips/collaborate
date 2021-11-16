import os
import pathlib
from pandas import read_csv

from collaborate.database import Database
from collaborate.service import CollaborateService
from collaborate.match import (
    BlackHoleMatchingStrategy,
    FFAMatchingStrategy,
    XDMatchingStrategy
)

# Config
AUTHOR = "elliott.phillips@ons.gov.uk"
DATA_DIR = pathlib.Path("data/")
MEMBERS_DATA = DATA_DIR / "members.json"
NEW_MATCHES = DATA_DIR / "new_matches.csv"


def main():
    # Create a service provider
    service = CollaborateService()

    # Load datasets
    db = Database(MEMBERS_DATA)
    
    members_data = db.load()

    # Register members
    service.register_members(members_data)
    all_members = service.get_all_members()
    
    # Create matches
    matches = service.match(
        members=all_members,
        author=AUTHOR,
        strategy=XDMatchingStrategy()
    )

    db.clear_member_histories()

    db.update_member_histories(matches)

    db.save()

    db.output_table(NEW_MATCHES)
    

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    main()
