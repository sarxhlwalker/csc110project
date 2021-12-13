"""
CSC110: Final Project

This file contains functions and helper functions that create all the instances of
the city class and province class (see classes.py).
Run this file to execute all our functions and see the outputted graphs.
The graphs will be made as separate html files that can be manually opened individually.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of professors and TAs
at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021 Sarah Walker, Manya Mittal, Sima Shmuylovich, and Grace Fung.
"""

import pandas as pd
import classes
import covid_dataset
import sarah_dataset
import manya_dataset
import sima_dataset
import plotting

# GENERAL VARIABLES FOR MAIN.PY

# CITY_DICT maps Manya's city names to a list of first Sarah's and then Sima's city names.

CITY_DICT = {'Cambridge': ['Kitchener - Cambridge - Waterloo (CMA), Ontario',
                           'Kitchener-Cambridge-Waterloo, Ontario'],
             'Fredricton':
                 ['Fredericton (CA), New Brunswick',
                  'Saint John, Fredericton, and Moncton, New Brunswick'],
             'Greater Moncton':
                 ['Moncton (CMA), New Brunswick',
                  'Saint John, Fredericton, and Moncton, New Brunswick'],
             'Greater Toronto': ['Toronto (CMA), Ontario', 'Toronto, Ontario'],
             'Greater Vancouver':
                 ['Vancouver (CMA), British Columbia', 'Vancouver, British Columbia'],
             'Kitchener and Waterloo':
                 ['Kitchener - Cambridge - Waterloo (CMA), Ontario',
                  'Kitchener-Cambridge-Waterloo, Ontario'],
             'London St Thomas': ['London (CMA), Ontario', 'London, Ontario'],
             'Montreal CMA':
                 ['Montréal (CMA), Quebec', 'Montréal, Quebec'],
             'Niagara Region':
                 ['St. Catharines - Niagara (CMA), Ontario', 'St. Catharines-Niagara, Ontario'],
             'Quebec CMA': ['Québec (CMA), Quebec', 'Québec, Quebec'],
             'Saint John':
                 ['Saint John (CMA), New Brunswick', "St. John's, Newfoundland and Labrador"],
             'Victoria': ['Victoria (CMA), British Columbia', 'Victoria, British Columbia']}

CITIES_SIMA = ['Kitchener-Cambridge-Waterloo, Ontario',
               'Saint John, Fredericton, and Moncton, New Brunswick',
               "St. John's, Newfoundland and Labrador",
               'Toronto, Ontario', 'Vancouver, British Columbia',
               'Kitchener-Cambridge-Waterloo, Ontario',
               'London, Ontario',
               'Montréal, Quebec',
               'St. Catharines-Niagara, Ontario',
               'Québec, Quebec',
               "St. John's, Newfoundland and Labrador",
               'Victoria, British Columbia']

SIMA_FILE = 'Data Sets/House and Land Prices.csv'
SARAH_FILE = 'Data Sets/city migration and others.csv'
MANYA_FILES = {'Cambridge':
               'Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Cambridge.csv',
               'Fredricton':
                   'Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Fredricton.csv',
               'Greater Moncton':
                   'Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Greater Moncton.csv',
               'Greater Toronto':
                   'Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Greater '
                   'Toronto.csv',
               'Greater Vancouver':
                   'Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Greater '
                   'Vancouver.csv',
               'Kitchener and Waterloo':
                   'Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Kitchener '
                   'and Waterloo.csv',
               'London St Thomas':
                   'Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted London '
                   'St Thomas.csv',
               'Montreal CMA':
                   'Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Montreal CMA.csv',
               'Niagara Region':
                   'Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Niagara Region.csv',
               'Quebec CMA':
                   'Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Quebec CMA.csv',
               'Saint John':
                   'Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Saint John.csv',
               'Victoria':
                   'Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Victoria.csv'}


# MAIN FUNCTIONS (CALLED IN IF __MAIN__)

def create_cities(sima: str, sarah: str, manya: dict[str, str]) -> list[classes.City]:
    """
    Create a list of City instances so that we can plot their values.
    """
    condensed = create_sima(sima)  # Above prepares Sima's dataset into a dictionary with one key
    # (being a city) mapping to three lists of floats: five years of house only HPI, land only HPI,
    # and the total house and land HPI.

    inter, intra = create_sarah(sarah)  # Returns two DataFrames: one for every relevant city's net
    # interprovincial migration value and one for every relevant city's intraprovincial migration.

    city_accumulator = []  # Accumulator for classes.City instances

    for key in CITY_DICT:  # for each relevant city

        timed_manya_city = create_manya(manya, key, ['2015', '2016', '2017', '2018', '2019'])
        # Returns a list of five years' worth of the city's Single Family SA HPI.

        house, land, house_land_avg = create_items(condensed, key, timed_manya_city)  # Returns
        # relevant information from Sima's dataset for this specific city.

        province = get_province(key)  # Retrieves the province attribute for the city.

        city_inter, city_intra = sarah_dataset.restrict_city_sarah(inter, intra, CITY_DICT[key][0])
        # Returns a five-item list of the city's interprovincial and intraprovincial values.

        city_accumulator.append(classes.City(key, [2016, 2017, 2018, 2019, 2020], city_inter,
                                city_intra, house_land_avg, house, land, province))  # Creates a
        # classes.City instance and appends to city_accumulator

    city_accumulator = classes.moncton_and_fredericton(city_accumulator)  # Combines the Moncton and
    # Fredericton classes.City instances into one City, because we had data overlap.

    return city_accumulator  # Returns list of all classes.City instances we have data for


def plot_cities(city_accumulator: list) -> set[str]:
    """Now the actual plotting.

    This function should:
      - go through every item in city_accumulator
      - call plotting.plot_migration
      - call plotting.plot_hpi
      - ensure that all plots are uniquely named (ie. no duplicate files for one city, but each
      city should have 2 graphs) and stored in a folder specifically for plots
      - plot the COVID data
    """
    for city in city_accumulator:
        plotting.plot_migration(city)
        plotting.plot_hpi(city)
    return {specific_city.province for specific_city in city_accumulator}


def create_provinces(city_accumulator: list, covid_cases: dict[str, list[int]]) -> \
        list[classes.Province]:
    """
    Create a list of Province instances so we can plot their values.
    """
    prov_accumulator = []
    for province in covid_cases:
        covid_nums = covid_cases[province]
        cities = []
        for city in city_accumulator:
            if city.province == province:
                cities.append(city)
        prov_accumulator.append(classes.Province(province, cities, covid_nums))
    return prov_accumulator


def plot_provinces(prov_accumulator: list) -> None:
    """
    Plot a number of graphs juxtaposing the values from each city in a shared province against
    each other and the number of COVID cases in that province.
    """
    for prov in prov_accumulator:
        plotting.plot_interprovincial(prov, 500)  # Can change these 500s to any other integer;
        # only scales COVID case numbers. Picked 500 because it makes the graphs look the best.
        plotting.plot_intraprovincial(prov, 500)
        plotting.plot_tot_hpi(prov, 500)
        plotting.plot_house_hpi(prov, 500)
        plotting.plot_land_hpi(prov, 500)


# HELPER FUNCTIONS FOR MAIN FUNCTIONS


def create_sima(sima: str) -> list:
    """
    Helper function for create_cities. Prepares Sima's dataset into a dictionary with one key
    (being a city) mapping to three lists of floats: five years of house only HPI, land only HPI,
    and the total house and land HPI.
    """
    adjusted_values = sima_dataset.adjust_sima_hpi(pd.read_csv(sima))
    restricted_cities = sima_dataset.restrict_city_sima(adjusted_values, CITIES_SIMA)
    split_type_for_cities = sima_dataset.split_type_sima(restricted_cities)
    condensed = sima_dataset.run_condense_time(split_type_for_cities)
    sima_dataset.append_sima_csv(condensed)
    return condensed


def create_sarah(sarah: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Helper function for create_cities. Prepares Sarah's dataset to return two DataFrames:
    one for every relevant city's net interprovincial migration value and one for every relevant
    city's intraprovincial migration.
    """
    sar = read_file(sarah, ['REF_DATE', 'GEO',
                            'Components of population growth', 'VALUE'])
    sorted_sar = sort_file(sar, {'Net interprovincial migration',
                                 'Net intraprovincial migration'},
                           'Components of population growth')
    inter, intra = sarah_dataset.split_type_sarah(sorted_sar)

    return inter, intra


def create_manya(manya: dict[str, str], key: str, manya_year: list) -> list[float]:
    """
    Helper function for create_cities. Returns a list of five years'
    worth of the city's Single Family SA HPI.
    """
    manya_city = read_file(manya[key], ['Date', 'Single_Family_HPI_SA'])
    clean_manya_city = manya_dataset.cleans_nan(manya_city)
    timed_manya_city = manya_dataset.condense_time_manya(clean_manya_city, manya_year)
    return timed_manya_city


def get_province(key: str) -> str:
    """
    Helper function for create_cities. Returns the province attribute for the city provided.
    """
    _, prov = CITY_DICT[key][0].split(',')
    province = prov.strip()
    return province


def create_items(condensed: list, key: str, timed_manya_city: list[float]) -> \
        tuple[list[float], list[float], list[float]]:
    """
    Helper function for create_cities.
    """
    house = []
    land = []
    house_land_avg = []

    for item in condensed:
        for single_key in item:
            if single_key == CITY_DICT[key][1]:  # Finds the key/value of the relevant city from
                # Sima's dataset
                house = item[single_key][0]
                land = item[single_key][1]
                comp = item[single_key][2]  # Acquires the relevant information from the
                # dictionary to call house_land_avg
                house_land_avg = avg_datasets(timed_manya_city, comp)

    return house, land, house_land_avg


# HELPER FUNCTIONS THAT 2+ DATASETS USE. FOR SPECIFIC DATASET FUNCTIONS, SEE OTHER PYTHON FILES.


def read_file(filename: str, lst: list[str]) -> pd.DataFrame:
    """
    Save only the desired columns in lst from filename as a DataFrame.

    >>> file = read_file('Data Sets/city migration and others.csv', ['REF_DATE', 'GEO', \
                'Components of population growth', 'VALUE'])
    """
    file = pd.read_csv(filename, usecols=lst)
    return file


def sort_file(dataframe: pd.DataFrame, keywords: set[str], column: str) -> pd.DataFrame:
    """
    Create and return a new DataFrame containing only rows whose specified column are a
        specific keyword.

    >>> file = read_file('Data Sets/city migration and others.csv', ['REF_DATE', 'GEO', \
                'Components of population growth', 'VALUE'])
    >>> sorted_file = sort_file(file, {'Net interprovincial migration', \
            'Net intraprovincial migration'}, 'Components of population growth')
    """
    lst = []
    for x in range(len(dataframe)):
        if dataframe.loc[x, column] in keywords:
            lst.append(dataframe.loc[x])
    return pd.DataFrame(lst)


def avg_datasets(list_cities: list[float], house_list: list[float]) -> list[float]:
    """
    Return a list of average values from Manya's Single Family HPI values and Sima's HPI value.
    This is for one specific city only.

    Preconditions:
        - len(list_cities) == len(house_list)
    """
    return_list = []
    for i in range(len(list_cities)):
        s = list_cities[i] + house_list[i]
        avg = s / 2
        return_list.append(avg)
    return return_list


if __name__ == '__main__':
    city_list = create_cities(SIMA_FILE, SARAH_FILE, MANYA_FILES)
    provinces = plot_cities(city_list)
    covid_dict = covid_dataset.get_covid_cases_per_province(provinces)
    prov_list = create_provinces(city_list, covid_dict)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['classes', 'covid_dataset', 'manya_dataset', 'plotting', 'sarah_dataset',
                          'sima_dataset', 'pandas'],
        # the names (strs) of imported modules
        # 'allowed-io': [],     # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
