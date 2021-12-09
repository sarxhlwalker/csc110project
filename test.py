import pandas as pd
import statistics

def test(filename: str, lst: list[str]):
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


def city_restrict(inter, intra, city: str):
    """Return the restriction of the data from split_file to the data only pertaining to city.

    Preconditions:
        - len(inter) == len(intra)

    >>> city_migration = test('Data Sets/city migration and others.csv', ['REF_DATE', 'GEO', \
                'Components of population growth', 'VALUE'])
    >>> city_migration = sort_file(city_migration,{'Net interprovincial migration', \
            'Net intraprovincial migration'}, 'Components of population growth')
    >>> inter, intra = split_file(city_migration)
    >>> st_john_inter, st_john_intra = city_restrict(inter, intra, 'Saint John')
    """
    city_inter = []
    city_intra = []

    for row in inter.iterrows():
        if row.loc['GEO'] == city:
            city_inter.append(row.loc['VALUE'])

    for row in intra.iterrows():
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

"""


def condense_time_manya(dataframe, range_of_years: list[str], col: str) -> list:
    """Create a copy of a dataframe such that REF_DATE is the span of one year, and VALUE is
        adjusted accordingly.
    >>> file = test('Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Saint John.csv', \
            ['Date', 'Single_Family_Benchmark_SA'])
    >>> clean_file = cleans_nan(file)
    >>> condensed = condense_time_manya(clean_file, ['2015', '2016', '2017', '2018', '2019', \
            '2020'], 'Single_Family_Benchmark_SA')
    """
    return_list = []
    for x in range_of_years:
        year_list = []
        for row in range(len(dataframe)):
            if dataframe.loc[row, 'Date'][4:] == x:
                year_list.append(dataframe.loc[row, col])
        avg = sum(year_list) / len(year_list)
        return_list.append(avg)
    return return_list


if __name__ == '__main__':
    pass
