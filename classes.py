"""
CSC110: Final Project

This file contains the main City class and Province class.
It also contains a function that combines some overlapping data in our datasets.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of professors and TAs
at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021 Sarah Walker, Manya Mittal, Sima Shmuylovich, and Grace Fung.
"""


class City:
    """"
    A class to contain all the necessary information for one city.

    Instance Attributes:
     - name: the name of the city
     - year: the years that we are considering (2015, 2016, 2017, 2018, 2019)
     - intraprovincial: the number of people travelling within the city
     - interprovincial: the number of people in and out of the city
     - house_land_avg: the average HPI value of house and land combined
     - house_avg: the HPI value of only houses
     - land_avg: the HPI value of only the land
     - province: the province that the city is in

    Representation Invariants:
        - self.name != ''
        - all(x in {2015, 2016, 2017, 2018, 2019} for x in self.year)
        - len(self.intraprovincial) == len(self.interprovincial) == len(house_land_avg)
        - len(house_land_avg) == len(house_avg) == len(land_avg) == 5
        - self.province != ''
    """
    name: str
    year: list[int]
    intraprovincial: list[int]  # sarah
    interprovincial: list[int]  # sarah
    house_land_avg: list[float]  # manya and sima
    house_avg: list[float]  # sima
    land_avg: list[float]  # sima
    province: str

    def __init__(self, name: str, year: list[int],
                 intraprovincial: list[int], interprovincial: list[int],
                 house_land_avg: list[float], house_avg: list[float],
                 land_avg: list[float], province: str) -> None:
        self.name = name
        self.year = year
        self.intraprovincial = intraprovincial
        self.interprovincial = interprovincial
        self.house_land_avg = house_land_avg
        self.house_avg = house_avg
        self.land_avg = land_avg
        self.province = province


def moncton_and_fredericton(city_list: list[City]) -> list[City]:
    """
    Combine the Moncton and Fredericton City instances because we have data overlap in Manya and
    Sima's data.

    Preconditions:
        - len(city_list) != 0
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
    new_list.append(City(name, year, inter, intra, comp, house, land, moncton.province))
    return new_list


class Province:
    """
    A class to store province data.

    Instance Attributes:
        - name: the name of the province
        - city_list: a list of all the relevant cities in the province
        - covid_cases: a list of the COVID cases each year in the province

    Representation Invariants:
        - self.name != ''
        - city_list != []
        - len(covid_cases) == 5
    """
    name: str
    city_list: list[City]
    covid_cases: list[int]

    def __init__(self, name: str, city_list: list[City], covid_cases: list[int]) -> None:
        self.name = name
        self.city_list = city_list
        self.covid_cases = covid_cases


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['classes', 'covid_dataset', 'manya_dataset', 'bokeh', 'sarah_dataset',
                          'sima_dataset', 'pandas'],
        # the names (strs) of imported modules
        # 'allowed-io': [],     # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'R0902', 'R0913']
    })
