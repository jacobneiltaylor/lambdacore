import os
import json
import setuptools

STR_README_FILE = 'README.md'
STR_CONFIG_FILE = 'config.json'

get_filename = lambda name: os.path.join(os.path.dirname(__file__), name)

config = {}

readme_filename = get_filename(STR_README_FILE)
config_filename = get_filename(STR_CONFIG_FILE)

with open(readme_filename, 'r') as readme_file:
    config['long_description'] = readme_file.read()

with open(config_filename, 'r') as config_file:
    config.update(json.load(config_file))

setuptools.setup(**config)
