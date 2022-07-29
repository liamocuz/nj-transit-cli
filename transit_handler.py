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
    """This class handles getting information from all data sources to construct routes and stop info"""

    def __init__(self):
        self.stops = StopHandler(DIRECTORY_PATH + "stops.txt")
        self.stop_times = StopTimeHandler(DIRECTORY_PATH + "stop_times.txt")
        self.trips = TripHandler(DIRECTORY_PATH + "trips.txt")
        self.routes = RouteHandler(DIRECTORY_PATH + "routes.txt")
        self.calendar = CalendarHandler(DIRECTORY_PATH + "calendar_dates.txt")

    def get_station_info(self, station_name: str, date: str):
        """Returns the arrival times for a station stop per headsign for given date"""
        stop_id: int = self.stops.get_stop_by_name(station_name).stop_id
        service_ids: set = self.calendar.get_service_ids(date)

        stop_times: dict = self.stop_times.get_trips(stop_id)
        valid_stop_times: list = self.filter_trips(stop_times, service_ids)

        trip_info = self.build_time_info(valid_stop_times)

        for key in trip_info:
            print(key)
            trip_info[key].sort(key=lambda x: x.arrival_time)
            for stop_time in trip_info[key]:
                print(stop_time.arrival_time)

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

    def get_route_info(self, route_name: str):
        pass
