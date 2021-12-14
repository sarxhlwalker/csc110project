"""
CSC110: Final Project

This file contains functions that extract data from the dataset with covid-19 statistics.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of professors and TAs
at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021 Sarah Walker, Manya Mittal, Sima Shmuylovich, and Grace Fung.
"""

import pandas as pd


def get_covid_cases_per_province(provinces: set[str]) -> dict[str, list[int]]:
    """
    Returns a dictionary mapping all the provinces in provinces to the corresponding
    total number of corresponding covid cases during 2015 to June 2020.

    Preconditions:
        - provinces != set()

    >>> import main
    >>> city_list = main.create_cities(main.HOUSE_LAND_FILE, main.MIGRATION_FILE, main.HPI_FILES)
    >>> provs = main.plot_cities(city_list)
    >>> prov_covid = get_covid_cases_per_province(provs)
    """
    covid_file = pd.read_csv('Data Sets/covid19-download.csv')
    c_reversed = reversed(covid_file.index)
    # an iterable that has reversed the order of rows in covid_file
    province_to_covid_cases = {}
    for province in provinces:
        province_to_covid_cases[province] = get_covid_case_value(province, covid_file, c_reversed)
    # iterates through each province in the set provinces and finds the corresponding
    # number of covid cases in 2020 for that province
    return province_to_covid_cases


def get_covid_case_value(province: str, covid_file: pd.DataFrame, c_reversed: reversed) -> \
        list[int]:
    """
    Helper function for get_covid_cases_per_province.

    Returns a list of integers that represents the total covid cases during 2015 to June 2020
    for the corresponding province.

    Preconditions:
        - province != ''
    """
    cases_list = [0, 0, 0, 0]  # initializes a list with 4 zeros corresponding to the covid
    # cases for years 2015/2016, 2016/2017, 2017/2018, 2018/2019
    for row in c_reversed:  # iterates through the reversed order of the covid_file
        if any(f'2020-0{i}' in covid_file.loc[row, 'date']
               for i in range(7)) \
                and province in covid_file.loc[row, 'prname']:
            # checks if 2020-00 <= date <= 2020-06 and if it matches the province
            cases_list.append(covid_file.loc[row, 'numtotal'])  # adds the total cases to the list
            return cases_list
    return cases_list


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['classes', 'covid_dataset', 'hpi_dataset', 'bokeh',
                          'migration_dataset',
                          'house_land_dataset', 'pandas'],
        # the names (strs) of imported modules
        # 'allowed-io': [],     # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
