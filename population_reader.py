'''file for reading and filtering population data'''
import pandas as pd


def remove_before_1900(df: pd.DataFrame) -> None:
    '''removes all data from a year before 1900'''
    return df[df["Year"] > 1900]


def get_data_of_country(country_name: str) -> pd.DataFrame:
    '''gets all rows associated with country'''
    df = pd.read_csv("./resources/population.csv")
    df = remove_before_1900(df)
    return df[df["Entity"] == country_name]


def get_single_year_growth(df: pd.DataFrame) -> pd.DataFrame:
    """Provide summary statistics for growth."""
    last_year = df.iloc[-1]
    previous_year = df.iloc[-2]
    growth = last_year['Population (historical)'] - \
        previous_year['Population (historical)']
    return growth


def get_5year_avg(df: pd.DataFrame) -> pd.DataFrame:
    """Provide summary statistics for growth."""
    df = df.sort_values('Year').tail(6)
    df['Growth'] = df['Population (historical)'].diff()
    avg_growth = df['Growth'].iloc[1:].mean()

    return avg_growth


def get_maxmin_growth(df: pd.DataFrame):
    df = df.sort_values('Year')
    df['Growth'] = df['Population (historical)'].diff()
    max_year = df.loc[df['Growth'].idxmax()]['Year']
    max_growth = df.loc[df['Growth'].idxmax()]['Growth']
    min_year = df.loc[df['Growth'].idxmin()]['Year']
    min_growth = df.loc[df['Growth'].idxmin()]['Growth']
    return max_year, max_growth, min_year, min_growth


if __name__ == "__main__":
    df = get_data_of_country('China')
    a = get_5year_avg(df)
    maxy, maxg, miny, ming = get_maxmin_growth(df)
    print(maxy, maxg, miny, ming)
