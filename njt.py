#!/usr/local/opt/python@3.10/bin/python3

"""
This is the main file for the njt-cli project
"""

import sys
import os
import zipfile
import argparse
import requests
from transit_handler import TransitHandler
from dates_and_times import get_today_date, get_tomorrow_date


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


# For single station ./njt <station name> <date> -> prints arrival times per headsign

if __name__ == "__main__":
    RAIL_DATA_URL = "https://content.njtransit.com/public/developers-resources/rail_data.zip"
    ZIP_PATH = "/tmp/njt/rail-data.zip"
    DIRECTORY_PATH = "/tmp/njt/rail-data/"

    # Create the argument parser and add arguments
    parser = argparse.ArgumentParser(description="print out departure times for a rail stop")
    parser.add_argument("stop_name",
                        metavar="stop_name",
                        type=str,
                        help="name of the rail stop. surround the name in quotes if it has spaces")
    parser.add_argument("-d",
                        "--date",
                        default=get_today_date(),
                        nargs='?',
                        help="the date of the departure times in a YYYYMMDD format")
    parser.add_argument("-r",
                        "--refresh",
                        action="store_true",
                        help="force a download the NJ Transit Rail Data")
    parser.add_argument("-t",
                        "--tomorrow",
                        action="store_true",
                        help="gets times for tomorrow. this will override any date specified by -d")
    parser.add_argument("-l",
                        "--list",
                        nargs='?',
                        type=int,
                        default=float("inf"),
                        help="number of times to list per headsign")
    args = parser.parse_args()

    # Handle downloading and unzipping the rail data
    if not os.path.exists(DIRECTORY_PATH) or args.refresh:
        print("Downloading NJ Transit Rail Data")
        if not get_rail_data(RAIL_DATA_URL, ZIP_PATH, DIRECTORY_PATH):
            print("Unable to download rail data")
            sys.exit(1)

    # Create the transit handler, which is the main handler for retrieving data
    transit = TransitHandler()
    transit.get_station_info(
        name=str(args.stop_name),
        date=get_tomorrow_date() if args.tomorrow else str(args.date),
        list_length=args.list
    )

    sys.exit(0)
