"""
This file creates the Stop and StopHandler classes
It is designed to import and handle the data from rail-data/stops.txt file
"""
from dataclasses import dataclass
from data_handler import DataHandler


@dataclass
class Stop:
    """Class for representing a rail stop"""
    stop_id: int
    stop_code: str
    stop_name: str
    stop_desc: str
    stop_lat: str
    stop_lon: str
    zone_id: str


class StopHandler(DataHandler):
    """Loads info from the stops.txt file"""
    def __init__(self, path: str):
        super().__init__(path)
        self.dictionary = self.build_dictionary()

    def build_dictionary(self) -> dict:
        """Builds a dictionary mapping stop_ids and stop_names to a Stop class"""
        dictionary = {}

        for row in self.dataframe.values:
            new_stop = Stop(*row)
            dictionary[new_stop.stop_id] = new_stop
            dictionary[new_stop.stop_name.lower()] = new_stop

        return dictionary

    def get_stop_by_name(self, stop_name: str) -> Stop:
        """Returns the Stop object given its string name"""
        return self.dictionary[stop_name.lower()]

    def get_stop_by_id(self, stop_id: int) -> Stop:
        """Returns the Stop object given its stop id"""
        return self.dictionary[stop_id]

