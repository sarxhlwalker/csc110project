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
    data = {'years': city.year, \
            2016: city.year[0], \
            2017: city.year[1], \
            2018: city.year[2], \
            2019: city.year[3], \
            2020: city.year[4]}

    # TODO: there is an issue with x_range.

    p = plotting.figure(x_range=city.year, height=250, title=(city.name + ' HPI'))
    p.vbar_stack(city.year, x='years', width=0.9, color=colours, source=data,
                 legend_label=city.year)

    # p.y_range.start = 0
    # p.x_range.range_padding = 0.1
    # p.xgrid.grid_line_color = None
    # p.axis.minor_tick_line_color = None
    # p.outline_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"

    plotting.show(p)


if __name__ == '__main__':
    pass
