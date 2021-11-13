from json import load
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
MEMBERS_DATASET = DATA_DIR / "members.csv"
PREVIOUS_MATCHES = DATA_DIR / "previous_matches.csv"


def main():
    # Create a service provider
    service = CollaborateService()

    # Load datasets
    db = Database(MEMBERS_DATA)
    
    memories = db.load()
    
    members_data = read_csv(MEMBERS_DATASET)
    previous_matches = read_csv(PREVIOUS_MATCHES)

    # Register members
    # TODO: Change service.register_members() to accept
    #       the members data read in from JSON.
    #       
    #   01. For each member, insert and assign name, email
    #       and division into Member object. 
    #   02. Only generate ID if new to the system.
    service.register_members(members_data)

    all_members = service.get_all_members()
    
    print(service.get_id(AUTHOR))
        
    print(service.get_member(email=AUTHOR))

    # print(
    #     *[
    #         " meets ".join([
    #             m.name.split()[1] + f" ({m.division.name})"
    #             for m in sorted(
    #                 service.match(
    #                     all_members,
    #                     XDMatchingStrategy()
    #                 )
    #             )
    #         ])
    #     ],
    #     "\n"
    # )

    # print(
    #     *[
    #         "\t->\t".join([
    #             first.division.name + "\t" + first.email,
    #             second.division.name + "\t" + second.email
    #         ]) for first, second in service.match(
    #             all_members,
    #             FFAMatchingStrategy()
    #         )
    #     ],
    #     "\n",
    #     sep="\n"
    # )
    

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    main()
