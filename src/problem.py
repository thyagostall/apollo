from enum import Enum
from collections import namedtuple

import settings
import os
import dbaccess
import urllib.request
import ast
import shutil

def move_file(filename, src, dest):
    src = os.path.join(src, filename)
    dest = os.path.join(dest, filename)
    shutil.move(src, dest)

def create_file(filename, path):
    filename = os.path.join(path, filename)
    f = open(filename, 'w+')
    f.close()

def delete_file(filename, path):
    filename = os.path.join(path, filename)
    os.remove(filename)

def delete_directory(directory):
    os.rmdir(directory)

def get_problem_name(number):
    url = "http://uhunt.felix-halim.net/api/p/id/{0}".format(number)

    with urllib.request.urlopen(url) as response:
        result = response.read()
        result = ast.literal_eval(result.decode('utf-8'))
        result = result["title"]

    return result


class Language(Enum):
    C, CPP, JAVA, PYTHON = range(4)

language_extensions = {
        Language.C: 'c',
        Language.CPP: 'cpp',
        Language.JAVA: 'java',
        Language.PYTHON: 'py'}

class Status(Enum):
    TEMPORARY, WORKING, PAUSED, FINISHED, ARCHIVED = range(5)

    @staticmethod
    def get_directory(status):
        return status.name.lower()

class ProblemData(object):
    def __init__(self, problem_id, name, category_id=None):
        self.problem_id = problem_id
        self.name = name
        self.category_id = category_id

        self.language = None
        self.attempt_no = None
        self.status = None

        self.source_file = None
        self.input_file = None
        self.output_file = None

    def __eq__(self, other):
        if other:
            return self.problem_id == other.problem_id and self.attempt_no == other.attempt_no
        else:
            return False

    def __ne__(self, other):
        if other:
            return other and self.problem_id != other.problem_id or self.attempt_no != other.attempt_no
        else:
            return True

class ProblemNotFound(Exception):
    pass

class ProblemManager(object):
    def __get_problem_from_db(self, problem_id):
        result = dbaccess.read('problem', where={'id': problem_id})

        if result:
            result = result[0]
            problem = ProblemData(result[0], result[1], result[2])
            return problem
        else:
            return None

    def create_files(self, problem):
        path = os.path.join(settings.get('repo_path'), Status.get_directory(problem.status))

        create_file(problem.source_file, path)
        create_file(problem.input_file, path)
        create_file(problem.output_file, path)

    def create_data(self, problem):
        result = dbaccess.read('problem', where={'id': problem.problem_id})

        if not result:
            dbaccess.insert('problem', data={'id': problem.problem_id,
                'name': problem.name, 'category_id': problem.category_id})

        result = dbaccess.read('problem_attempt', where={'problem_id': problem.problem_id})
        attempt_no = len(result)
        attempt_no += 1

        dbaccess.insert('problem_attempt',
                data={'problem_id': problem.problem_id, 'attempt_no': attempt_no,
                    'language_id': problem.language.value, 'status_id': problem.status.value})

    def delete_files(self, problem):
        path = os.path.join(settings.get('repo_path'), Status.get_directory(problem.status))

        delete_file(problem.source_file, path)
        delete_file(problem.input_file, path)
        delete_file(problem.output_file, path)

    def delete_data(self, problem):
        dbaccess.delete('problem_attempt',
                where={'problem_id': problem.problem_id,
                    'attempt_no': problem.attempt_no})

        result = dbaccess.read('problem_attempt',
                where={'problem_id': problem.problem_id})
        if not result:
            dbaccess.delete('problem', where={'id': problem.problem_id})

    def set_status(self, status, problem):
        src_dir = Status.get_directory(problem.status)
        src_dir = os.path.join(settings.get('repo_path'), src_dir)

        problem.status = status
        dest_dir = Status.get_directory(problem.status)
        dest_dir = os.path.join(settings.get('repo_path'), dest_dir)

        move_file(problem.source_file, src_dir, dest_dir)
        move_file(problem.input_file, src_dir, dest_dir)
        move_file(problem.output_file, src_dir, dest_dir)

        dbaccess.update(
                'problem_attempt',
                data={'status_id': problem.status.value},
                where={'problem_id': problem.problem_id,
                    'attempt_no': problem.attempt_no})

    def get_data_for_new(self, problem_id, language):
        problem = self.__get_problem_from_db(problem_id)

        if not problem:
            name = get_problem_name(problem_id)
            problem = ProblemData(problem_id, name, None)

        problem.language = language

        result = dbaccess.read('problem_attempt', where={'problem_id': problem_id})
        problem.attempt_no = len(result) + 1
        problem.status = Status.TEMPORARY

        prefix = str(problem_id) + '.'
        problem.source_file = prefix + language_extensions[language]
        problem.input_file = prefix + 'in'
        problem.output_file = prefix + 'out'

        return problem

    def get_data(self, problem_id, attempt_no):
        problem = self.__get_problem_from_db(problem_id)

        result = dbaccess.read('problem_attempt',
                columns=['status_id', 'language_id'],
                where={'problem_id': problem_id, 'attempt_no': attempt_no})

        if not result:
            message = ' '.join(['Problem:', str(problem_id), 'was not found on the database.'])
            raise ProblemNotFound(message)

        problem.attempt_no = attempt_no
        problem.status = Status(result[0][0])
        problem.language = Language(result[0][1])

        prefix = str(problem_id) + '.'
        problem.source_file = prefix + language_extensions[problem.language]
        problem.input_file = prefix + 'in'
        problem.output_file = prefix + 'out'

        return problem


    def update_category(self, problem):
        dbaccess.update('problem', data={'category_id': problem.category_id}, where={'id': problem.problem_id})
