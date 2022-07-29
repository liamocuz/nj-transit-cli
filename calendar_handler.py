"""
This file creates the Calendar and CalendarHandler classes
It is designed to import and handle the data from rail-data/calendar_dates.txt file
"""
from dataclasses import dataclass
from data_handler import DataHandler
from datetime import datetime


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
            new_stop.date = str(new_stop.date)
            if new_stop.date not in dictionary:
                dictionary[new_stop.date] = {}
            dictionary[new_stop.date][new_stop.service_id] = new_stop

        return dictionary

    def get_service_ids(self, date: str) -> set:
        calendars = self.dictionary[date]
        service_ids = set(calendars.keys())
        return service_ids

    @staticmethod
    def get_today_date() -> str:
        return datetime.today().strftime("%Y%m%d")
