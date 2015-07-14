from abc import ABCMeta
from abc import abstractmethod

import configparser
import problem


_filename = None
_settings = {}


def _string_to_raw(name, value):
    if name == 'current_problem':
        if value == '0|0':
            return None
        else:
            problem_id, attempt_no = value.split('|')
            problem_id = int(problem_id)
            attempt_no = int(attempt_no)

            manager = problem.ProblemManager()
            return manager.get_data(problem_id, attempt_no)
    elif name == 'language':
        return problem.Language(int(value))
    else:
        return str(value)


def _raw_to_string(name, value):
    if name == 'current_problem':
        if value == None:
            return '0|0'
        else:
            return '|'.join([str(value.problem_id), str(value.attempt_no)])
    elif name == 'language':
        return str(value.value)
    else:
        return str(value)


def load():
    config = configparser.ConfigParser()
    config.read(_filename)

    _settings['db_path'] = config['global']['db_path']
    _settings['repo_path'] = config['global']['repo_path']

    _settings['language'] = config['default']['language']
    _settings['category'] = config['default']['category']
    _settings['current_problem'] = config['default']['current_problem']


def save():
    config = configparser.ConfigParser()
    config.read(_filename)

    config['global']['db_path'] = _settings['db_path']
    config['global']['repo_path'] = _settings['repo_path']

    config['default']['language'] = _settings['language']
    config['default']['category'] = _settings['category']
    config['default']['current_problem'] = _settings['current_problem']

    with open(_filename, 'w') as f:
        config.write(f)


def get(name, refresh=True):
    if refresh:
        load()

    return _string_to_raw(name, _settings[name])


def set(name, value, refresh=True):
    _settings[name] = _raw_to_string(name, value)

    if refresh:
        save()
