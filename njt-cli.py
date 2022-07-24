#!/usr/local/bin/python3
import sys
import os
import requests
import zipfile
from stopHandler import StopHandler
from tripHandler import TripHandler
from stopTimeHandler import StopTimeHandler
from routeHandler import RouteHandler


def getRailData(url: str, save_path: str, extract_path: str) -> bool:
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
    except Exception as e:
        print(e)
        return False

    return True


# TODO
# 1. Create an args parser for different flags
# 2. Figure out how we want the cli to work, is it just going to be a single input or multiple
# 2.1 Multiple will need some sort of dfs to find best route between two
# 3. Fix the way downloading works

# Input should be like ./transit <from name> <to name>

if __name__ == "__main__":
    rail_data_url = "https://content.njtransit.com/public/developers-resources/rail_data.zip"
    rail_data_zip_path = "/tmp/njt/rail-data.zip"
    rail_data_extract_path = "/tmp/njt/rail-data/"

    # if not getRailData(rail_data_url, rail_data_zip_path, rail_data_extract_path):
    #     print("Unable to download rail data")
    #     sys.exit(1)

    stop_handler = StopHandler(rail_data_extract_path + "stops.txt")
    print(stop_handler.dataframe)
    print(stop_handler.getStopByName("Manasquan"))

    trip_handler = TripHandler(rail_data_extract_path + "trips.txt")
    print(trip_handler.dataframe)

    stop_time_handler = StopTimeHandler(rail_data_extract_path + "stop_times.txt")
    print(stop_time_handler.dataframe)

    route_handler = RouteHandler(rail_data_extract_path + "routes.txt")
    print(route_handler.dataframe)

    sys.exit(0)
