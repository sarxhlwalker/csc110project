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
    >>> split = split_file(sorted_file)
    """
    inter = dataframe[dataframe['Components of population growth'] == 'Net interprovincial migration']
    intra = dataframe[dataframe['Components of population growth'] == 'Net intraprovincial migration']
    return (inter, intra)


def condense_time(dataframe, r: set[str], ds: int, cols: int):
    """Create a copy of a dataframe such that REF_DATE is the span of one year, and VALUE is
        adjusted accordingly.

    ds indicates whether or not it is a MLS dataset (month year; 1) or other (year month; 0).

    >>> file = test('Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Saint John.csv', \
            ['Date', 'Composite_Benchmark_SA', 'Single_Family_Benchmark_SA', \
            'One_Storey_Benchmark_SA', 'Two_Storey_Benchmark_SA', 'Apartment_Benchmark_SA'])
    >>> condensed = condense_time(file, {'2015', '2016', '2017', '2018', '2019', '2020'}, 1, 5)
    """
    lst = []
    if ds == 1:
        for year in r:
            lst.append(build_year(dataframe, year, cols))




    return df


def build_year(dataframe, year, cols):
    """Helper function for condense_time."""
    by = {}
    count = 0
    for i in range(len(dataframe)):
        if dataframe.loc[i, 0][4:] == year:
            by[year] = [dataframe.loc[i, x] for x in range(cols)] # how to add instead of replace? 
            count += 1



if __name__ == '__main__':
    pass
