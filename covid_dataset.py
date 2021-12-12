import pandas as pd


# def get_canada_cases(dataframe: pd.DataFrame) -> list[int]:
#     """
#     # TODO: Add the doctest
#     """
#     canada_cases = []
#     for _, row in dataframe.iterrows():
#         # iterrows() returns  each row in a tuple of the form (index, Series)
#         if row.loc['prname'] == 'Canada':
#             canada_cases.append(row.loc['numconf'])
#         # gets only the values that correspond with the Canada
#     return canada_cases
#
#
# def condense_time_covid(cases: list[int]) -> float:
#     """
#     # TODO: Add the doctest
#     """
#     return sum(cases) / len(cases)
#     # the covid cases dataset only has values for 2020 so if we want to aggregate them,
#     # just take the average of all of them


def get_covid_cases_per_province(provinces: set[str]) -> dict[str, list[int]]:
    """ return a dictionary mapping all the provinces in provinces to the corresponding
    total number of corresponding covid cases during 2015 to June 2020"""
    covid_file = pd.read_csv('Data Sets/covid19-download.csv')
    c_reversed = reversed(covid_file.index)
    # an iterable that has reversed the order of rows in covid_file
    province_to_covid_cases = {}
    for province in provinces:
        province_to_covid_cases[province] = get_covid_case_value(province, covid_file, c_reversed)
    # iterates through each province in the set provinces and finds the corresponding
    # number of covid cases in 2020 for that province

    return province_to_covid_cases


def get_covid_case_value(province: str, covid_file: pd.DataFrame, c_reversed: reversed) -> list[int]:
    """ return a list of integers that represents the total covid cases during 2015 to June 2020
    for the corresponding province"""
    cases_list = [0, 0, 0, 0]  # initializes a list with 4 zeros corresponding to the covid
    # cases for years 2015/2016, 2016/2017, 2017/2018, 2018/2019
    for row in c_reversed:  # iterates through the reversed order of the covid_file
        if any(f'2020-0{i}' in covid_file.loc[row, 'date']
               for i in range(7)) \
                and province in covid_file.loc[row, 'prname']:
            # checks if 2020-00 <= date <= 2020-06 and if it matches the province
            cases_list.append(covid_file.loc[row, 'numtotal'])  # adds the total cases to the list
            return cases_list


