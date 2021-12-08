import pandas as pd

def test(filename: str, lst: list[str]):
    """
    Save only the desired columns in lst from filename as a DataFrame.

    Note: filename should have double backslashes in the path.

    Generalization untested.
    """
    file = pd.read_csv(filename, usecols=lst)
    return file


def sort_file(dataframe, keywords: set[str], column: str):
    """
    Create and return a new DataFrame containing only rows whose specified column are a
        specific keyword.

    Ex. city_migration; keywords = {'Net interprovincial migration',
            'Net intraprovincial migration'}, column = 'Components of population growth'.

    Generalization untested.
    """
    lst = []
    for x in range(len(dataframe)):
        if dataframe.loc[x, column] in keywords:
            lst.append(dataframe.loc[x])
    return pd.DataFrame(lst)


def split_file(dataframe):
    """
    Split city_migration data into two separate DataFrames; one for intraprovincial
        migration and the other for interprovincial.
    """
    column = 'Components of population growth'
    inter = []
    intra = []
    for x in range(len(dataframe)):
        if dataframe.loc[x, column] == 'Net interprovincial migration':
            inter.append(dataframe.loc[x])
        else:
            intra.append(dataframe.loc[x])
    return inter, intra




if __name__ == '__main__':
    pass
