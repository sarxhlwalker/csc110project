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


def cleans_nan(dataframe):
    """Removes random commas.
    >>> file = test('Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Saint John.csv', \
            ['Date', 'Single_Family_Benchmark_SA'])
    >>> clean_file = cleans_nan(file)
    """
    return dataframe.dropna()


## HARD STUFF BELOW!

"""
- put together times -- average the 'value' columns when we do this
  - iterate through the column 'Date', if the substring has the correct year that we want, then we add the value to a list for that year 
  - after we finish iterating through, add all the values in the list by calling the sum function and then divide by the length of the list by calling the len function (gives us the avergae for that year)
  - append average to another list (ie. what we return)? 
  - Repeat for every year


- note: worry about years starting in july after

"""


def condense_time_manya(dataframe, range_of_years: list[str]) -> list:
    """Create a copy of a dataframe such that REF_DATE is the span of one year, and VALUE is
        adjusted accordingly.
    >>> file = test('Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Saint John.csv', \
            ['Date', 'Single_Family_Benchmark_SA'])
    >>> clean_file = cleans_nan(file)
    >>> condensed = condense_time_manya(clean_file, ['2015', '2016', '2017', '2018', '2019', '2020'])
    """
    return_list = []
    for x in range_of_years:
        year_list = []
        for row in range(len(dataframe)):
            if dataframe.loc[row, 'Date'][4:] == x:
                year_list.append(dataframe.loc[row, 'Single_Family_Benchmark_SA'])
        avg = sum(year_list) / len(year_list)
        return_list.append(avg)
    return return_list


if __name__ == '__main__':
    pass
