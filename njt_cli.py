#!/usr/local/bin/python3

"""
This is the main file for the njt-cli project
"""

import sys
import os
import zipfile
import requests
from stop_handler import StopHandler
from trip_handler import TripHandler
from stop_time_handler import StopTimeHandler
from route_handler import RouteHandler


def get_rail_data(url: str, save_path: str, extract_path: str) -> bool:
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
        with open(save_path, 'wb') as file:
            file.write(response.content)

        # Extract zip file
        with zipfile.ZipFile(save_path, 'r') as rail_data:
            rail_data.extractall(extract_path)
    except (FileNotFoundError, PermissionError) as error:
        print(error)
        return False

    return True


# TODO
#   1. Create an args parser for different flags
#   2. Figure out how we want the cli to work, is it just going to be a single input or multiple
#   2.1 Multiple will need some sort of dfs to find best route between two
#   3. Fix the way downloading works

# Input should be like ./transit <from name> <to name>

if __name__ == "__main__":
    RAIL_DATA_URL = "https://content.njtransit.com/public/developers-resources/rail_data.zip"
    ZIP_PATH = "/tmp/njt/rail-data.zip"
    DIRECTORY_PATH = "/tmp/njt/rail-data/"

    # if not get_rail_data(RAIL_DATA_URL, ZIP_PATH, DIRECTORY_PATH):
    #     print("Unable to download rail data")
    #     sys.exit(1)

    stop_handler = StopHandler(DIRECTORY_PATH + "stops.txt")
    print(stop_handler.dataframe)
    print(stop_handler.get_stop_by_name("Manasquan"))

    trip_handler = TripHandler(DIRECTORY_PATH + "trips.txt")
    print(trip_handler.dataframe)

    stop_time_handler = StopTimeHandler(DIRECTORY_PATH + "stop_times.txt")
    print(stop_time_handler.dataframe)

    route_handler = RouteHandler(DIRECTORY_PATH + "routes.txt")
    print(route_handler.dataframe)

    sys.exit(0)
