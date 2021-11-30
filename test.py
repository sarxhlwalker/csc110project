import pandas as pd

def test(filename: str, lst: list[str]):
    file = pd.read_csv(filename, usecols=lst)
    return file


def sort_file(city_migration):
    lst = []
    keywords = {'Net interprovincial migration', 'Net intraprovincial migration'}
    for x in range(len(city_migration)):
        if city_migration.loc[x, 'Components of population growth'] in keywords:
            lst.append(city_migration.loc[x])
    return pd.DataFrame(lst)


def split_file(city_migration):
    inter = []
    intra = []



if __name__ == '__main__':
    print('hi')
