__settings_data = {}

def get(name):
    return __settings_data[name]

def set(name, value):
    __settings_data[name] = value
