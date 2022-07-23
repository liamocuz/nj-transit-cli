from transitHandler import TransitHandler
from dataclasses import dataclass


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


class StopHandler(TransitHandler):
    def __init__(self, path: str):
        super().__init__(path)
        self.dictionary = self.buildDictionary()

    def buildDictionary(self) -> dict:
        """Builds a dictionary mapping stop_ids and stop_names to a Stop class"""
        dictionary = dict()
        STOP_ID_INDEX = 0
        STOP_NAME_INDEX = 2

        for row in self.dataframe.values:
            newStop = Stop(*row)
            dictionary[row[STOP_ID_INDEX]] = newStop
            dictionary[row[STOP_NAME_INDEX].lower()] = newStop

        return dictionary

    def getStopByName(self, stop_name: str) -> Stop:
        return self.dictionary[stop_name.lower()]

    def getStopById(self, stop_id: int) -> Stop:
        return self.dictionary[stop_id]
