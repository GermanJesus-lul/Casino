import json
from pathlib import Path

def load_config():
    config_file = Path(__file__).parent.resolve() / "config.json"
    with open(config_file, 'r') as f:
        return json.load(f)


def local():
    return load_config()['local']


def db_path():
    return load_config()['db_path']
