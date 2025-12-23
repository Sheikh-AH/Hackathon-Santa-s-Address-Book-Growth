"""Filtering and processing data"""

from os import environ as ENV, _Environ
from dotenv import load_dotenv
from boto3 import client
from mypy_boto3_s3.client import S3Client
import pandas as pd


def get_data_from_s3(config: _Environ) -> S3Client:
    """Create and return an S3 client."""
    s3_client = client(
        service_name="s3",
        aws_access_key_id=config["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"]
    )

    bucket = config["S3_BUCKET_NAME"]
    objects = s3_client.list_objects_v2(Bucket=bucket)

    dataframes = {}
    for obj in objects['Contents']:
        key = obj['Key']
        file_obj = s3_client.get_object(Bucket=bucket, Key=key)
        df_name = key.replace('.csv', '')
        dataframes[df_name] = pd.read_csv(file_obj['Body'])

    return dataframes


def get_data_of_country(df_pop: dict, country: str) -> pd.DataFrame:
    """Gets all rows associated with country."""
    df = df_pop[df_pop["Year"] >= 1900]
    return df[df["Entity"] == country]


def get_single_year_growth(df_pop: pd.DataFrame, country: str) -> pd.DataFrame:
    """Provide summary statistics for growth."""
    df = df_pop[df_pop['Entity'] == country]
    df = df.sort_values('Year').tail(2)
    print(df)
    last_year = df.iloc[-1]
    previous_year = df.iloc[-2]
    growth = last_year['Population (historical)'] - \
        previous_year['Population (historical)']

    return growth


def get_5year_avg(df_pop: pd.DataFrame, country: str) -> pd.DataFrame:
    """Provide summary statistics for growth."""
    df = df_pop[df_pop['Entity'] == country].sort_values('Year').tail(6)
    df['Growth'] = df['Population (historical)'].diff()
    avg_growth = df['Growth'].iloc[1:].mean()

    return avg_growth


def get_maxmin_growth(df_pop: pd.DataFrame, country):
    """Provide min/max growth stats for a country."""
    df = df_pop[df_pop['Entity'] == country].sort_values('Year')
    df['Growth'] = df['Population (historical)'].diff()

    max_year = df.loc[df['Growth'].idxmax()]['Year']
    max_growth = df.loc[df['Growth'].idxmax()]['Growth']
    min_year = df.loc[df['Growth'].idxmin()]['Year']
    min_growth = df.loc[df['Growth'].idxmin()]['Growth']

    return max_year, max_growth, min_year, min_growth


if __name__ == "__main__":
    load_dotenv()
    data = get_data_from_s3(ENV)
    df_pop = get_data_of_country(data['population'], 'China')
    a = get_5year_avg(df_pop, 'China')
    s = get_single_year_growth(df_pop, 'China')
    maxy, maxg, miny, ming = get_maxmin_growth(df_pop, 'China')
    print(maxy, maxg, miny, ming)
    print(a, s)
