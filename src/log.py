from enum import Enum

import datetime
import dbaccess


class Action(Enum):
    PAUSE, FINISH, ARCHIVE, WORK, CREATE, DELETE = range(6)


class Log(object):
    def __init__(self, action, problem_id, name, category_id, dt=None):
        self.action = action
        self.problem_id = problem_id
        self.name = name
        self.category_id = category_id

        if dt:
            self.datetime = dt
        else:
            self.datetime = datetime.datetime.now()

    def __str__(self):
        return ' '.join([str(self.datetime), str(self.action), 'Problem:', str(self.problem_id), self.name, 'Cat:', str(self.category_id)])

class LogManager(object):
    def tolog(self, record):
        action = Action(int(record[0]))
        problem_id, name, category_id = record[1].split('|')
        dt = datetime.datetime.strptime(record[2], '%Y-%m-%dT%H:%M:%S.%f')

        result = Log(action, problem_id, name, category_id, dt)
        return result

    def torecord(self, log):
        action = log.action.value
        problem = '|'.join([str(log.problem_id), log.name, str(log.category_id)])
        dt = log.datetime.isoformat()

        return {'action': action, 'problem': problem, 'datetime': dt}

    def read(self):
        records = dbaccess.read('log')
        result = []

        for record in records:
            result.append(self.tolog(record))

        return result


    def insert(self, log):
        dbaccess.insert('log', self.torecord(log))


    def dump(self):
        dbaccess.delete('log')
