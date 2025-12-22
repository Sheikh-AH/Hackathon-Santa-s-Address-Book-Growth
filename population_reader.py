'''file for reading and filtering population data'''
import pandas as pd


def remove_before_1900(frame: pd.DataFrame) -> pd.DataFrame:
    '''removes all data from a year before 1900'''
    return frame[frame["Year"] > 1900]


def get_data_of_country(frame: pd.DataFrame, country_name) -> pd.DataFrame:
    '''gets all rows associated with country'''
    return frame[frame["Entity"] == country_name]


if __name__ == "__main__":
    df = pd.read_csv("./resources/population.csv")
    df = remove_before_1900(df)
    print(get_data_of_country(df, "United Kingdom"))
