import pandas as pd

# CITY_DICT maps Manya's city names to a list of first Sarah's and then Sima's city names.

CITY_DICT = {'Cambridge': ['Kitchener - Cambridge - Waterloo (CMA), Ontario', \
                           'Kitchener-Cambridge-Waterloo, Ontario'], 'Fredricton': \
    ['Fredericton (CA), New Brunswick', 'Saint John, Fredericton, and Moncton, New Brunswick'], \
             'Greater Moncton': \
                 ['Moncton (CMA), New Brunswick', "St. John's, Newfoundland and Labrador"], \
    'Greater Toronto': ['Toronto (CMA), Ontario', 'Toronto, Ontario'], 'Greater Vancouver': \
             ['Vancouver (CMA), British Columbia', 'Vancouver, British Columbia'], \
    'Guelph and district': ['Guelph (CMA), Ontario', 'Guelph, Ontario'], 'Kitchener and Waterloo': \
             ['Kitchener - Cambridge - Waterloo (CMA), Ontario', \
              'Kitchener-Cambridge-Waterloo, Ontario'], \
    'London St Thomas': ['London (CMA), Ontario', 'London, Ontario'], 'Montreal CMA': \
                 ['Montréal (CMA), Quebec', 'Montréal, Quebec'], 'Niagara Region': \
                 ['St. Catharines - Niagara (CMA), Ontario', 'St. Catharines-Niagara, Ontario'], \
    'Quebec CMA': ['Québec (CMA), Quebec', 'Québec, Quebec'], 'Saint John': \
                 ['Saint John (CMA), New Brunswick', "St. John's, Newfoundland and Labrador"], \
    'Victoria': ['Victoria (CMA), British Columbia', 'Victoria, British Columbia']}

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
    >>> sorted_file = sort_file(file,{'Net interprovincial migration', \
            'Net intraprovincial migration'}, 'Components of population growth')
    """
    lst = []
    for x in range(len(dataframe)):
        if dataframe.loc[x, column] in keywords:
            lst.append(dataframe.loc[x])
    return pd.DataFrame(lst)


def split_file(dataframe):
    """
    Split city_migration data into two separate DataFrames; one for intraprovincial
    migration and the other for interprovincial.

    >>> file = read_file('Data Sets/city migration and others.csv', ['REF_DATE', 'GEO', \
                'Components of population growth', 'VALUE'])
    >>> sorted_file = sort_file(file, {'Net interprovincial migration', \
            'Net intraprovincial migration'}, 'Components of population growth')
    >>> inter, intra = split_file(sorted_file)
    """
    inter = dataframe[dataframe['Components of population growth'] == 'Net interprovincial migration']
    intra = dataframe[dataframe['Components of population growth'] == 'Net intraprovincial migration']
    return inter, intra


def restrict_city_sarah(dataframe: pd.DataFrame, city: str, lookup: str, add: str) -> list:
    """
    Return the restriction of the data from split_file to the data only pertaining to city. No more
    computations are needed on Sarah's dataset, so this returns a list, ready for input to Class
    City.

    Preconditions:
        - len(inter) == len(intra)

    >>> city_migration = read_file('Data Sets/city migration and others.csv', ['REF_DATE', 'GEO', \
                'Components of population growth', 'VALUE'])
    >>> city_migration = sort_file(city_migration,{'Net interprovincial migration', \
            'Net intraprovincial migration'}, 'Components of population growth')
    >>> inter, intra = split_file(city_migration)
    >>> st_john_inter = restrict_city_sarah(inter, 'Saint John (CMA), New Brunswick', 'GEO', 'VALUE')
    >>> st_john_intra = restrict_city_sarah(inter, 'Saint John (CMA), New Brunswick', 'GEO', 'VALUE')
    """
    lst = []
    for _, row in dataframe.iterrows():
        if row.loc[lookup] == city:
            lst.append(row.loc[add])
    return lst


def restrict_city_sima(dataframe: pd.DataFrame, city: str, lookup: str) -> pd.DataFrame:
    """Restricts city but returns a DataFrame, because more computations are needed on Sima's data.

    >>> type_of_house = 'Total (house and land)'
    >>> house = read_file('Data Sets/House and Land Prices.csv', ['REF_DATE', 'GEO', \
                'New housing price indexes', 'VALUE'])
    >>> house = sort_file(house, {type_of_house}, 'New housing price indexes')
    >>> house = cleans_nan(house)
    >>> house = restrict_city_sima(house, "St. John's, Newfoundland and Labrador", \
                                'GEO')
    """
    lst = []
    for _, row in dataframe.iterrows():
        if row.loc[lookup] == city:
            lst.append(row)
    return pd.DataFrame(lst)


def cleans_nan(dataframe):
    """Removes random commas.

    >>> file = read_file('Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Saint John.csv', \
            ['Date', 'Single_Family_Benchmark_SA'])
    >>> clean_file = cleans_nan(file)
    """
    return dataframe.dropna()


""" 
TODO: 
- Create a run_simulation function that calls all the functions that we made in the order that we 
    want the TA's to run it in. implement CITY_DICT in run_simulation()
- instead of pass in if __main__, put run_simulation()
- add pythonta to if __main__
- finish plotting
- make website
- complexity things (ex. downloading csv) 
"""

def condense_time_manya(dataframe: pd.DataFrame, range_of_years: list[str], col: str) \
        -> list[float]:
    """
    Create a copy of a dataframe such that Date is the span of one year, and Single_Family_Benchmark_SA is
    adjusted accordingly.

    >>> file = read_file('Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Saint John.csv', \
            ['Date', 'Single_Family_Benchmark_SA'])
    >>> clean_file = cleans_nan(file)
    >>> condensed = condense_time_manya(clean_file, ['2015', '2016', '2017', '2018', '2019'], \
            'Single_Family_Benchmark_SA')
    """
    return_list = []
    for x in range_of_years:
        year_list = []
        row = 0
        while row < len(dataframe):
            if dataframe.loc[row, 'Date'][0:3] == 'Jul' and dataframe.loc[row, 'Date'][4:] == x:
                year_list = iterate_twelve(dataframe, year_list, row, col)
                row += 12
            else:
                row += 1
        avg = sum(year_list) / len(year_list)
        return_list.append(avg)
    return return_list


def iterate_twelve(dataframe: pd.DataFrame, year_list: list[str], row: int, col: str):
    """
    Add twelve items to year_list. Helper function for condense_time_manya.
    """
    for i in range(12):
        year_list.append(dataframe.loc[row + i, col])
    return year_list


def condense_time_sima(dataframe: pd.DataFrame, range_years: list[str]) -> list[float]:
    """
    Create a copy of a dataframe such that REF_DATE is the span of one year from July to June, and
    VALUE is adjusted accordingly.

    >>> house = read_file('Data Sets/House and Land Prices.csv', ['REF_DATE', 'GEO', \
                'New housing price indexes', 'VALUE'])
    >>> house = sort_file(house, {'Total (house and land)'}, 'New housing price indexes')
    >>> house = cleans_nan(house)
    >>> house_list = condense_time_sima(house, ['2015', '2016', '2017', '2018', '2019', \
                '2020'])

    >>> house_only = read_file('Data Sets/House and Land Prices.csv', ['REF_DATE', 'GEO', \
                'New housing price indexes', 'VALUE'])
    >>> house_only = sort_file(house_only, {'House only'}, 'New housing price indexes')
    >>> house_only = cleans_nan(house_only)
    >>> house = restrict_city_sima(house, "St. John's, Newfoundland and Labrador", \
                                'GEO')
    >>> house_only_list = condense_time_sima(house_only, ['2015', '2016', '2017', '2018', '2019', \
                '2020'])
    """
    return_list = []
    month1 = {'07', '08', '09', '10', '11', '12'}
    month2 = {'01', '02', '03', '04', '05', '06'}
    for year in range(len(range_years) - 1):
        year_list = []
        for _, row in dataframe.iterrows():
            if row.loc['REF_DATE'][5:] in month1 and row.loc['REF_DATE'][0:4] == range_years[year]:
                year_list.append(row.loc['VALUE'])
            elif row.loc['REF_DATE'][5:0] in month2 and row.loc['REF_DATE'][0:4] == \
                range_years[year + 1]:
                    year_list.append(row.loc['VALUE'])
        avg = sum(year_list) / len(year_list)
        return_list.append(avg)
    return return_list


def avg_datasets(city_list: list[float], house_list: list[float]) -> list[float]:
    """
    Return a list of values from the two datasets provided.

    Preconditions:
        - len(city_list) == len(house_list)

    >>> city = read_file('Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Saint John.csv', \
              ['Date', 'Single_Family_Benchmark_SA'])
    >>> city = cleans_nan(city)
    >>> city_list = condense_time_manya(city, ['2015', '2016', '2017', '2018', '2019'], \
                                        'Single_Family_Benchmark_SA')

    >>> type_of_house = 'Total (house and land)'
    >>> house = read_file('Data Sets/House and Land Prices.csv', ['REF_DATE', 'GEO', \
                'New housing price indexes', 'VALUE'])
    >>> house = sort_file(house, {type_of_house}, 'New housing price indexes')
    >>> house = cleans_nan(house)
    >>> house = restrict_city_sima(house, "St. John's, Newfoundland and Labrador", \
                                'GEO')
    >>> house_list = condense_time_sima(house, ['2015', '2016', '2017', '2018', '2019', \
                '2020'])

    >>> house_land_avg = avg_datasets(city_list, house_list)
    """
    return_list = []
    for i in range(len(city_list)):
        s = city_list[i] + house_list[i]
        avg = s / 2
        return_list.append(avg)
    return return_list


def adjust_sima_hpi(dataframe: pd.DataFrame) -> dict:
    """
    Return a dictionary mapping (month, year, land, house, or composite) to (house price indexes with index=100 set in
    January 2005).

    The file originally had index=100 set in January 2016. This was done so that our data matched the other csv files.
    """
    hpi_base_case = []
    for row in range(34562, 34682):  # 2005-01
        hpi_base_case.append(dataframe.loc[row, 'VALUE'])
    adjusted_values = {}
    for row in range(49682, 56882):
        old_hpi = dataframe.loc[row, 'VALUE']
        key = str(dataframe.loc[row, 'REF_DATE']) + ', ' + str(
            dataframe.loc[row, 'GEO'] + ', ' + dataframe.loc[row, 'New housing price indexes'])
        if hpi_base_case[(row - 2) % 120] is not None and old_hpi is not None:
            adjusted_values[key] = round((float(old_hpi) / float(hpi_base_case[(row - 2) % 120]))
                                         * 100, 1)
        else:
            adjusted_values[key] = None
    return adjusted_values


if __name__ == '__main__':
    pass
