import test
import datetime


class City:
    """"Main Superclass of all the cities.

    >>> st_john_mls = test.test('Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Saint John.csv', \
                 ['Date', 'Single_Family_Benchmark_SA'])
    >>> st_john_mls = test.cleans_nan(st_john_mls)
    >>> st_john_mls = test.condense_time_manya(st_john_mls, ['2015', '2016', '2017', '2018', '2019', \
                                                '2020'], 'Single_Family_Benchmark_SA')
    >>> year = [(datetime.date(2015, 6, 1), datetime.date(2016, 6, 1)), (datetime.date(2016, 6, 1), \
                datetime.date(2017, 6, 1)), (datetime.date(2017, 6, 1), datetime.date(2018, 6, 1)), \
                 (datetime.date(2018, 6, 1), datetime.date(2018, 6, 1)), \
                 (datetime.date(2019, 6, 1), datetime.date(2020, 6, 1))]
    >>> city_migration = test.test('Data Sets/city migration and others.csv', ['REF_DATE', 'GEO', \
                'Components of population growth', 'VALUE'])
    >>> city_migration = test.sort_file(city_migration,{'Net interprovincial migration', \
            'Net intraprovincial migration'}, 'Components of population growth')
    >>> inter, intra = test.split_file(city_migration)
    >>> st_john_inter, st_john_intra = test.city_restrict(inter, intra, 'Saint John')
    """
    name: str
    year: list[tuple[datetime.datetime, datetime.datetime]]
    intraprovincial: list[int]      # sarah
    interprovincial: list[int]      # sarah
    house_land_avg: list[float]     # manya and sima
    house_avg: list[float]          # sima
    land_avg: list[float]           # sima

    def __init__(self, name: str, year: list[tuple[datetime.datetime, datetime.datetime]], intraprovincial: list[int],
             interprovincial: list[int], house_land_avg: list[float], house_avg: list[float],
             land_avg: list[float]) -> None:
        self.name = name
        self.year = year
        self.intraprovincial = intraprovincial
        self.interprovincial = interprovincial
        self.house_land_avg = house_land_avg
        self.house_avg = house_avg
        self.land_avg = land_avg

    def get_values_xy(self, par: list) -> dict:
        """Return a dictionary with the key as the name of the city, and the value is a list of tuples that store the x and y coorindates.

        Ensure that the order of year corresponds to the other of the intraprovincial values; and that their lengths are the same."""
        d = {}
        lst = []
        for x in range(len(self.year)):
            temp = (self.year[x], par[x])
            lst.append(temp)
            d[self.name] = lst
        return d
