'''file for reading and filtering population data'''
import pandas as pd


def remove_before_1900(df: pd.DataFrame) -> None:
    '''removes all data from a year before 1900'''
    return df[df["Year"] > 1900]


def get_data_of_country(country_name) -> pd.DataFrame:
    '''gets all rows associated with country'''
    df = pd.read_csv("./resources/population.csv")
    df = remove_before_1900(df)
    return df[df["Entity"] == country_name]


if __name__ == "__main__":
    pass
