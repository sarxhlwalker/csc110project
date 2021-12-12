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
    intraprovincial: list[int]  # sarah
    interprovincial: list[int]  # sarah
    house_land_avg: list[float]  # manya and sima
    house_avg: list[float]  # sima
    land_avg: list[float]  # sima

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


def moncton_and_fredericton(city_list: list[City]) -> list[City]:
    """
    Combine the Moncton and Fredericton City instances because we have data overlap in Manya and
    Sima's data.
    """
    new_list = []
    moncton = city_list[0]  # because pycharm hates me
    fredricton = city_list[1]  # because pycharm hates me pt 2
    for city in city_list:
        if city.name != 'Greater Moncton' and city.name != 'Fredricton':
            new_list.append(city)
        elif city.name == 'Greater Moncton':
            moncton = city
        elif city.name == 'Fredricton':
            fredricton = city

    name = 'Greater Moncton and Fredricton'
    year = moncton.year
    inter = []
    intra = []
    comp = []
    house = []
    land = []
    for i in range(5):
        inter.append(moncton.interprovincial[i] + fredricton.interprovincial[i])
        intra.append(moncton.intraprovincial[i] + fredricton.intraprovincial[i])
        comp.append(moncton.house_land_avg[i] + fredricton.house_land_avg[i])
        house.append(moncton.house_avg[i] + fredricton.house_avg[i])
        land.append(moncton.land_avg[i] + fredricton.land_avg[i])
    new_list.append(City(name, year, inter, intra, comp, house, land))
    return new_list


if __name__ == '__main__':
    pass
