"""
This file creates the Route and RouteHandler classes
It is designed to import and handle the data from rail-data/routes.txt file
"""
from dataclasses import dataclass
from data_handler import DataHandler


@dataclass
class Route:
    """Class for representing each route"""
    route_id: int
    agency_id: str
    route_short_name: str
    route_long_name: str
    route_type: int
    route_url: str
    route_color: str


class RouteHandler(DataHandler):
    """Loads info from the routes.txt file"""
    def __init__(self, path):
        super().__init__(path)
        self.dictionary = self.build_dictionary()

    def build_dictionary(self):
        """Builds a dictionary mapping route_id to a Route class"""
        dictionary = {}

        for row in self.dataframe.values:
            new_route = Route(*row)
            dictionary[new_route.route_id] = new_route

        return dictionary
