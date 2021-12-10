import pandas as pd
import classes
import sarah_dataset
import manya_dataset
import sima_dataset

# TODO:
# - Create a run_simulation function that calls all the functions that we made in the order that we
#     want the TA's to run it in. implement CITY_DICT in run_simulation()
# - Deal with COVID-19 Data
# - instead of pass in if __main__, put run_simulation()
# - add pythonta to if __main__
# - finish plotting
# - make website
# - complexity things (ex. downloading csv)

# CITY_DICT maps Manya's city names to a list of first Sarah's and then Sima's city names.

CITY_DICT = {'Cambridge': ['Kitchener - Cambridge - Waterloo (CMA), Ontario',
                           'Kitchener-Cambridge-Waterloo, Ontario'], 'Fredricton':
                 ['Fredericton (CA), New Brunswick', 'Saint John, Fredericton, and Moncton, New Brunswick'],
             'Greater Moncton':
                 ['Moncton (CMA), New Brunswick', "St. John's, Newfoundland and Labrador"],
             'Greater Toronto': ['Toronto (CMA), Ontario', 'Toronto, Ontario'], 'Greater Vancouver':
                 ['Vancouver (CMA), British Columbia', 'Vancouver, British Columbia'],
             'Kitchener and Waterloo':
                 ['Kitchener - Cambridge - Waterloo (CMA), Ontario',
                  'Kitchener-Cambridge-Waterloo, Ontario'],
             'London St Thomas': ['London (CMA), Ontario', 'London, Ontario'], 'Montreal CMA':
                 ['Montréal (CMA), Quebec', 'Montréal, Quebec'], 'Niagara Region':
                 ['St. Catharines - Niagara (CMA), Ontario', 'St. Catharines-Niagara, Ontario'],
             'Quebec CMA': ['Québec (CMA), Quebec', 'Québec, Quebec'], 'Saint John':
                 ['Saint John (CMA), New Brunswick', "St. John's, Newfoundland and Labrador"],
             'Victoria': ['Victoria (CMA), British Columbia', 'Victoria, British Columbia']}

def create_cities(sima: str, sarah: str, manya: dict[str, str]) -> list:
    """
    Do the thing!
    """
    # TODO: call sima's functions on sima.

    year = [2016, 2017, 2018, 2019, 2020]

    sar = read_file(sarah, ['REF_DATE', 'GEO',
                            'Components of population growth', 'VALUE'])
    sorted_sar = sort_file(sar, {'Net interprovincial migration',
                            'Net intraprovincial migration'}, 'Components of population growth')
    inter, intra = sarah_dataset.split_type_sarah(sorted_sar)

    manya_year = ['2015', '2016', '2017', '2018', '2019']

    city_list = []

    for key in CITY_DICT:
        manya_city = read_file(manya[key], ['Date', 'Single_Family_HPI_SA'])
        clean_manya_city = manya_dataset.cleans_nan(manya_city)
        timed_manya_city = manya_dataset.condense_time_manya(clean_manya_city, manya_year)

        # TODO: Average timed_manya_city with whatever we get from Sima's dataset.

        city_inter, city_intra = sarah_dataset.restrict_city_sarah(inter, intra, CITY_DICT[key][0])

        # TODO: this method of initializing cities won't work.

        city_list.append(classes.City(key, year, city_inter, city_intra, tot_avg, house_only,
                                    land_only))

    return city_list


def plot_things(city_list: list) -> None:
    """Now the actual plotting."""


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
    Return a list of values from the two datasets provided.

    Preconditions:
        - len(city_list) == len(house_list)

    >>> city = read_file('Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Saint John.csv', \
              ['Date', 'Single_Family_HPI_SA'])
    >>> city = manya_dataset.cleans_nan(city)
    >>> city_list = manya_dataset.condense_time_manya(city, ['2015', '2016', '2017', '2018', '2019'], \
                                        'Single_Family_HPI_SA')

    >>> house = read_file('Data Sets/House and Land Prices.csv', ['REF_DATE', 'GEO', \
                'New housing price indexes', 'VALUE'])
    TODO: Sima's thing.

    >>> house_land_avg = avg_datasets(city_list, house_list)
    """
    return_list = []
    for i in range(len(city_list)):
        s = city_list[i] + house_list[i]
        avg = s / 2
        return_list.append(avg)
    return return_list


if __name__ == '__main__':
    sima = 'Data Sets/Housing in 6 Major Cities.csv'
    sarah = 'Data Sets/city migration and others.csv'
    manya = {'Cambridge':
                 'Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Cambridge.csv',
             'Fredricton':
                 'Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Fredricton.csv',
             'Greater Moncton':
                 'Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Greater Moncton.csv',
             'Greater Toronto':
                 'Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Greater Toronto.csv',
             'Greater Vancouver':
                 'Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Greater Vancouver.csv',
             'Kitchener and Waterloo':
                 'Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Kitchener and Waterloo.csv',
             'London St Thomas':
                 'Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted London St Thomas.csv',
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

    # TODO: include COVID-19 data.

    create_cities(sima, sarah, manya)
