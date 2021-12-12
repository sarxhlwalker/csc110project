"""
All functions that have to do with Sima's Dataset.
"""
import main
import pandas as pd


def adjust_sima_hpi(dataframe: pd.DataFrame) -> dict[tuple[str, str, str], float]:
    """
    Returns a dictionary mapping (month, year, type) to (house price indexes with index=100 set in January 2005).
    The file originally had index=100 set in December 2016.
    It is being adjusted to match the the other csv files beong used for this project.

    Preconditions:
      - dataframe = pd.read_csv("18100205.csv")

    TODO: shouldn't this precondition be a doctest? b/c it doesn't restrict anything right
    TODO: seconding this; the csv file I read from my computer is not called the same thing either,
    since we renamed it when adding to the GitHub (and I pulled the csv files from there)
    """
    hpi_base_case = []
    for row in range(34560, 34680):  # 2005-01
        hpi_base_case.append(dataframe.loc[row, 'VALUE'])
    adjusted_values = {}
    for row in range(49680, 56880):  # 2015-07 to 2020-06
        old_hpi = dataframe.loc[row, 'VALUE']
        key = (dataframe.loc[row, 'REF_DATE'], dataframe.loc[row, 'GEO'],
               dataframe.loc[row, 'New housing price indexes'])
        if hpi_base_case[(row - 2) % 120] is not None and old_hpi is not None:
            adjusted_values[key] = round((float(old_hpi) / float(hpi_base_case[row % 120])) * 100, 1)
        else:
            adjusted_values[key] = None
    return adjusted_values


def restrict_city_sima(adjusted_values: dict, cities: list[str]) -> list[dict[tuple[str, str, str], float]]:
    """Returns a list of dictionaries where each dictionary maps a tuple (date, city, type) to a float (hpi).
    Dictionaries are only created for cities if they are in the given list.

    Restricts city but returns a DataFrame, because more computations are needed on Sima's data.

    TODO: This doesn't match with the type annotation?

    TODO: write doctest
    """
    restricted_cities = []
    for city in cities:
        city_list = {}
        for key, value in adjusted_values.items():
            if key[1] == city:
                city_list[key] = value
        restricted_cities.append(city_list)
        # gets only the values that correspond with the given city
    return restricted_cities


def split_type_sima(restricted_cities: list[dict[tuple[str, str, str], float]]) -> list[
    tuple[dict[tuple[str, str, str], float], dict[tuple[str, str, str], float], dict[tuple[str, str, str], float]]]:
    """
    Split Sima's datatype into three dictionaries: HPI for total house and land, house only, and land only.
    """
    split_type_for_cities = []
    for city in restricted_cities:
        house_type = {}
        land_type = {}
        composite_type = {}
        count = 0
        for key, value in city.items():
            if count % 3 == 0:
                composite_type[key] = value
                # if count is a multiple of 3, the row contains data about total house and land HPIs
            elif count % 3 == 1:
                house_type[key] = value
            else:
                land_type[key] = value
            count += 1
        split_type_for_cities.append((house_type, land_type, composite_type))
    return split_type_for_cities


def condense_time_sima(dictionary: dict) -> list[float]:
    """
    Create a copy of a dataframe such that REF_DATE is the span of one year from July to June, and
    VALUE is adjusted accordingly.
    """
    # TODO: Explain the pattern of this function using comments
    return_list = []
    count = 0
    that_year = []
    for key, value in dictionary.items():
        if count % 11 == 0 and count > 1:
            return_list.append(round(sum(that_year) / 11, 1))
            that_year = []
        that_year.append(value)
        count += 1
    return return_list


def run_condense_time(split_type_for_cities: list[tuple[dict[tuple[str, str, str], float],
                                                        dict[tuple[str, str, str], float],
                                                        dict[tuple[str, str, str], float]]]) -> \
        list[dict[str, tuple[list[float], list[float], list[float]]]]:
    """
    Implement consense_time_sima.
    """
    cities = []
    for city in split_type_for_cities:
        individual_city = {}
        house, land, composite = city
        city_key = ''
        for key, value in house.items():
            city_key = key[1]
            break  # EW EW EW EW EW EW
        individual_city[city_key] = (condense_time_sima(house), condense_time_sima(land), condense_time_sima(composite))
        cities.append(individual_city)
    return cities


def append_sima_csv(cities: list[dict[str, tuple[list[float], list[float], list[float]]]]) -> None:
    """
    Appends csv files I created as needed.
    Refer to sima_template.csv to see how they looked before the function was called.
    """
    reset_sima_csvs()
    from csv import writer
    for city in cities:
        for key, value in city.items():
            row_house = [key, 'House only', value[0][0], value[0][1], value[0][2], value[0][3], value[0][4]]
            row_land = [key, 'Land only', value[1][0], value[1][1], value[1][2], value[1][3], value[1][4]]
            row_composite = [key, 'Composite (house and land)', value[2][0], value[2][1], value[2][2], value[2][3],
                             value[2][4]]
            # TODO: What if we used dataclasses to avoid all this crazy indexing lol

            with open('sima_house.csv', 'a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(row_house)
                f_object.close()
            with open('sima_land.csv', 'a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(row_land)
                f_object.close()
            with open('sima_composite.csv', 'a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(row_composite)
                f_object.close()


def reset_sima_csvs() -> None:
    """
    Empties sima's csv files.
    """
    f = open('sima_house.csv', "w")
    f.truncate()
    f.close()

    f = open('sima_land.csv', "w")
    f.truncate()
    f.close()

    f = open('sima_composite.csv', "w")
    f.truncate()
    f.close()


if __name__ == '__main__':
    adjusted_values = adjust_sima_hpi(pd.read_csv("18100205.csv"))
    restricted_cities = restrict_city_sima(adjusted_values, main.CITIES_SIMA)
    split_type_for_cities = split_type_sima(restricted_cities)
    condensed = run_condense_time(split_type_for_cities)
    append_sima_csv(condensed)
