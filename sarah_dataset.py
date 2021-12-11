import main
import pandas as pd


def split_type_sarah(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split city_migration data into two separate DataFrames; one for intraprovincial
    migration and the other for interprovincial.

    >>> file = main.read_file('Data Sets/city migration and others.csv', ['REF_DATE', 'GEO', \
                'Components of population growth', 'VALUE'])
    >>> sorted_file = main.sort_file(file, {'Net interprovincial migration', \
            'Net intraprovincial migration'}, 'Components of population growth')
    >>> inter, intra = split_type_sarah(sorted_file)
    """
    inter = dataframe[dataframe['Components of population growth'] == 'Net interprovincial migration']
    intra = dataframe[dataframe['Components of population growth'] == 'Net intraprovincial migration']
    return inter, intra


def restrict_city_sarah(inter: pd.DataFrame, intra: pd.DataFrame, city: str) -> tuple[list, list]:
    """
    Return the restriction of the data from split_file to the data only pertaining to city. No more
    computations are needed on Sarah's dataset, so this returns a list, ready for input to Class
    City.

    Preconditions:
        - len(inter) == len(intra)

    >>> city_migration = main.read_file('Data Sets/city migration and others.csv', ['REF_DATE', 'GEO', \
                'Components of population growth', 'VALUE'])
    >>> city_migration = main.sort_file(city_migration,{'Net interprovincial migration', \
            'Net intraprovincial migration'}, 'Components of population growth')
    >>> inter, intra = split_type_sarah(city_migration)
    >>> st_john_inter, st_john_intra = restrict_city_sarah(inter, intra, \
                'Saint John (CMA), New Brunswick')
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


if __name__ == '__main__':
    pass
