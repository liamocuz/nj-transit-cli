from transitHandler import TransitHandler
from dataclasses import dataclass


@dataclass
class StopTime:
    """Class for representing the stop times for each station"""
    trip_id: int
    arrival_time: str
    departure_time: str
    stop_id: int
    stop_sequence: int
    pickup_type: int
    drop_off_type: int
    shape_dist_traveled: float


class StopTimeHandler(TransitHandler):
    """Loads info from the stop_times.txt file"""
    def __init__(self, path: str):
        super().__init__(path)
        self.dictionary = self.buildDictionary()

    def buildDictionary(self) -> dict:
        """Builds a dictionary mapping trip_id and stop_id to a StopTime class"""
        dictionary = dict()
        TRIP_ID_INDEX = 0
        STOP_ID_INDEX = 3

        for row in self.dataframe.values:
            new_stop_time = StopTime(*row)
            dictionary[row[TRIP_ID_INDEX]] = new_stop_time
            dictionary[row[STOP_ID_INDEX]] = new_stop_time

        return dictionary
