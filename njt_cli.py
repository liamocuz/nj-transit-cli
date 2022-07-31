#!/usr/local/bin/python3

"""
This is the main file for the njt-cli project
"""

import sys
import os
import zipfile
import argparse
from datetime import datetime
import requests
from transit_handler import TransitHandler


def get_rail_data(url: str, zip_path: str, extract_path: str) -> bool:
    """
    Downloads and writes rail data to the current directory if it does not already exist
    First downloads the .zip file from NJ Transit and then expands the file into a subdirectory
    """
    try:
        # First make the directory to store files in if it doesn't exist
        if not os.path.exists("/tmp/njt/"):
            os.makedirs("/tmp/njt/")

        # Download and write data to zip file in current directory if file doesn't already exist
        # Download data
        response = requests.get(url, allow_redirects=True)

        # Write data from memory to zip file in /tmp/njt/
        with open(zip_path, 'wb') as file:
            file.write(response.content)

        # Extract zip file
        with zipfile.ZipFile(zip_path, 'r') as rail_data:
            rail_data.extractall(extract_path)
    except (FileNotFoundError, PermissionError) as error:
        print(error)
        return False

    return True


def get_today_date() -> str:
    """Returns today's date in the form YYYYMMDD"""
    return datetime.today().strftime("%Y%m%d")

# TODO # pylint: disable=fixme
#   1. Create an args parser for different flags
#   2. Figure out how we want the cli to work, is it just going to be a single input or multiple
#   2.1 Multiple will need some sort of dfs to find best route between two
#   3. Fix the way downloading works
#   4. Filter times based upon current time of day
#   5. Implement a trie when incomplete stops are put in

# Input should be like ./transit <from name> <to name> <date> -> prints list of time
# For single station ./njt <station name> <date> -> prints arrival times per headsign


if __name__ == "__main__":
    RAIL_DATA_URL = "https://content.njtransit.com/public/developers-resources/rail_data.zip"
    ZIP_PATH = "/tmp/njt/rail-data.zip"
    DIRECTORY_PATH = "/tmp/njt/rail-data/"

    parser = argparse.ArgumentParser(description="print out departure times for a rail stop")
    parser.add_argument("stop_name",
                        metavar="stop_name",
                        help="rail stop name. If the name has spaces, surround the name in quotes")
    parser.add_argument("-d",
                        "--date",
                        default=get_today_date(),
                        nargs='?',
                        help="the date of the departure times in a YYYYMMDD format")
    parser.add_argument("-r",
                        "--refresh",
                        action="store_true",
                        help="force a download the NJ Transit Rail Data")
    args = parser.parse_args()

    if not os.path.exists(DIRECTORY_PATH) or args.refresh:
        print("Downloading NJ Transit Rail Data")
        if not get_rail_data(RAIL_DATA_URL, ZIP_PATH, DIRECTORY_PATH):
            print("Unable to download rail data")
            sys.exit(1)

    transit = TransitHandler()
    transit.get_station_info(args.stop_name, args.date)

    sys.exit(0)
