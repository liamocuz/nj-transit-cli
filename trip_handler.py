"""
This file creates the Trip and TripHandler classes
It is designed to import and handle the data from rail-data/trips.txt file
"""
from dataclasses import dataclass
from data_handler import DataHandler


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
        """Builds a dictionary mapping trip_id to a Trip class"""
        dictionary = {}

        for row in self.dataframe.values:
            new_trip = Trip(*row)
            dictionary[new_trip.trip_id] = new_trip

        return dictionary

    def is_valid_trip(self, trip_id: int, service_ids: set[int]):
        trip = self.dictionary[trip_id]
        return trip.service_id in service_ids

    def get_headsign(self, trip_id: int) -> str:
        if trip_id in self.dictionary:
            return self.dictionary[trip_id].trip_headsign
        else:
            raise KeyError
