from abc import ABC, abstractmethod
import pandas


class TransitHandler(ABC):
    """Parent class for importing information from NJ Transit text files"""
    def __init__(self, path: str):
        self.dataframe = self.getDataframe(path)

    @staticmethod
    def getDataframe(path: str):
        dataframe = None
        try:
            dataframe = pandas.read_csv(path, delimiter=',')
        except Exception as e:
            print(f"Unable to read {path}")
            print(e)
            raise IOError

        return dataframe

    @abstractmethod
    def buildDictionary(self):
        pass
