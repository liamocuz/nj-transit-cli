"""
This file creates methods to retrieve info from the Handler classes
Given a station and date, find out the next arrivals per headsign for the rest of the day
"""

from stop_handler import StopHandler
from trip_handler import TripHandler
from stop_time_handler import StopTimeHandler
from route_handler import RouteHandler
from calendar_handler import CalendarHandler
from dates_and_times import get_datetime, get_pretty_date, \
    get_pretty_time, get_iso_time, get_njt_date, get_today_date, \
    get_iso_date

# Constants
DIRECTORY_PATH = "/tmp/njt/rail-data/"


class TransitHandler:
    """This class handles importing data sources to construct routes and stop info"""

    def __init__(self, date: str, time: str):
        self.stops = StopHandler(DIRECTORY_PATH + "stops.txt")
        self.stop_times = StopTimeHandler(DIRECTORY_PATH + "stop_times.txt")
        self.trips = TripHandler(DIRECTORY_PATH + "trips.txt")
        self.routes = RouteHandler(DIRECTORY_PATH + "routes.txt")
        self.calendar = CalendarHandler(DIRECTORY_PATH + "calendar_dates.txt")
        self.trie = self.build_trie()
        self.datetime = get_datetime(date, time)

    def get_station_info(self, name: str, list_length: int):
        """Prints the departure times for a station stop per headsign for given date"""

        # Attempt to get the stop_name from the trie
        stop_name: str = self.get_name_from_trie(name)
        if isinstance(stop_name, list):
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

        # Get the proper YYYYMMDD date that can be hashed
        njt_date: str = get_njt_date(self.datetime)
        if njt_date not in self.calendar.dictionary:
            print(f"Unable to find the date \"{get_iso_date(self.datetime)}\". "
                  f"The date should be on or after {get_today_date()}")
            return

        # Get the stop_id from the name
        stop_id: int = self.stops.get_stop_by_name(stop_name).stop_id
        # Get the service_ids from the date
        service_ids: set = self.calendar.get_service_ids(njt_date)

        # Get the trips given the name and service_ids
        trips: dict = self.stop_times.get_trips(stop_id)
        valid_stop_times: list = self.filter_trips(trips, service_ids)

        # Get the stop_times
        stop_time_info: dict = self.build_time_info(valid_stop_times)

        self.print_stop_info(stop_name, stop_time_info, list_length)
        return

    def print_stop_info(self, stop_name: str, stop_time_info: dict, list_length: int):
        """Prints out rail stop information"""

        check_time = get_iso_time(self.datetime)
        print(f"From {stop_name.upper()} on {get_pretty_date(self.datetime)}\n")
        for headsign, station_info in stop_time_info.items():
            # Don't need to print times for the current station
            if headsign.lower() == stop_name.lower():
                continue
            print(f"To {headsign}")

            # Sort and filter the objects
            station_info.sort(key=lambda x: x.departure_time)  # sort departure times in order
            station_info = [stop_time for stop_time in station_info
                            if stop_time.departure_time > check_time]

            # Print out the objects
            for idx in range(min(list_length, len(station_info))):
                stop_time = station_info[idx]
                print(f"{get_pretty_time(stop_time.departure_time)}")
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
        If it is unique enough it will return the full station name string
        If multiple stations are matched, a list of those stations will be returned
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
