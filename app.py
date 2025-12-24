"""Application for growth in different metric for countries."""

from os import environ as ENV
from dotenv import load_dotenv
import csv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from population_reader import (
    get_data_from_s3,
    get_data_of_country,
    get_single_year_growth,
    get_5year_avg
)

from country_info import country_info_main

app = Flask(__name__)

COUNTRIES = []

with open("resources/population.csv", "r") as file:
    reader = csv.DictReader(file)
    country = ""
    for row in reader:
        if row["Entity"] == country:
            continue
        country = row["Entity"]
        COUNTRIES.append(country)

# Template Endpoints (HTML Pages)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/countries/<country_name>')
def country_page(country_name):
    if country_name not in COUNTRIES:
        return redirect(url_for('not_found'))

    load_dotenv()
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


@app.route('/countries/search', methods=['POST'])
def search_country():
    '''Note: validation for search query is required.'''
    search_query = request.form.get('query').strip().lower()
    matches = []
    for country in COUNTRIES:
        if country.lower() == search_query:
            return redirect(url_for('country_page', country_name=country))
        if search_query in country.lower():
            matches.append(country)

    if len(matches) == 1:
        return redirect(url_for('country_page', country_name=matches[0]))

    if len(matches) > 1:
        error_message = "Multiple countries found: {}. Please be more specific.".format(
            ", ".join(matches))

    else:
        error_message = "Country '{}' not found. Please try again.".format(
            search_query)
    return render_template('not_found.html', error_message=error_message)


@app.route('/countries/not_found')
def not_found(error_message="The country you are looking for cannot be found."):
    return render_template('not_found.html', error_message=error_message)


if __name__ == "__main__":

    app.run(debug=True, host='0.0.0.0', port=5000)
