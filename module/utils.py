import json
import os

def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

def save_config(config):
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)

def get_save_directory():
    config = load_config()
    return os.path.expanduser(config.get("save_directory", "~/Downloads"))
