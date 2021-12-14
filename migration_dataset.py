"""
CSC110: Final Project

This file contains functions that relates to the 'city migration and others' dataset.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of professors and TAs
at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.
.l
This file is Copyright (c) 2021 Sarah Walker, Manya Mittal, Sima Shmuylovich, and Grace Fung.
"""

import pandas as pd


def split_type_migration(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split city_migration data into two separate DataFrames; one for intraprovincial
    migration and the other for interprovincial.

    >>> import main
    >>> file = main.read_file('Data Sets/city migration and others.csv', ['REF_DATE', 'GEO', \
                'Components of population growth', 'VALUE'])
    >>> sorted_file = main.sort_file(file, {'Net interprovincial migration', \
            'Net intraprovincial migration'}, 'Components of population growth')
    >>> inter, intra = split_type_migration(sorted_file)
    """
    inter = dataframe[dataframe['Components of population growth']
                      == 'Net interprovincial migration']
    intra = dataframe[dataframe['Components of population growth']
                      == 'Net intraprovincial migration']
    return inter, intra


def restrict_city_migration(inter: pd.DataFrame, intra: pd.DataFrame, city: str) -> \
        tuple[list, list]:
    """
    Return the restriction of the data from split_file to the data only pertaining to city. No more
    computations are needed on Sarah's dataset, so this returns a list, ready for input to class
    City.

    >>> import main
    >>> city_migration = main.read_file('Data Sets/city migration and others.csv', \
                ['REF_DATE', 'GEO', 'Components of population growth', 'VALUE'])
    >>> city_migration = main.sort_file(city_migration,{'Net interprovincial migration', \
            'Net intraprovincial migration'}, 'Components of population growth')
    >>> inter, intra = split_type_migration(city_migration)
    >>> st_john_inter, st_john_intra = restrict_city_migration(inter, intra, \
                'Saint John (CMA), New Brunswick')
    """
    city_inter = []
    city_intra = []
    for _, row in inter.iterrows():
        # .iterrows() returns each row in a tuple of the form (index, Series)
        if row.loc['GEO'] == city:
            city_inter.append(row.loc['VALUE'])
        # gets only the values that correspond with the given city

    for _, row in intra.iterrows():
        if row.loc['GEO'] == city:
            city_intra.append(row.loc['VALUE'])
    # repeats the same thing for intra dataframe

    return city_inter, city_intra


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['main', 'classes', 'covid_dataset', 'hpi_dataset', 'bokeh',
                          'migration_dataset',
                          'house_land_dataset', 'pandas'],
        # the names (strs) of imported modules
        # 'allowed-io': [],     # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
