"""
This file creates methods to retrieve info from the Handler classes
Given a station and date, find out the next arrivals per headsign for the rest of the day
"""

from stop_handler import StopHandler
from trip_handler import TripHandler
from stop_time_handler import StopTimeHandler
from route_handler import RouteHandler
from calendar_handler import CalendarHandler

# Constants
DIRECTORY_PATH = "/tmp/njt/rail-data/"


class TransitHandler:
    """This class handles importing data sources to construct routes and stop info"""

    def __init__(self):
        self.stops = StopHandler(DIRECTORY_PATH + "stops.txt")
        self.stop_times = StopTimeHandler(DIRECTORY_PATH + "stop_times.txt")
        self.trips = TripHandler(DIRECTORY_PATH + "trips.txt")
        self.routes = RouteHandler(DIRECTORY_PATH + "routes.txt")
        self.calendar = CalendarHandler(DIRECTORY_PATH + "calendar_dates.txt")
        self.trie = self.build_trie()

    def get_station_info(self, name: str, date: str):
        """Prints the arrival times for a station stop per headsign for given date"""

        stop_name: str = self.get_name_from_trie(str(name))
        if type(stop_name) == list:
            print(f"Unable to find a unique stop name starting with \"{name}\". "
                  f"Perhaps you meant one of these?\n")
            for stop in stop_name:
                print(stop.upper())
            return

        if not stop_name or stop_name.lower() not in self.stops.dictionary:
            print(f"Unable to find stop name \"{name}\". "
                  f"Are you missing a space? "
                  f"Stop names with spaces in them must be surrounded in quotes.")
            return

        if date not in self.calendar.dictionary:
            print(f"Unable to find the date \"{date}\". "
                  f"It must be in a YYYYMMDD format.")
            return

        stop_id: int = self.stops.get_stop_by_name(stop_name).stop_id
        service_ids: set = self.calendar.get_service_ids(date)

        stop_times: dict = self.stop_times.get_trips(stop_id)
        valid_stop_times: list = self.filter_trips(stop_times, service_ids)

        trip_info = self.build_time_info(valid_stop_times)

        print(f"From {stop_name.upper()} on {date}\n")
        for headsign, station_info in trip_info.items():
            # Don't need to print times for the current station
            if headsign.lower() == stop_name.lower():
                continue
            print(f"To {headsign}")
            station_info.sort(key=lambda x: x.departure_time)
            for stop_time in station_info:
                print(stop_time.departure_time)
            print()

    def filter_trips(self, stop_times: dict, service_ids: set) -> list:
        """Filters the trips and returns a list of valid StopTime objects"""
        valid_stop_times = []
        for key in stop_times:
            if self.trips.is_valid_trip(key, service_ids):
                valid_stop_times.append(stop_times[key])

        return valid_stop_times

    def build_time_info(self, stop_times: list) -> dict:
        """Builds a dictionary mapping headsign to a list of stop_times"""
        trip_info = {}
        for stop_time in stop_times:
            headsign = self.trips.get_headsign(stop_time.trip_id)
            if headsign not in trip_info:
                trip_info[headsign] = []
            trip_info[headsign].append(stop_time)

        return trip_info

    def build_trie(self) -> dict:
        """Builds a trie of all station name, so that incomplete station names can still be found"""
        root = {}
        station_names = self.stops.get_stop_names()

        for name in station_names:
            level = root
            for char in name.lower():
                if char not in level:
                    level[char] = {}
                    level[char]['*'] = []
                level[char]['*'].append(name.lower())
                level = level[char]
        return root

    def get_name_from_trie(self, name: str):
        """
        Gets the station name from the trie
        The given name can be an unfinished name
        If it is unique enough it will return the full station name
        """
        level = self.trie

        for char in name.lower():
            if char not in level:
                return None
            level = level[char]

        if '*' not in level:
            return None
        if len(level['*']) == 1:
            return level['*'][0]

        return level['*']
