"""Application for growth in different metric for countries."""

from os import environ
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
