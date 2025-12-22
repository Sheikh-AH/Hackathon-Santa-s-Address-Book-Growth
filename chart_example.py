from flask import Flask, render_template
import os

from population_reader import get_data_of_country

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './templates/')

app = Flask(__name__, template_path)


@app.route("/")
def index():
    country = "United Kingdom"
    data = get_data_of_country(country)
    return render_template('countries.html',
                           title=country,
                           labels=list(data["Year"]),
                           data=list(data["Population (historical)"]))


if __name__ == "__main__":
    app.run()
