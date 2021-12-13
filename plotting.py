import bokeh.plotting as plot
import bokeh.palettes as palettes
from bokeh.layouts import row


def plot_migration(city) -> plot.figure:
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

    return p


def plot_hpi(city) -> plot.figure:
    """
    Plots the three HPI values for one city as a bar graph.
    """
    file_name = 'City_Plots/' + city.name + '_hpi.html'
    plot.output_file(file_name)

    palette = palettes.viridis(6)
    colours = [palette[2], palette[3], palette[4]]

    y_axis = ['Total (house and land)', 'House only', 'Land only']

    data = {'years': ['2016', '2017', '2018', '2019', '2020'],
            'Total (house and land)': [x for x in city.house_land_avg],
            'House only': [x for x in city.house_avg],
            'Land only': [x for x in city.land_avg]}

    p = plot.figure(x_range=[str(x) for x in city.year], title=(city.name + ' HPI'))
    p.vbar_stack(y_axis, x='years', width=0.9, source=data, fill_color=colours,
                 legend_label=[x for x in y_axis])

    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"

    plot.save(p)

    return p


def plot_intraprovincial(province, index: int) -> plot.figure:
    """
    Plots each city in province's intraprovincial values, contrasted by the province's COVID cases.
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

    return p


def plot_interprovincial(province, index: int) -> plot.figure:
    """
    Plots each city in province's interprovincial values, contrasted by the province's COVID cases.
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
                                                                         + str(index),
           line_color=colours[len(province.city_list)])

    p.legend.location = 'top_left'
    p.legend.click_policy = 'hide'

    plot.save(p)

    return p


def plot_tot_hpi(province, index: int) -> plot.figure:
    """
    Plots each city in province's total HPI values, contrasted with the province's COVID cases.
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
                                                                                  + str(index),
           line_color=colours[len(province.city_list)])

    p.legend.location = "top_left"
    p.legend.click_policy = "hide"

    plot.save(p)

    return p


def plot_house_hpi(province, index: int) -> plot.figure:
    """
    Plots each city in province's house HPI values, contrasted with the province's COVID cases.
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
                                                                         + str(index),
           line_color=colours[len(province.city_list)])

    p.legend.location = "top_left"
    p.legend.click_policy = "hide"

    plot.save(p)

    return p


def plot_land_hpi(province, index: int) -> plot.figure:
    """
    Plots each city in province's land HPI values, contrasted with the province's COVID cases.
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
                                                                         + str(index),
           line_color=colours[len(province.city_list)])

    p.legend.location = "top_left"
    p.legend.click_policy = "hide"

    plot.save(p)

    return p


def divide_covid_cases(prov_cov_cases: list[int], index: int) -> list[int]:
    """
    Return a list of covid cases for a specific province that will match scale for another set of
    values for a graph.
    """
    new_list = []
    for val in prov_cov_cases:
        new_list.append(val // index)
    return new_list


def plot_all(city_migration: list, city_hpi: list, prov_inter: list, prov_intra: list,
             prov_hpi: list, prov_house: list, prov_land: list) -> None:
    """
    Collect all our plots into one HTML file.
    """
    list_all = city_migration + city_hpi + prov_inter + prov_intra + prov_hpi + prov_house + \
               prov_land
    plot.show(row([item for item in list_all]))



if __name__ == '__main__':
    pass
