import pandas as pd


def get_canada_cases(dataframe: pd.DataFrame) -> list[int]:
    """
    # TODO: Add the doctest
    """
    canada_cases = []
    for _, row in dataframe.iterrows():
        # iterrows() returns  each row in a tuple of the form (index, Series)
        if row.loc['prname'] == 'Canada':
            canada_cases.append(row.loc['numconf'])
        # gets only the values that correspond with the Canada
    return canada_cases


def condense_time_covid(cases: list[int]) -> float:
    """
    # TODO: Add the doctest
    """
    return sum(cases) / len(cases)
    # the covid cases dataset only has values for 2020 so if we want to aggregate them,
    # just take the average of all of them
