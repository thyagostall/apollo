import sqlite3
import os

class DataAccess(object):
    def __init__(self, dbfile):
        self.connection = sqlite3.connect(dbfile)
        self.cursor = self.connection.cursor()


    def read(self, table, columns=None, where=None, order=None):
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

        result = [row for row in self.cursor.execute(*prepared)]
        return result

    def insert(self, table, data):
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

        self.cursor.execute(statement, list(data.values()))
        self.connection.commit()
    
    def update(self, table, data, where):
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

        self.cursor.execute(statement, params)
        self.connection.commit()

    def delete(self, table, where):
        where_columns = where.keys()

        statement = 'DELETE\n'
        statement += 'FROM\n'
        statement += table
        statement += '\n'

        statement += 'WHERE\n'
        statement += ' AND '.join([column + ' = ?' for column in where_columns])

        params = list(where.values())
        
        self.cursor.execute(statement, params)
        self.connection.commit()
