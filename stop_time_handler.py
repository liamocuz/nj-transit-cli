"""
This file creates the StopTime and StopTimeHandler classes
It is designed to import and handle the data from rail-data/stops.txt file
"""
from dataclasses import dataclass
from data_handler import DataHandler


@dataclass
class StopTime:
    """Class for representing the stop times for each station"""
    # pylint: disable=too-many-instance-attributes
    trip_id: int
    arrival_time: str
    departure_time: str
    stop_id: int
    stop_sequence: int
    pickup_type: int
    drop_off_type: int
    shape_dist_traveled: float


class StopTimeHandler(DataHandler):
    """Loads info from the stop_times.txt file"""
    def __init__(self, path: str):
        super().__init__(path)
        self.dictionary = self.build_dictionary()

    def build_dictionary(self) -> dict:
        """ Builds a dictionary mapping stop_id to a dictionary of trip_ids to a StopTime object """
        dictionary = {}

        for row in self.dataframe.values:
            new_stop_time = StopTime(*row)
            if new_stop_time.stop_id not in dictionary:
                dictionary[new_stop_time.stop_id] = {}
            dictionary[new_stop_time.stop_id][new_stop_time.trip_id] = new_stop_time

        return dictionary

    def get_trips(self, stop_id: int):
        return self.dictionary[stop_id]
