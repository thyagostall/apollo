import sqlite3
import os
import settings


_connection = None
_cursor = None


def connect():
    global _connection
    global _cursor

    _connection = sqlite3.connect(settings.get('db_path'))
    _cursor = _connection.cursor()


def read(table, columns=None, where=None, order=None):
    statement = 'SELECT\n'
    if columns:
        statement += ', '.join(columns)
    else:
        statement += '*'
    statement += '\n'

    statement += 'FROM\n'
    statement += table
    statement += '\n'

    if where:
        statement += 'WHERE\n'
        statement += ' AND '.join([col + ' = :' + col for col in where])
        statement += '\n'

    if order:
        statement += 'ORDER BY\n'
        statement += ', '.join([col[0] + ' ' + col[1] for col in order])

    prepared = (statement, where) if where else (statement, )

    result = [row for row in _cursor.execute(*prepared)]
    return result


def insert(table, data):
    columns = data.keys()

    statement = 'INSERT INTO\n'
    statement += table
    statement += '\n'

    statement += '('
    statement += ', '.join(columns)
    statement += ')\n'

    statement += 'VALUES\n'
    statement += '('
    statement += ', '.join(['?'] * len(columns))
    statement += ')'

    _cursor.execute(statement, list(data.values()))
    _connection.commit()
    return _cursor.lastrowid


def update(table, data, where):
    data_columns = data.keys()
    where_columns = where.keys()

    statement = 'UPDATE\n'
    statement += table
    statement += '\n'

    statement += 'SET\n'
    statement += ', '.join([column + ' = ?' for column in data_columns])

    statement += 'WHERE\n'
    statement += ' AND '.join([column + ' = ?' for column in where_columns])

    params = list(data.values()) + list(where.values())

    _cursor.execute(statement, params)
    _connection.commit()


def delete(table, where=None):
    statement = 'DELETE\n'
    statement += 'FROM\n'
    statement += table
    statement += '\n'

    if where:
        where_columns = where.keys()

        statement += 'WHERE\n'
        statement += ' AND '.join([column + ' = ?' for column in where_columns])

        params = list(where.values())
    else:
        params = []

    _cursor.execute(statement, params)
    _connection.commit()
