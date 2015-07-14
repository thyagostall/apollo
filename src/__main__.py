from interpreter import Interpreter
from problem import ProblemManager

import os
import sys
import settings
import dbaccess

__app_data__ = {
    'name': 'Apollo',
    'version': '0.0.2',
    'release_date': '2015-07-09',
    'description': 'Small source files manager for UVa Online Judge',
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
    settings._filename = get_settings_filename()
    dbaccess.connect()
    interpreter = Interpreter()

    print_init_message()
    try:
        interpreter.cmdloop('')
    except KeyboardInterrupt:
        print('')
        sys.exit(0)

if __name__ == '__main__':
    main()
