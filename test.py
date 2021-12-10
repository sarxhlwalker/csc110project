import pandas as pd
from typing import Optional

def test(filename: str, lst: list[str]) -> pd.DataFrame:
    """
    Save only the desired columns in lst from filename as a DataFrame.

    >>> file = test('Data Sets/city migration and others.csv', ['REF_DATE', 'GEO', \
                'Components of population growth', 'VALUE'])
    """
    file = pd.read_csv(filename, usecols=lst)
    return file


def sort_file(dataframe, keywords: set[str], column: str):
    """
    Create and return a new DataFrame containing only rows whose specified column are a
        specific keyword.

    Generalization untested.
    >>> file = test('Data Sets/city migration and others.csv', ['REF_DATE', 'GEO', \
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

    >>> file = test('Data Sets/city migration and others.csv', ['REF_DATE', 'GEO', \
                'Components of population growth', 'VALUE'])
    >>> sorted_file = sort_file(file, {'Net interprovincial migration', \
            'Net intraprovincial migration'}, 'Components of population growth')
    >>> inter, intra = split_file(sorted_file)
    """
    inter = dataframe[dataframe['Components of population growth'] == 'Net interprovincial migration']
    intra = dataframe[dataframe['Components of population growth'] == 'Net intraprovincial migration']
    return inter, intra


def city_restrict(inter, intra, city: str) -> tuple[list, list]:
    """Return the restriction of the data from split_file to the data only pertaining to city.

    Preconditions:
        - len(inter) == len(intra)

    >>> city_migration = test('Data Sets/city migration and others.csv', ['REF_DATE', 'GEO', \
                'Components of population growth', 'VALUE'])
    >>> city_migration = sort_file(city_migration,{'Net interprovincial migration', \
            'Net intraprovincial migration'}, 'Components of population growth')
    >>> inter, intra = split_file(city_migration)
    >>> st_john_inter, st_john_intra = city_restrict(inter, intra, 'Saint John (CMA), New Brunswick')
    """
    city_inter = []
    city_intra = []

    for _, row in inter.iterrows():
        if row.loc['GEO'] == city:
            city_inter.append(row.loc['VALUE'])

    for _, row in intra.iterrows():
        if row.loc['GEO'] == city:
            city_intra.append(row.loc['VALUE'])

    return city_inter, city_intra


def cleans_nan(dataframe):
    """Removes random commas.
    >>> file = test('Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Saint John.csv', \
            ['Date', 'Single_Family_Benchmark_SA'])
    >>> clean_file = cleans_nan(file)
    """
    return dataframe.dropna()


"""
- years need to start in july
- Create a run_simulation function that calls all the functions that we made in the order that we want the TA's to run 
    it in
- instead of pass in if __main__, put run_simulation()
- make dictionary mapping manya's dataset city names to sarah and sima's dataset city names; str -> list
"""


def condense_time_manya(dataframe, range_of_years: list[str], col: str, target: str) -> list:
    """Create a copy of a dataframe such that REF_DATE is the span of one year, and VALUE is
        adjusted accordingly.
    >>> file = test('Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Saint John.csv', \
            ['Date', 'Single_Family_Benchmark_SA'])
    >>> clean_file = cleans_nan(file)
    >>> condensed = condense_time_manya(clean_file, ['2015', '2016', '2017', '2018', '2019', \
            '2020'], 'Single_Family_Benchmark_SA', 'Date')
    """
    return_list = []
    for x in range_of_years:
        year_list = []
        for row in range(len(dataframe)):
            if dataframe.loc[row, target][4:] == x:
                year_list.append(dataframe.loc[row, col])
        avg = sum(year_list) / len(year_list)
        return_list.append(avg)
    return return_list


def condense_time_sima(dataframe: pd.DataFrame, range_years: list[str], col: str, target: str) -> list[float]:
    """
    Does the thing.

    >>> house = test('Data Sets/House and Land Prices.csv', ['REF_DATE', 'GEO', \
                'New housing price indexes', 'VALUE'])
    >>> house = sort_file(house, {'Total (house and land)'}, 'New housing price indexes')
    >>> house = cleans_nan(house)
    >>> house_list = condense_time_sima(house, ['2015', '2016', '2017', '2018', '2019', \
                '2020'], 'VALUE', 'REF_DATE')
    """
    return_list = []
    for year in range_years:
        year_list = []
        for _, row in dataframe.iterrows():
            if row.loc['REF_DATE'][0:4] == year:
                year_list.append(row.loc['VALUE'])
        avg = sum(year_list) / len(year_list)
        return_list.append(avg)
    return return_list


def avg_things(city_list: Optional[list[float]], house_list: list[float]) -> list[float]:
    """
    Return a list of values from the two datasets provided.

    Preconditions:
        - len(city_list) == len(house_list)

    >>> city = test('Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Saint John.csv', \
              ['Date', 'Single_Family_Benchmark_SA'])
    >>> city = cleans_nan(city)
    >>> city_list = condense_time_manya(city, ['2015', '2016', '2017', '2018', '2019', \
              '2020'], 'Single_Family_Benchmark_SA', 'Date')

    >>> type_of_house = 'Total (house and land)'
    >>> house = test('Data Sets/House and Land Prices.csv', ['REF_DATE', 'GEO', \
                'New housing price indexes', 'VALUE'])
    >>> house = sort_file(house, {type_of_house}, 'New housing price indexes')
    >>> house = cleans_nan(house)
    >>> house_list = condense_time_manya(house, ['2015', '2016', '2017', '2018', '2019', \
                '2020'], 'VALUE', 'REF_DATE')

    >>> house_land_avg = avg_things(city_list, house_list)
    """
    return_list = []
    for i in range(len(city_list)):
        s = city_list[i] + house_list[i]
        avg = s / 2
        return_list.append(avg)
    return return_list


if __name__ == '__main__':
    pass
