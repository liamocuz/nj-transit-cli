"""
This file creates the Trip and TripHandler classes
It is designed to import and handle the data from rail-data/trips.txt file
"""
from dataclasses import dataclass
from data_handler import DataHandler

# Index constants to map info to dataclass object
ROUTE_ID_INDEX = 0
TRIP_ID_INDEX = 2


@dataclass
class Trip:
    """Class for representing a rail trip"""
    route_id: int
    service_id: int
    trip_id: int
    trip_headsign: str
    direction_id: int
    block_id: str
    shape_id: int


class TripHandler(DataHandler):
    """Loads info from the trips.txt file"""
    def __init__(self, path: str):
        super().__init__(path)
        self.dictionary = self.build_dictionary()

    def build_dictionary(self) -> dict:
        """Builds a dictionary mapping route_id and trip_id to a Trip class"""
        dictionary = {}

        for row in self.dataframe.values:
            new_trip = Trip(*row)
            dictionary[row[ROUTE_ID_INDEX]] = new_trip
            dictionary[row[TRIP_ID_INDEX]] = new_trip

        return dictionary
