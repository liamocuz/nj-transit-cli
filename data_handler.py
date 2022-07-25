"""
This module creates a class designed from importing information from a given txt file
"""
from abc import ABC, abstractmethod
import pandas


class DataHandler(ABC):
    """Parent class for importing information from NJ Transit text files"""
    def __init__(self, path: str):
        self.dataframe = self.get_dataframe(path)

    @staticmethod
    def get_dataframe(path: str):
        """Uses pandas to read the csv formatted .txt file passed in by the path variable"""
        dataframe = None
        try:
            dataframe = pandas.read_csv(path, delimiter=',')
        except Exception as error:
            print(f"Unable to read {path}")
            raise error

        return dataframe

    @abstractmethod
    def build_dictionary(self):
        """Populates a dictionary, mapping key(s) from the dataframe to the info dataclass"""
