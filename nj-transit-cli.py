#!/usr/local/bin/python3
import sys
import os
import requests
import zipfile


def getRailData(url: str, save_path: str = "./rail-data.zip", extract_path: str = "./rail-data") -> bool:
    try:
        # Download and write data to zip file in current directory if file doesn't already exist
        if not os.path.isfile(save_path):
            # Download data
            response = requests.get(url, allow_redirects=True)

            # Write data from memory to zip file in current directory
            with open(save_path, 'wb') as file:
                file.write(response.content)

        # Extract zip file
        with zipfile.ZipFile(save_path, 'r') as rail_data:
            rail_data.extractall(extract_path)
    except Exception as e:
        print(e)
        return False

    return True


if __name__ == "__main__":
    railDataUrl = "https://content.njtransit.com/public/developers-resources/rail_data.zip"

    if not getRailData(railDataUrl):
        print("Unable to download rail data")
        sys.exit(1)

    sys.exit(0)
