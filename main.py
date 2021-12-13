"""

Final Project


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

def create_cities(sima: str, sarah: str, manya: dict[str, str]) -> list:
    """
    Create a list of City instances so that we can plot their values.
    """
    year = [2016, 2017, 2018, 2019, 2020]

    adjusted_values = \
        sima_dataset.adjust_sima_hpi(pd.read_csv(sima))
    restricted_cities = sima_dataset.restrict_city_sima(adjusted_values, CITIES_SIMA)
    split_type_for_cities = sima_dataset.split_type_sima(restricted_cities)
    condensed = sima_dataset.run_condense_time(split_type_for_cities)
    sima_dataset.append_sima_csv(condensed)

    # Above prepares Sima's dataset into a dictionary with one key (being a city) mapping to three
    # lists of floats: five years of house only HPI, land only HPI, and the total house
    # and land HPI.

    sar = read_file(sarah, ['REF_DATE', 'GEO',
                            'Components of population growth', 'VALUE'])
    sorted_sar = sort_file(sar, {'Net interprovincial migration',
                                 'Net intraprovincial migration'},
                           'Components of population growth')
    inter, intra = sarah_dataset.split_type_sarah(sorted_sar)

    # Above returns two DataFrames: one for every relevant city's net interprovincial migration
    # value and one for every relevant city's intraprovincial migration.

    manya_year = ['2015', '2016', '2017', '2018', '2019']

    city_list = []  # Accumulator for classes.City instances

    for key in CITY_DICT:  # for each relevant city
        manya_city = read_file(manya[key], ['Date', 'Single_Family_HPI_SA'])
        clean_manya_city = manya_dataset.cleans_nan(manya_city)
        timed_manya_city = manya_dataset.condense_time_manya(clean_manya_city, manya_year)

        # Above returns a list of five years' worth of the city's Single Family SA HPI.

        house_land_avg = []
        house = []
        land = []

        for item in condensed:
            for single_key in item:
                if single_key == CITY_DICT[key][1]:  # Finds the key/value of the relevant city from
                    # Sima's dataset
                    house = item[single_key][0]
                    land = item[single_key][1]
                    comp = item[single_key][2]

                    # Above acquires the relevant information from the dictionary to call
                    # house_land_avg

                    house_land_avg = avg_datasets(timed_manya_city, comp)

                    # We have acquired all the information we need from the loop(s),
                    # so we can safely break to save time.

        _, prov = CITY_DICT[key][0].split(',')
        province = prov.strip()

        # Above retrieves the province attribute for the city.

        city_inter, city_intra = sarah_dataset.restrict_city_sarah(inter, intra, CITY_DICT[key][0])

        # Above returns a five-item list of the city's interprovincial and intraprovincial values.

        city_list.append(classes.City(key, year, city_inter,
                                      city_intra, house_land_avg, house, land, province))

        # Creates a classes.City instance and appends to city_list

    city_list = classes.moncton_and_fredericton(city_list)

    # Above combines the Moncton and Fredericton classes.City instance into one City,
    # because we had data overlap.

    return city_list  # Returns list of all classes.City instances we have data for


def plot_cities(city_list: list) -> tuple[list, list, set]:
    """Now the actual plotting.

    This function should:
      - go through every item in city_list
      - call plotting.plot_migration
      - call plotting.plot_hpi
      - ensure that all plots are uniquely named (ie. no duplicate files for one city, but each
      city should have 2 graphs) and stored in a folder specifically for plots
      - plot the COVID data
    """
    city_migration = []
    city_hpi = []
    for city in city_list:
        city_migration.append(plotting.plot_migration(city))
        city_hpi.append(plotting.plot_hpi(city))

    return city_migration, city_hpi, {city.province for city in city_list}


def create_provinces(city_list: list, covid_cases: dict[str, list[int]]) -> list:
    """
    Create a list of Province instances so we can plot their values.
    """
    prov_list = []
    for province in covid_cases:
        covid_nums = covid_cases[province]
        cities = []
        for city in city_list:
            if city.province == province:
                cities.append(city)
        prov_list.append(classes.Province(province, cities, covid_nums))
    return prov_list


def plot_provinces(prov_list: list) -> tuple[list, list, list, list, list]:
    """
    Plot a number of graphs juxtaposing the values from each city in a shared province against
    each other and the number of COVID cases in that province.
    """
    prov_intra = []
    prov_inter = []
    prov_hpi = []
    prov_house = []
    prov_land = []
    for prov in prov_list:
        prov_inter.append(plotting.plot_interprovincial(prov, 500))
        prov_intra.append(plotting.plot_intraprovincial(prov, 500))
        prov_hpi.append(plotting.plot_tot_hpi(prov, 500))
        prov_house.append(plotting.plot_house_hpi(prov, 500))
        prov_land.append(plotting.plot_land_hpi(prov, 500))
    return prov_inter, prov_intra, prov_hpi, prov_house, prov_land


# HELPER FUNCTIONS THAT 2+ DATASETS USE. FOR SPECIFIC DATASET FUNCTIONS, SEE OTHER PYTHON FILES.


def read_file(filename: str, lst: list[str]) -> pd.DataFrame:
    """
    Save only the desired columns in lst from filename as a DataFrame.

    >>> file = read_file('Data Sets/city migration and others.csv', ['REF_DATE', 'GEO', \
                'Components of population growth', 'VALUE'])
    """
    file = pd.read_csv(filename, usecols=lst)
    return file


def sort_file(dataframe, keywords: set[str], column: str):
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


def avg_datasets(city_list: list[float], house_list: list[float]) -> list[float]:
    """
    Return a list of average values from Manya's Single Family HPI values and Sima's HPI value.
    This is for one specific city only.

    Preconditions:
        - len(city_list) == len(house_list)

    TODO: Doctest

    """
    return_list = []
    for i in range(len(city_list)):
        s = city_list[i] + house_list[i]
        avg = s / 2
        return_list.append(avg)
    return return_list


if __name__ == '__main__':
    city_list = create_cities(SIMA_FILE, SARAH_FILE, MANYA_FILES)
    city_migration, city_hpi, provinces = plot_cities(city_list)
    covid_dict = covid_dataset.get_covid_cases_per_province(provinces)
    prov_list = create_provinces(city_list, covid_dict)
    prov_inter, prov_intra, prov_hpi, prov_house, prov_land = plot_provinces(prov_list)
    # plotting.plot_all(city_migration, city_hpi, prov_inter, prov_intra, prov_hpi, prov_house,
    #                   prov_land)

    # TODO: sort out python_ta

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['classes', 'covid_dataset', 'manya_dataset', 'plotting', 'sarah_dataset',
                          'sima_dataset', 'pandas'],
        # the names (strs) of imported modules
        # 'allowed-io': [],     # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
