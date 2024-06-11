import json

with open('config.json', 'r') as f:
    config_json = json.load(f)

config_json["local"] = False

with open('config.json', 'w') as f:
    json.dump(config_json, f)
