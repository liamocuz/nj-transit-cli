from transitHandler import TransitHandler
from dataclasses import dataclass


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


class TripHandler(TransitHandler):
    """Class for loading in data from ./rail-data/trips.txt"""
    def __init__(self, path: str):
        super().__init__(path)
        self.dictionary = self.buildDictionary()

    def buildDictionary(self) -> dict:
        """Builds a dictionary mapping route_id and trip_id to a Trip class"""
        dictionary = dict()
        ROUTE_ID_INDEX = 0
        TRIP_ID_INDEX = 2

        for row in self.dataframe.values:
            new_trip = Trip(*row)
            dictionary[row[ROUTE_ID_INDEX]] = new_trip
            dictionary[row[TRIP_ID_INDEX]] = new_trip

        return dictionary
