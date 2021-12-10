import bokeh.plotting as plotting
import bokeh.palettes as palettes
import main
import classes

def plot(city: classes.City, city_name: str) -> None:
    """
    Plots all five values of city into one graph; x-axis is consistently the years.

    >>> st_john_mls = main.read_file('Data Sets/Housing Prices Dataset (MLS)/Seasonally Adjusted Saint John.csv', \
                 ['Date', 'Single_Family_Benchmark_SA'])
    >>> st_john_mls = main.cleans_nan(st_john_mls)
    >>> st_john_mls_list = main.condense_time_manya(st_john_mls, ['2015', '2016', '2017', \
                                                '2018', '2019'], 'Single_Family_Benchmark_SA')
    >>> year = [2016, 2017, 2018, 2019, 2020]

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

    >>> st_john = classes.City('Saint John', year, st_john_intra, st_john_inter, st_john_mls_list, \
                        house_only_list, land_only_list)

    >>> plot(st_john, 'Saint John')
    """
    file_name = city_name + '.html'
    plotting.output_file(file_name)
    p = plotting.figure(title=city_name)
    colours = palettes.viridis(5)
    p.line(x=city.year, y=city.intraprovincial, line_color=colours[0])
    p.line(x=city.year, y=city.interprovincial, line_color=colours[1])
    p.line(x=city.year, y=city.house_land_avg, line_color=colours[2])
    plotting.show(p)

#
# def condense_info(city: classes.City) -> list[list]:
#     """Condense aspects of city so that plot() can call multi_line."""
#     intra = [city.year, city.intraprovincial]
#     inter = [city.year, city.interprovincial]
#     hl_avg = [city.year, city.house_land_avg]
#     house = [city.year, city.house_avg]
#     land = [city.year, city.land_avg]
#     tot = [intra, inter, hl_avg, house, land]
#     return tot

if __name__ == '__main__':
    pass
