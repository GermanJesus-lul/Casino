import json

config_json = {
    'local': False
}

with open('config.json', 'w') as f:
    json.dump(config_json, f)
