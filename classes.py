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


def merge_cities(city_list: list[City], merges: list[tuple]) -> list[City]:
    """
    Combine the Moncton and Fredericton City instances because we have data overlap in Manya and
    Sima's data.

    Preconditions:
        - len(city_list) != 0
    """
    new_list = []
    city1 = city_list[0]
    city2 = city_list[1]  # just initializing these variables; won't actually use them
    for tup in merges:
        for city in city_list:
            if city.name == tup[0]:
                city1 = city
            elif city.name == tup[1]:
                city2 = city
        name = city1.name + ' and ' + city2.name
        year = city1.year  # all year values are the same
        inter, intra, comp, house, land = append_values(city1, city2)
        new_list.append(City(name, year, inter, intra, comp, house, land, city1.province))
    tups = [val for tup in merges for val in tup]
    for city in city_list:
        if city.name not in tups:
            new_list.append(city)
    return new_list


def append_values(city1: City, city2: City) -> tuple[list, list, list, list, list]:
    """
    Helper function for merge_cities.
    """
    inter = []
    intra = []
    comp = []
    house = []
    land = []
    for i in range(5):
        inter.append(city1.interprovincial[i])   # the migration dataset is too general and has the
        # same values for both city1 and city2
        intra.append(city1.intraprovincial[i])
        comp.append((city1.house_land_avg[i] + city2.house_land_avg[i]) / 2)  # the HPI dataset
        # has two different values for the cities and so there will be two different averages,
        # so we average the two averages.
        house.append(city1.house_avg[i])  # Again, the House and Land dataset is too general and
        # so will have the same values across both cities
        land.append(city1.land_avg[i])
    return inter, intra, comp, house, land


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
