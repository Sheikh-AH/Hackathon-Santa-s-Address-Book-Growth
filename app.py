
"""Application for growth in different metric for countries."""

from os import environ
from dotenv import load_dotenv
from flask import Flask, render_template

import pandas as pd

from population_reader import get_data_of_country, get_single_year_growth

app = Flask(__name__)


# Template Endpoints (HTML Pages)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/countries/<country_name>')
def country_page(country_name):
    data = get_data_of_country(country_name)
    growth = get_single_year_growth(data)

    return render_template('countries.html',
                           title=country_name,
                           labels=list(data["Year"]),
                           data=list(data["Population (historical)"]))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
