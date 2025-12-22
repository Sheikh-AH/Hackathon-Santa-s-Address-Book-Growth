"""Application for growth in different metric for countries."""

from os import environ
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

import pandas as pd

from population_reader import remove_before_1900, get_data_of_country

app = Flask(__name__)

df = pd.read_csv("./resources/population.csv")
all_countries = remove_before_1900(df)

# JSON Endpoints


# @app.route('/api/countries/<country_code>')
# def get_country(country_code):
#     # Get all data for specified country
#     country_data = all_countries[all_countries['code'] == country_code]
#     country_data = country_data.to_dict('records')

#     return country_data


# Template Endpoints (HTML Pages)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/countries/<country_name>')
def country_page(country_name):
    data = get_data_of_country(country_name)

    return render_template('countries.html',
                           title=country_name,
                           labels=list(data["Year"]),
                           data=list(data["Population (historical)"]))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
