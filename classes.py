import main
import manya_dataset
import sarah_dataset
import sima_dataset
import datetime

class City:
    """"
    A class to contain all the necessary information for one city.
    """
    name: str
    year: list[int]
    intraprovincial: list[int]      # sarah
    interprovincial: list[int]      # sarah
    house_land_avg: list[float]     # manya and sima
    house_avg: list[float]          # sima
    land_avg: list[float]           # sima

    def __init__(self, name: str, year: list[int],
                 intraprovincial: list[int], interprovincial: list[int],
                 house_land_avg: list[float], house_avg: list[float],
                 land_avg: list[float]) -> None:
        self.name = name
        self.year = year
        self.intraprovincial = intraprovincial
        self.interprovincial = interprovincial
        self.house_land_avg = house_land_avg
        self.house_avg = house_avg
        self.land_avg = land_avg


if __name__ == '__main__':
    pass
