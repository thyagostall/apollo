import json

__settings_data = {}

def load(filename):
    global __settings_data

    with open(filename, 'r') as settings_file:
        __settings_data = json.load(settings_file)

def save(filename):
    with open(filename, 'w') as settings_file:
        json.dump(__settings_data, settings_file)

def get(name):
    return __settings_data[name]

def set(name, value):
    __settings_data[name] = value
