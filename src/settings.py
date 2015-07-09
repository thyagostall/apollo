from abc import ABCMeta
from abc import abstractmethod

import configparser


class InvalidSettingName(Exception):
    pass


class TranslatorNotSet(Exception):
    pass


class SettingTranslator(metaclass=ABCMeta):
    @abstractmethod
    def fromstring(self, name, value):
        pass


    @abstractmethod
    def tostring(self, name, value):
        pass


class Settings(object):
    def __init__(self, filename, translator=None):
        self.filename = filename
        self.translator = translator
        self.settings = {}


    def get(self, name, refresh=True):
        if refresh:
            self.load()

        if name in self.settings:
            return self.settings[name]
        else:
            name_id = ''.join([name, '_id'])
            if name_id in self.settings:
                if self.translator:
                    self.settings[name] = self.translator.fromstring(name, self.settings[name_id])
                    return self.settings[name]
                else:
                    raise TranslatorNotSet()
            else:
                raise InvalidSettingName()


    def set(self, name, value, refresh=True):
        name_id = ''.join([name, '_id'])
        if name_id in self.settings:
            if self.translator:
                self.settings[name_id] = self.translator.tostring(name, value)
            else:
                raise TranslatorNotSet()

        self.settings[name] = value

        if refresh:
            self.save()


    def load(self):
        config = configparser.ConfigParser()
        config.read(self.filename)
        sets = self.settings

        sets['db_path'] = config['global']['db_path']
        sets['repo_path'] = config['global']['repo_path']

        sets['language_id'] = config['defaults']['language_id']
        sets['category_id'] = config['defaults']['category_id']

        sets['current_problem_id'] = config['current_problem']['id_attempt']


    def save(self):
        config = configparser.ConfigParser()
        config.read(self.filename)
        sets = self.settings

        config['global']['db_path'] = sets['db_path']
        config['global']['repo_path'] = sets['repo_path']

        config['defaults']['language_id'] = sets['language_id']
        config['defaults']['category_id'] = sets['category_id']

        config['current_problem']['id_attempt'] = sets['current_problem_id']

        with open(self.filename, 'w') as f:
            config.write(f)
