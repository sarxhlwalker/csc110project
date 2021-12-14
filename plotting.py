"""
CSC110: Final Project

This file contains functions that plot all of our data.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of professors and TAs
at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021 Sarah Walker, Manya Mittal, Sima Shmuylovich, and Grace Fung.
"""

from bokeh import plotting as plot
from bokeh import palettes
from classes import City
from classes import Province


def plot_migration(city: City) -> None:
    """
    Plots inter and intra values for one city as a line graph.
    """
    file_name = 'City_Plots/' + city.name + '_migration.html'
    plot.output_file(file_name)
    p = plot.figure(title=(city.name + ' migration'))
    colours = palettes.viridis(6)
    p.line(x=city.year, y=city.intraprovincial, line_color=colours[0],
           legend_label='Intraprovincial')
    p.line(x=city.year, y=city.interprovincial, line_color=colours[5],
           legend_label='Interprovincial')

    p.legend.location = "top_right"
    p.legend.click_policy = "hide"

    plot.save(p)


def plot_hpi(city: City) -> None:
    """
    Plots the three HPI values for one city as a bar graph.
    """
    file_name = 'City_Plots/' + city.name + '_hpi.html'
    plot.output_file(file_name)

    palette = palettes.viridis(6)
    colours = [palette[2], palette[3], palette[4]]

    y_axis = ['Total (house and land)', 'House only', 'Land only']

    data = {'years': ['2016', '2017', '2018', '2019', '2020'],
            'Total (house and land)': list(city.house_land_avg),
            'House only': list(city.house_avg),
            'Land only': list(city.land_avg)}

    p = plot.figure(x_range=[str(x) for x in city.year], title=(city.name + ' HPI'))
    p.vbar_stack(y_axis, x='years', width=0.9, source=data, fill_color=colours,
                 legend_label=list(y_axis))

    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"

    plot.save(p)


def plot_intraprovincial(province: Province, index: int) -> None:
    """
    Plots each city in province's intraprovincial values, contrasted by the province's COVID cases.

    Preconditions:
        - index != 0
    """
    file_name = 'Province_Plots/' + province.name + '_intraprovincial.html'
    plot.output_file(file_name)
    p = plot.figure(title=(province.name + ' intraprovincial'))
    colours = palettes.viridis(len(province.city_list) + 1)
    for x in range(len(province.city_list)):
        p.line(x=province.city_list[x].year, y=province.city_list[x].intraprovincial,
               legend_label=province.city_list[x].name,
               line_color=colours[x])

    covid_cases = divide_covid_cases(province.covid_cases, index)

    p.line(x=[2016, 2017, 2018, 2019, 2020], y=covid_cases,
           legend_label='COVID cases divided by ' + str(index),
           line_color=colours[len(province.city_list)])

    p.legend.location = 'top_left'
    p.legend.click_policy = 'hide'

    plot.save(p)


def plot_interprovincial(province: Province, index: int) -> None:
    """
    Plots each city in province's interprovincial values, contrasted by the province's COVID cases.

    Preconditions:
        - index != 0
    """
    file_name = 'Province_Plots/' + province.name + '_interprovincial.html'
    plot.output_file(file_name)
    p = plot.figure(title=(province.name + ' interprovincial'))
    colours = palettes.viridis(len(province.city_list) + 1)
    for x in range(len(province.city_list)):
        p.line(x=province.city_list[x].year, y=province.city_list[x].interprovincial,
               legend_label=province.city_list[x].name,
               line_color=colours[x])

    covid_cases = divide_covid_cases(province.covid_cases, index)

    p.line(x=[2016, 2017, 2018, 2019, 2020], y=covid_cases, legend_label='COVID cases divided by '
           + str(index), line_color=colours[len(province.city_list)])

    p.legend.location = 'top_left'
    p.legend.click_policy = 'hide'

    plot.save(p)


def plot_tot_hpi(province: Province, index: int) -> None:
    """
    Plots each city in province's total HPI values, contrasted with the province's COVID cases.

    Preconditions:
        - index != 0
    """
    file_name = 'Province_Plots/' + province.name + '_total_hpi.html'
    plot.output_file(file_name)
    colours = palettes.viridis(len(province.city_list) + 1)
    p = plot.figure(title=(province.name + ' total HPI'))

    for x in range(len(province.city_list)):
        p.line(x=province.city_list[x].year, y=province.city_list[x].house_land_avg,
               legend_label=province.city_list[x].name, line_color=colours[x])

    covid_cases = divide_covid_cases(province.covid_cases, index)

    p.line(x=[2016, 2017, 2018, 2019, 2020], y=covid_cases, legend_label='COVID cases divided by '
           + str(index), line_color=colours[len(province.city_list)])

    p.legend.location = "top_left"
    p.legend.click_policy = "hide"

    plot.save(p)


def plot_house_hpi(province: Province, index: int) -> None:
    """
    Plots each city in province's house HPI values, contrasted with the province's COVID cases.

    Preconditions:
        - index != 0
    """
    file_name = 'Province_Plots/' + province.name + '_house_hpi.html'
    plot.output_file(file_name)
    colours = palettes.viridis(len(province.city_list) + 1)
    p = plot.figure(title=(province.name + ' house HPI'))

    for x in range(len(province.city_list)):
        p.line(x=province.city_list[x].year, y=province.city_list[x].house_avg,
               legend_label=province.city_list[x].name, line_color=colours[x])

    covid_cases = divide_covid_cases(province.covid_cases, index)

    p.line(x=[2016, 2017, 2018, 2019, 2020], y=covid_cases, legend_label='COVID cases divided by '
           + str(index), line_color=colours[len(province.city_list)])

    p.legend.location = "top_left"
    p.legend.click_policy = "hide"

    plot.save(p)


def plot_land_hpi(province: Province, index: int) -> None:
    """
    Plots each city in province's land HPI values, contrasted with the province's COVID cases.

    Preconditions:
        - index != 0
    """
    file_name = 'Province_Plots/' + province.name + '_land_hpi.html'
    plot.output_file(file_name)
    colours = palettes.viridis(len(province.city_list) + 1)
    p = plot.figure(title=(province.name + ' land HPI'))

    for x in range(len(province.city_list)):
        p.line(x=province.city_list[x].year, y=province.city_list[x].land_avg,
               legend_label=province.city_list[x].name, line_color=colours[x])

    covid_cases = divide_covid_cases(province.covid_cases, index)

    p.line(x=[2016, 2017, 2018, 2019, 2020], y=covid_cases, legend_label='COVID cases divided by '
           + str(index), line_color=colours[len(province.city_list)])

    p.legend.location = "top_left"
    p.legend.click_policy = "hide"

    plot.save(p)


def divide_covid_cases(prov_cov_cases: list[int], index: int) -> list[int]:
    """
    Return a list of covid cases for a specific province that will match scale for another set of
    values for a graph.

    Preconditions:
        - index != 0
    """
    new_list = []
    for val in prov_cov_cases:
        new_list.append(val // index)
    return new_list


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
