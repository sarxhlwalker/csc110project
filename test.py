import pandas as pd

def test(filename: str, lst: list[str]):
    """
    Save only the desired columns in lst from filename as a DataFrame.

    Note: filename should have double backslashes in the path.
    """
    file = pd.read_csv(filename, usecols=lst)
    return file


def sort_file(city_migration):
    """
    WIP: generalizing sorting by row.
    """
    lst = []
    keywords = {'Net interprovincial migration', 'Net intraprovincial migration'}
    for x in range(len(city_migration)):
        if city_migration.loc[x, 'Components of population growth'] in keywords:
            lst.append(city_migration.loc[x])
    return pd.DataFrame(lst)


def split_file(city_migration):
    """
    Split city_migration data into two separate DataFrames; one for intraprovincial
        migration and the other for interprovincial.
    """
    inter = []
    intra = []



if __name__ == '__main__':
    print('hi')
