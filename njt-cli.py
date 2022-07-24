#!/usr/local/bin/python3
import sys
import os
import requests
import zipfile
from stopHandler import StopHandler
from tripHandler import TripHandler
from stopTimeHandler import StopTimeHandler


def getRailData(url: str, save_path: str = "./rail-data.zip", extract_path: str = "./rail-data") -> bool:
    """
    Downloads and writes rail data to the current directory if it does not already exist
    First downloads the .zip file from NJ Transit and then expands the file into a subdirectory
    """
    try:
        # Download and write data to zip file in current directory if file doesn't already exist
        if not os.path.isfile(save_path):
            # Download data
            response = requests.get(url, allow_redirects=True)

            # Write data from memory to zip file in current directory
            with open(save_path, 'wb') as file:
                file.write(response.content)

        # Extract zip file
        if not os.path.exists(extract_path):
            with zipfile.ZipFile(save_path, 'r') as rail_data:
                rail_data.extractall(extract_path)
    except Exception as e:
        print(e)
        return False

    return True


# TODO
# 1. Create an args parser for different flags
# 2. Figure out how we want the cli to work, is it just going to be a single input or multiple

# Input should be like ./transit <from name> <to name>

if __name__ == "__main__":
    rail_data_url = "https://content.njtransit.com/public/developers-resources/rail_data.zip"
    rail_data_zip_path = "./rail-data.zip"
    rail_data_extract_path = "./rail-data"

    if not getRailData(rail_data_url):
        print("Unable to download rail data")
        sys.exit(1)

    stop_handler = StopHandler("./rail-data/stops.txt")
    print(stop_handler.dataframe)
    print(stop_handler.getStopByName("Manasquan"))

    trip_handler = TripHandler("./rail-data/trips.txt")
    print(trip_handler.dataframe)

    stop_time_handler = StopTimeHandler("./rail-data/trips.txt")
    print(trip_handler.dataframe)
    sys.exit(0)
