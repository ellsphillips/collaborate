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

    print(
        *[
            " meets ".join([
                m.name.split()[1] + f" ({m.division.name})"
                for m in sorted(
                    service.match(
                        all_members,
                        XDMatchingStrategy()
                    )
                )
            ])
        ],
        "\n"
    )

    print(
        *[
            "\t->\t".join([
                first.division.name + "\t" + first.email,
                second.division.name + "\t" + second.email
            ]) for first, second in service.match(
                all_members,
                FFAMatchingStrategy()
            )
        ],
        "\n",
        sep="\n"
    )

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
