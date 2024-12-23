import configparser
from flask import make_response, request
from werkzeug.wrappers import Response
from dbconfig import app
import requests

def load_config():
    config = configparser.ConfigParser()
    config.read('data.ini')
    return config

config = load_config()

max_attempts = int(config['security']['max_attempts'])
