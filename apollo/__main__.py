from interpreter import Interpreter
from settings import Settings
from dbaccess import DataAccess
from translator import Translator
from problem import ProblemManager

import os

__app_data__ = {
    'name': 'Apollo',
    'version': '0.0.1',
    'release_date': '2015-07-01',
    'description': 'Small source files manager (Homeworks, contests, etc...)',
    'author': 'Thyago Stall',
    'author_email': 'thstall@gmail.com',
    'url': 'https://github.com/thyagostall/apollo/',
    }


def get_settings_filename():
    return 'settings.ini'

def print_init_message():
    print(__app_data__['name'])
    print('Version:', __app_data__['version'], 'in', __app_data__['release_date'])
    print('Designed for Python 3')
    print('Current settings file:', get_settings_filename())
    print('')
    print('\'help\' to show all the commands available.')
    print('<command> --help or <command> -h to show specific help.')
    print('')

def main():
    settings = Settings(get_settings_filename())

    db = DataAccess(settings.get('db_path'))
    manager = ProblemManager(settings=settings, db=db)
    translator = Translator(manager)

    settings.translator = translator

    interpreter = Interpreter(settings=settings, database=db)

    print_init_message()
    interpreter.cmdloop('')

if __name__ == '__main__':
    main()
