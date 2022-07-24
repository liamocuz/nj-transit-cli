from transitHandler import TransitHandler
from dataclasses import dataclass


@dataclass
class Route:
    route_id: int
    agency_id: str
    route_short_name: str
    route_long_name: str
    route_type: int
    route_url: str
    route_color: str


class RouteHandler(TransitHandler):
    """"""
    def __init__(self, path):
        super().__init__(path)
        self.dictionary = self.buildDictionary()

    def buildDictionary(self):
        dictionary = dict()
        ROUTE_ID_INDEX = 0

        for row in self.dataframe.values:
            new_route = Route(*row)
            dictionary[row[ROUTE_ID_INDEX]] = new_route

        return dictionary

