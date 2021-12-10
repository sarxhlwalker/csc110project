from bokeh.plotting import figure, output_file, show
import main
import classes

def plot_intra(city: classes.City, city_name: str, w: int, h: int):
    output_file('line.html')
    p = figure(title=city_name, width=w, height=h)
    p.line(x=city.year, y=city.intraprovincial)
    show(p)

if __name__ == '__main__':
    pass
