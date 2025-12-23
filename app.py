"""Application for growth in different metric for countries."""

from os import environ as ENV
from dotenv import load_dotenv
from flask import Flask, render_template

import pandas as pd

from population_reader import get_data_from_s3, get_data_of_country, get_single_year_growth, get_5year_avg
from country_info import country_info_main

app = Flask(__name__)


# Template Endpoints (HTML Pages)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/countries/<country_name>')
def country_page(country_name):
    Dataframes = get_data_from_s3(ENV)
    df_population = Dataframes['population']
    data = get_data_of_country(df_population, country_name)
    growth = get_single_year_growth(df_population, country_name)
    avg_growth = get_5year_avg(df_population, country_name)
    country_facts = country_info_main(country_name)

    return render_template('countries.html',
                           title=country_name,
                           labels=list(data["Year"]),
                           data=list(data["Population (historical)"]/1000000),
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

    load_dotenv()
    Dataframes = get_data_from_s3(ENV)
    df_population = Dataframes['population']

    app.run(debug=True, host='0.0.0.0', port=5000)
