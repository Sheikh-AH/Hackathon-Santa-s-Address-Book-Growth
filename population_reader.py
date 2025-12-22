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


def get_single_year_growth(country_name) -> pd.DataFrame:
    """Provide summary statistics for growth."""
    df = pd.read_csv("./resources/population.csv")
    df = remove_before_1900(df)
    df = df[df["Entity"] == country_name]
    last_year = df.iloc[-1]
    previous_year = df.iloc[-2]
    growth = last_year['Population (historical)'] - \
        previous_year['Population (historical)']
    return growth


def get_trend_growth(country_name) -> pd.DataFrame:
    """Provide summary statistics for growth."""
    df = pd.read_csv("./resources/population.csv")
    df = remove_before_1900(df)
    df = df[df["Entity"] == country_name].sort_values('Year').tail(6)
    df['growth'] = df['Population (historical)'].diff()
    avg_growth = df['growth'].iloc[1:].mean()
    return avg_growth


if __name__ == "__main__":
    pass
