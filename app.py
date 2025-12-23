"""Application for growth in different metric for countries."""

from os import environ as ENV
from dotenv import load_dotenv
from flask import Flask, render_template

import pandas as pd

from population_reader import (get_data_from_s3, get_data_of_country, get_single_year_growth, get_5year_avg,
                               get_literacy_rate, get_access_to_electricity, get_access_to_internet, get_gdp_per_capita)
from country_info import country_info_main

app = Flask(__name__)


# Template Endpoints (HTML Pages)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/countries/<country_name>')
def country_page(country_name):
    load_dotenv()
    Dataframes = get_data_from_s3(ENV)
    df_population = Dataframes['population']
    df_literacy = Dataframes['literacy']
    df_electricity = Dataframes['electricity']
    df_internet = Dataframes['internet']
    df_gdp = Dataframes['gdp']

    electricity_access = get_access_to_electricity(
        df_electricity, country_name)

    data = get_data_of_country(df_population, country_name)
    growth = get_single_year_growth(df_population, country_name)
    avg_growth = get_5year_avg(df_population, country_name)
    country_facts = country_info_main(country_name)
    literacy_rate = get_literacy_rate(df_literacy, country_name)
    internet_access = get_access_to_internet(df_internet, country_name)
    gdp_per_capita = get_gdp_per_capita(df_gdp, country_name)

    return render_template('countries.html',
                           title=country_name,
                           population_info={
                               "title": "Population (historical)",
                               "labels": list(data["Year"]),
                               "data": list(data["Population (historical)"] / 1000000)
                           },
                           literacy_info={
                               "title": "Percentage of Literacy",
                               "labels": ["Literate", "Illiterate"],
                               "data": [literacy_rate, 100-literacy_rate]
                           },
                           electricity_info={
                               "title": "Percentage Access to Electricity",
                               "labels": ["With Access", "Without Access"],
                               "data": [electricity_access, 100-electricity_access]
                           },

                           internet_info={
                               "title": "Percentage Access to Internet",
                               "labels": ["With Access", "Without Access"],
                               "data": [internet_access, 100-internet_access]
                           },
                           income_info={
                               "title": "GDP per Capita (Last 5 Years)",
                               "labels": list(data["Year"].tail(5)),
                               "data": list(gdp_per_capita)
                           },

                           growth_stats=(growth, avg_growth),
                           area=country_facts.get('area', 'N/A'),
                           capital=country_facts.get(
                               'capital', 'N/A'),
                           languages=country_facts.get(
                               'languages', 'N/A'),
                           currencies=country_facts.get(
                               'currencies', 'N/A'),
                           timezones=country_facts.get(
                               'timezones', 'N/A'),
                           flag_png=country_facts.get(
                               'flag_png', 'N/A'),
                           flag_alt=country_facts.get(
                               'flag_alt', 'N/A')
                           )


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
