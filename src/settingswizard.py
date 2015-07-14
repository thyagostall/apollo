import os
import configparser


def checkconfigfile(filename):
    if not os.path.isfile(filename):
        wizard(filename)


def _get_dbpath():
    print('Insert the database filename full path:')
    return input('>>> ')


def _get_repopath():
    print('Insert the problem repository full path:')
    return input('>>> ')


def _get_default_category():
    print('Insert the default category id:')
    return input('>>> ')


def _get_default_language():
    print('Insert the default language id:')
    return input('>>> ')


def wizard(filename):
    print('Using:', filename)
    print('No configuration file was found.')
    print('Set the configurations manually:')
    print('')

    config = configparser.ConfigParser()
    config.add_section('global')
    config.add_section('default')

    config.set('global', 'db_path', _get_dbpath())
    config.set('global', 'repo_path', _get_repopath())

    config.set('default', 'category', _get_default_category())
    config.set('default', 'language', _get_default_language())
    config.set('default', 'current_problem', '0|0')


    with open(filename, 'w') as configfile:
        config.write(configfile)

    print('')
    print('The configuration file was created successfully.')
    print('')
