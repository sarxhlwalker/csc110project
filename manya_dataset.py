import main
import pandas as pd


def cleans_nan(dataframe):
    """Removes random commas in Manya's dataframes.

    >>> file = main.read_file('Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Saint John.csv', \
            ['Date', 'Single_Family_HPI_SA'])
    >>> clean_file = cleans_nan(file)
    """
    return dataframe.dropna()


def condense_time_manya(dataframe: pd.DataFrame, range_of_years: list[str]) \
        -> list[float]:
    """
    Create a copy of one of Manya's dataframes such that Date is the span of one year, and Single_Family_HPI_SA is
    adjusted accordingly.

    >>> file = main.read_file('Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Saint John.csv', \
            ['Date', 'Single_Family_HPI_SA'])
    >>> clean_file = cleans_nan(file)
    >>> condensed = condense_time_manya(clean_file, ['2015', '2016', '2017', '2018', '2019'], \
            'Single_Family_HPI_SA')

    TODO: I think this doctest should expect a return??
    """
    return_list = []
    for x in range_of_years:
        year_list = []
        row = 0
        while row < len(dataframe):
            if dataframe.loc[row, 'Date'][0:3] == 'Jul' and dataframe.loc[row, 'Date'][4:] == x:
                # checks if the date is currently at July and if the year is equal to the current
                # year in range_of_years
                year_list = iterate_twelve(dataframe, year_list, row)
                row += 12  # skips 12 rows, to the next time that the month is July
            else:
                row += 1  # since the month didn't start at July, we don't want to start
                # aggregating the data for that year yet, so move onto the next row instead
        avg = sum(year_list) / len(year_list)
        return_list.append(avg)
    return return_list


def iterate_twelve(dataframe: pd.DataFrame, year_list: list[str], row: int):
    """
    Iterates through the dataframe tweleve times and adds the data for each row into year_list.
    This will include the data from July in one year to June in the next year.

    Helper function for condense_time_manya.
    """
    for i in range(12):
        year_list.append(dataframe.loc[row + i, 'Single_Family_HPI_SA'])
    return year_list


if __name__ == '__main__':
    pass
