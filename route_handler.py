"""
This file creates the Route and RouteHandler classes
It is designed to import and handle the data from rail-data/routes.txt file
"""
from dataclasses import dataclass
from transit_handler import TransitHandler

# Index constants to map info to dataclass object
ROUTE_ID_INDEX = 0


@dataclass
class Route:
    """Class for representing each route"""
    # pylint: disable=too-many-instance-attributes
    route_id: int
    agency_id: str
    route_short_name: str
    route_long_name: str
    route_type: int
    route_url: str
    route_color: str


class RouteHandler(TransitHandler):
    """Loads info from the routes.txt file"""
    def __init__(self, path):
        super().__init__(path)
        self.dictionary = self.build_dictionary()

    def build_dictionary(self):
        """Builds a dictionary mapping route_id to a Route class"""
        dictionary = {}

        for row in self.dataframe.values:
            new_route = Route(*row)
            dictionary[row[ROUTE_ID_INDEX]] = new_route

        return dictionary
