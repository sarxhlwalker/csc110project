import bokeh.plotting as plotting
import bokeh.palettes as palettes
import main
import classes


def plot_migration(city) -> None:
    """
    Plots inter and intra values for one city as a line graph.
    """
    file_name = city.name + '_migration.html'
    plotting.output_file(file_name)
    p = plotting.figure(title=(city.name + ' migration'))
    colours = palettes.viridis(6)
    p.line(x=city.year, y=city.intraprovincial, line_color=colours[0], legend_label='Intraprovincial')
    p.line(x=city.year, y=city.interprovincial, line_color=colours[5], legend_label='Interprovincial')

    p.legend.location = "top_right"
    p.legend.click_policy = "hide"

    plotting.show(p)


def plot_hpi(city) -> None:
    """
    Plots the three HPI values for one city as a bar graph.
    """
    file_name = city.name + '_hpi.html'
    plotting.output_file(file_name)

    palette = palettes.viridis(6)
    colours = [palette[2], palette[3], palette[4]]

    y_axis = ['Total (house and land)', 'House only', 'Land only']

    data = {'years': ['2016', '2017', '2018', '2019', '2020'],
            'Total (house and land)': [x for x in city.house_land_avg],
            'House only': [x for x in city.house_avg],
            'Land only': [x for x in city.land_avg]}

    p = plotting.figure(x_range=[str(x) for x in city.year], title=(city.name + ' HPI'))
    p.vbar_stack(y_axis, x='years', width=0.9, source=data, fill_color=colours,
                 legend_label=[x for x in y_axis])

    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"

    plotting.show(p)


if __name__ == '__main__':
    pass
