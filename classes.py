import test
import datetime


class City:
    """" Main Superclass of all the cities"""
    name: str
    year: list[tuple[datetime.datetime, datetime.datetime]]
    intraprovincial: list[int]
    interprovincial: list[int]
    house_land_avg: list[float]
    house_avg: list[float]
    land_avg: list[float]

    def __init__(self, name: str, year: list[tuple[datetime.datetime, datetime.datetime]], intraprovincial: list[int],
             interprovincial: list[int], house_land_avg: list[float], house_avg: list[float],
             land_avg: list[float]) -> None:
        self.name = name
        self.year = year
        self.intraprovincial = intraprovincial
        self.interprovincial = interprovincial
        self.house_land_avg = house_land_avg
        self.house_avg = house_avg
        self.land_avg = land_avg

    def get_values_xy(self, par: list) -> dict:
        """Return a dictionary with the key as the name of the city, and the value is a list of tuples that store the x and y coorindates.

        Ensure that the order of year corresponds to the other of the intraprovincial values; and that their lengths are the same."""
        d = {}
        lst = []
        for x in range(len(self.year)):
            temp = (self.year[x], par[x])
            lst.append(temp)
            d[self.name] = lst
        return d
