import pathlib
import pandas as pd
import random


# Config
AUTHOR = "elliott.phillips@ons.gov.uk"
DATA_DIR = pathlib.Path("data/")
SIGNUP_DATA = DATA_DIR / "signups.csv"
PREVIOUS_MATCHES = DATA_DIR / "previous_matches.csv"


def main():
    # Load datasets
    collaborate_data = pd.read_csv(SIGNUP_DATA)
    previous_matches = pd.read_csv(PREVIOUS_MATCHES)

    print(collaborate_data.head())
    print(previous_matches.head())


if __name__ =="__main__":
    main()