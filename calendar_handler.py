"""
This file creates the Calendar and CalendarHandler classes
It is designed to import and handle the data from rail-data/calendar_dates.txt file
"""
from dataclasses import dataclass
from data_handler import DataHandler

# Index constants to map info to dataclass object
SERVICE_ID_INDEX = 0
DATE_INDEX = 1


@dataclass
class Calendar:
    """Class for representing a calendar date"""
    service_id: int
    date: str
    exception_type: int


class CalendarHandler(DataHandler):
    """Loads info from the calendar_dates.txt file"""
    def __init__(self, path: str):
        super().__init__(path)
        self.dictionary = self.build_dictionary()

    def build_dictionary(self) -> dict:
        """Builds a dictionary mapping calendar date to a dictionary mapping service ids to a Calendar class"""
        dictionary = {}

        for row in self.dataframe.values:
            new_stop = Calendar(*row)
            if row[DATE_INDEX] not in dictionary:
                dictionary[row[DATE_INDEX]] = {}
            dictionary[row[DATE_INDEX]][row[SERVICE_ID_INDEX]] = new_stop

        return dictionary
