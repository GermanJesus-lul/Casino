import json


def local():
    with open('config.json', 'r') as f:
        config = json.load(f)
        return config['local']


def db_path():
    with open('config.json', 'r') as f:
        config = json.load(f)
        return config['db_path']
