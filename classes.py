import main
import datetime

class City:
    """"
    A class to contain all the necessary information for one city.

    >>> st_john_mls = main.read_file('Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Saint John.csv', \
                 ['Date', 'Single_Family_HPI_SA'])
    >>> st_john_mls = main.cleans_nan(st_john_mls)
    >>> st_john_mls_list = main.condense_time_manya(st_john_mls, ['2015', '2016', '2017', \
                                                '2018', '2019'], 'Single_Family_HPI_SA')

    >>> type_of_house = 'Total (house and land)'
    >>> house = main.read_file('Data Sets/House and Land Prices.csv', ['REF_DATE', 'GEO', \
                'New housing price indexes', 'VALUE'])
    >>> house = main.sort_file(house, {type_of_house}, 'New housing price indexes')
    >>> house = main.cleans_nan(house)
    >>> house = main.restrict_city_sima(house, "St. John's, Newfoundland and Labrador", \
                                'GEO')
    >>> house_list = main.condense_time_sima(house, ['2015', '2016', '2017', '2018', '2019', \
                '2020'])

    TODO: Call Sima's HPI adjuster before calling test.avg_datasets

    >>> h_l_avg = main.avg_datasets(st_john_mls_list, house_list)

    >>> year = [(datetime.date(2015, 7, 1), datetime.date(2016, 6, 30)), (datetime.date(2016, 7, 1), \
                datetime.date(2017, 6, 30)), (datetime.date(2017, 7, 1), datetime.date(2018, 6, 30)), \
                 (datetime.date(2018, 7, 1), datetime.date(2018, 6, 30)), \
                 (datetime.date(2019, 7, 1), datetime.date(2020, 6, 30))]

    >>> city_migration = main.read_file('Data Sets/city migration and others.csv', ['REF_DATE', 'GEO', \
                'Components of population growth', 'VALUE'])
    >>> city_migration = main.sort_file(city_migration,{'Net interprovincial migration', \
            'Net intraprovincial migration'}, 'Components of population growth')
    >>> inter, intra = main.split_file(city_migration)
    >>> st_john_inter = main.restrict_city_sarah(inter, 'Saint John (CMA), New Brunswick', 'GEO', 'VALUE')
    >>> st_john_intra = main.restrict_city_sarah(intra, 'Saint John (CMA), New Brunswick', 'GEO', 'VALUE')

    >>> house_only = main.read_file('Data Sets/House and Land Prices.csv', ['REF_DATE', 'GEO', \
                'New housing price indexes', 'VALUE'])
    >>> house_only = main.sort_file(house_only, {'House only'}, 'New housing price indexes')
    >>> house_only = main.cleans_nan(house_only)
    >>> house_only = main.restrict_city_sima(house_only, \
                                    "St. John's, Newfoundland and Labrador", 'GEO')
    >>> house_only_list = main.condense_time_sima(house_only, ['2015', '2016', '2017', '2018', '2019', \
                '2020'])

    >>> land_only = main.read_file('Data Sets/House and Land Prices.csv', ['REF_DATE', 'GEO', \
                'New housing price indexes', 'VALUE'])
    >>> land_only = main.sort_file(land_only, {'Land only'}, 'New housing price indexes')
    >>> land_only = main.cleans_nan(land_only)
    >>> land_only = main.restrict_city_sima(land_only, \
                                    "St. John's, Newfoundland and Labrador", 'GEO')
    >>> land_only_list = main.condense_time_sima(land_only, ['2015', '2016', '2017', '2018', '2019', \
                '2020'])

    >>> st_john = City('Saint John', year, st_john_intra, st_john_inter, h_l_avg, \
                        house_only_list, land_only_list)
    """
    name: str
    year: list
    intraprovincial: list[int]      # sarah
    interprovincial: list[int]      # sarah
    house_land_avg: list[float]     # manya and sima
    house_avg: list[float]          # sima
    land_avg: list[float]           # sima

    def __init__(self, name: str, year: list[tuple[datetime.datetime, datetime.datetime]],
                 intraprovincial: list[int], interprovincial: list[int],
                 house_land_avg: list[float], house_avg: list[float],
                 land_avg: list[float]) -> None:
        self.name = name
        self.year = year
        self.intraprovincial = intraprovincial
        self.interprovincial = interprovincial
        self.house_land_avg = house_land_avg
        self.house_avg = house_avg
        self.land_avg = land_avg

    def get_values_xy(self, par: list) -> dict[str, list]:
        """
        Return a dictionary with the key as the name of the city, and the value is a list of
        tuples that store the x and y co-ordinates.

        Preconditions:
            - TODO: Ensure that the order of year corresponds to the other of the intraprovincial
              (TODO CONT'D) values; and that their lengths are the same.
        """
        d = {}
        lst = []
        for x in range(len(self.year)):
            temp = (self.year[x], par[x])
            lst.append(temp)
            d[self.name] = lst
        return d

if __name__ == '__main__':
    pass
