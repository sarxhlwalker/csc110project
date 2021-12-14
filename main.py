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
import migration_dataset
import hpi_dataset
import house_land_dataset
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

CITIES_HOUSE_LAND = ['Kitchener-Cambridge-Waterloo, Ontario',
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

HOUSE_LAND_FILE = 'Data Sets/House and Land Prices.csv'
MIGRATION_FILE = 'Data Sets/city migration and others.csv'
HPI_FILES = {'Cambridge':
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

def create_cities(house_land: str, migration: str, hpi: dict[str, str]) -> list[classes.City]:
    """
    Create a list of City instances so that we can plot their values.

    >>> list_city = create_cities(HOUSE_LAND_FILE, MIGRATION_FILE, HPI_FILES)
    """
    condensed = create_house_land(house_land)  # Above prepares the House and Land dataset into a
    # dictionary with one key (being a city) mapping to three lists of floats: five years of house
    # only HPI, land only HPI, and the total house and land HPI.

    inter, intra = create_migration(migration)  # Returns two DataFrames: one for every relevant
    # city's net interprovincial migration value and one for every relevant city's intraprovincial
    # migration.

    city_accumulator = []  # Accumulator for classes.City instances

    for key in CITY_DICT:  # for each relevant city

        timed_hpi_city = create_hpi(hpi, key, ['2015', '2016', '2017', '2018', '2019'])
        # Returns a list of five years' worth of the city's Single Family SA HPI.

        house, land, house_land_avg = create_items(condensed, key, timed_hpi_city)  # Returns
        # relevant information from the House and Land dataset for this specific city.

        province = get_province(key)  # Retrieves the province attribute for the city.

        city_inter, city_intra = migration_dataset.restrict_city_migration(inter, intra,
                                                                           CITY_DICT[key][0])
        # Returns a five-item list of the city's interprovincial and intraprovincial values.

        city_accumulator.append(classes.City(key, [2016, 2017, 2018, 2019, 2020], city_inter,
                                city_intra, house_land_avg, house, land, province))  # Creates a
        # classes.City instance and appends to city_accumulator

    city_accumulator = classes.merge_cities(city_accumulator,
                                                       [('Greater Moncton', 'Fredricton'),
                                                        ('Cambridge', 'Kitchener and Waterloo')])
    # Combines the tuple of classes.City instances into one City, because we had data overlap.

    return city_accumulator  # Returns list of all classes.City instances we have data for


def plot_cities(city_accumulator: list) -> set[str]:
    """Now the actual plotting.

    This function runs through every item in city_accumulator, on which it calls
    plotting.plot_migration and plotting.plot_hpi.

    It returns a set of provinces from the list of cities such that the if __main__ block can easily
    call create_provinces and plot_provinces.

    Preconditions:
        - city_accumulator != []

    >>> list_city = create_cities(HOUSE_LAND_FILE, MIGRATION_FILE, HPI_FILES)
    >>> provs = plot_cities(city_accumulator)
    """
    for city in city_accumulator:
        plotting.plot_migration(city)
        plotting.plot_hpi(city)
    return {specific_city.province for specific_city in city_accumulator}


def create_provinces(city_accumulator: list, covid_cases: dict[str, list[int]]) -> \
        list[classes.Province]:
    """
    Create a list of Province instances so we can plot their values.

    Preconditions:
        - city_accumulator != []
        - covid_cases != {}

    >>> list_city = create_cities(HOUSE_LAND_FILE, MIGRATION_FILE, HPI_FILES)
    >>> provs = plot_cities(list_city)
    >>> dict_covid = covid_dataset.get_covid_cases_per_province(provs)
    >>> list_provs = create_provinces(list_city, dict_covid)
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

    Preconditions:
        - prov_accumulator != []

    >>> list_city = create_cities(HOUSE_LAND_FILE, MIGRATION_FILE, HPI_FILES)
    >>> provs = plot_cities(list_city)
    >>> dict_covid = covid_dataset.get_covid_cases_per_province(provs)
    >>> list_provs = create_provinces(list_city, dict_covid)
    >>> plot_provinces(list_provs)
    """
    for prov in prov_accumulator:
        plotting.plot_interprovincial(prov, 500)  # Can change these 500s to any other integer;
        # only scales COVID case numbers. Picked 500 because it makes the graphs look the best.
        plotting.plot_intraprovincial(prov, 500)
        plotting.plot_tot_hpi(prov, 500)
        plotting.plot_house_hpi(prov, 500)
        plotting.plot_land_hpi(prov, 500)


# HELPER FUNCTIONS FOR MAIN FUNCTIONS


def create_house_land(house_land: str) -> list:
    """
    Helper function for create_cities. Prepares the House and Land dataset into a dictionary with
    one key (being a city) mapping to three lists of floats: five years of house only HPI,
    land only HPI, and the total house and land HPI.
    """
    adjusted_values = house_land_dataset.adjust_house_land_hpi(pd.read_csv(house_land))
    restricted_cities = house_land_dataset.restrict_city_house_land(adjusted_values, CITIES_HOUSE_LAND)
    split_type_for_cities = house_land_dataset.split_type_house_land(restricted_cities)
    condensed = house_land_dataset.run_condense_time(split_type_for_cities)
    house_land_dataset.append_house_land_csv(condensed)
    return condensed


def create_migration(migration: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Helper function for create_cities. Prepares the migration dataset to return two DataFrames:
    one for every relevant city's net interprovincial migration value and one for every relevant
    city's intraprovincial migration.
    """
    migr = read_file(migration, ['REF_DATE', 'GEO',
                            'Components of population growth', 'VALUE'])
    sorted_migr = sort_file(migr, {'Net interprovincial migration',
                                 'Net intraprovincial migration'},
                           'Components of population growth')
    inter, intra = migration_dataset.split_type_migration(sorted_migr)
    return inter, intra


def create_hpi(hpis: dict[str, str], key: str, hpi_year: list) -> list[float]:
    """
    Helper function for create_cities. Returns a list of five years'
    worth of the city's Single Family SA HPI.
    """
    hpi_city = read_file(hpis[key], ['Date', 'Single_Family_HPI_SA'])
    clean_hpi_city = hpi_dataset.cleans_nan(hpi_city)
    timed_hpi_city = hpi_dataset.condense_time_hpi(clean_hpi_city, hpi_year)
    return timed_hpi_city


def get_province(key: str) -> str:
    """
    Helper function for create_cities. Returns the province attribute for the city provided.
    """
    _, prov = CITY_DICT[key][0].split(',')
    province = prov.strip()
    return province


def create_items(condensed: list, key: str, timed_hpi_city: list[float]) -> \
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
                # the House and Land dataset
                house = item[single_key][0]
                land = item[single_key][1]
                comp = item[single_key][2]  # Acquires the relevant information from the
                # dictionary to call house_land_avg
                house_land_avg = avg_datasets(timed_hpi_city, comp)
    return house, land, house_land_avg


# HELPER FUNCTIONS THAT 2+ DATASETS USE. FOR SPECIFIC DATASET FUNCTIONS, SEE OTHER PYTHON FILES.


def read_file(filename: str, lst: list[str]) -> pd.DataFrame:
    """
    Save only the desired columns in lst from filename as a DataFrame.

    >>> f = read_file('Data Sets/city migration and others.csv', ['REF_DATE', 'GEO', \
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


def avg_datasets(list_cities: list[float], house_land_list: list[float]) -> list[float]:
    """
    Return a list of average values from the Single Family HPI values and the total HPI value.
    This is for one specific city only.

    Preconditions:
        - len(list_cities) == len(house_land_list)
    """
    return_list = []
    for i in range(len(list_cities)):
        s = list_cities[i] + house_land_list[i]
        avg = s / 2
        return_list.append(avg)
    return return_list


if __name__ == '__main__':
    city_list = create_cities(HOUSE_LAND_FILE, MIGRATION_FILE, HPI_FILES)
    provinces = plot_cities(city_list)
    print('Cities have been plotted! Provinces are now being plotted. Thanks for your patience.')

    covid_dict = covid_dataset.get_covid_cases_per_province(provinces)
    prov_list = create_provinces(city_list, covid_dict)
    plot_provinces(prov_list)

    print('\n Province graphs have now been plotted! Feel free to open any of the HTML graphs in '
          '/City_Plots or /Province_Plots in your browser of choice.')

    # import python_ta
    #
    # python_ta.check_all(config={
    #     'extra-imports': ['classes', 'covid_dataset', 'hpi_dataset', 'plotting',
    #                       'migration_dataset',
    #                       'house_land_dataset', 'pandas'],
    #     # the names (strs) of imported modules
    #     # 'allowed-io': [],     # the names (strs) of functions that call print/open/input
    #     'max-line-length': 100,
    #     'disable': ['R1705', 'C0200']
    # })
