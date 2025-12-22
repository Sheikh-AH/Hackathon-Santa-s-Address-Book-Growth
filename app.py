"""Application for growth in different metric for countries."""

from os import environ
from dotenv import load_dotenv  # Loads variables from a file into the environment
from flask import Flask, jsonify, render_template
