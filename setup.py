import os
import json
import setuptools

STR_CONFIG_FILE = 'config.json'

config = {}

config_filename = os.path.join(os.path.dirname(__file__), STR_CONFIG_FILE)

with open(config_filename, 'r') as config_file:
    config = json.load(config_file)

setuptools.setup(**config)
