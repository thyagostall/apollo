from enum import Enum
from collections import namedtuple

import settings
import filemanager
import os
import webinterface

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
    def __init__(self, problem_id, name, category=None):
        self.problem_id = problem_id
        self.name = name
        self.category = category

        self.language = None
        self.attempt_no = None
        self.status = None

        self.source_file = None
        self.input_file = None
        self.output_file = None

class ProblemNotFound(Exception):
    pass

class ProblemManager(object):
    current_problem = None

    def __init__(self, db, settings):
        self.db = db
        self.settings = settings

    def __get_problem_from_db(self, problem_id):
        result = self.db.read('problem', where={'id': problem_id})
        result = result[0]

        if result:
            problem = ProblemData(result[0], result[1], result[2])
            return problem
        else:
            return None

    def create_files(self, problem):
        path = os.path.join(self.settings.repo_path, Status.get_directory(problem.status))

        filemanager.create_file(problem.source_file, path)
        filemanager.create_file(problem.input_file, path)
        filemanager.create_file(problem.output_file, path)

    def create_data(self, problem):
        result = self.db.read('problem', where={'id': problem.problem_id})

        if not result:
            self.db.insert('problem', data={'id': problem.problem_id,
                'name': problem.name})

        result = self.db.read('problem_attempt', where={'problem_id': problem.problem_id})
        attempt_no = len(result)
        attempt_no += 1

        self.db.insert('problem_attempt',
                data={'problem_id': problem.problem_id, 'attempt_no': attempt_no,
                    'language_id': problem.language.value, 'status_id': problem.status.value})

    def delete_files(self, problem):
        path = os.path.join(self.settings.repo_path, Status.get_directory(problem.status))

        filemanager.delete_file(problem.source_file, path)
        filemanager.delete_file(problem.input_file, path)
        filemanager.delete_file(problem.output_file, path)

    def delete_data(self, problem):
        self.db.delete('problem_attempt',
                where={'problem_id': problem.problem_id,
                    'attempt_no': problem.attempt_no})

        result = self.db.read('problem_attempt',
                where={'problem_id': problem.problem_id})
        if not result:
            self.db.delete('problem', where={'id': problem.problem_id})

    def set_status(self, status, problem):
        src_dir = Status.get_directory(problem.status)
        src_dir = os.path.join(self.settings.repo_path, src_dir)

        problem.status = status
        dest_dir = Status.get_directory(problem.status)
        dest_dir = os.path.join(self.settings.repo_path, dest_dir)

        filemanager.move_file(problem.source_file, src_dir, dest_dir)
        filemanager.move_file(problem.input_file, src_dir, dest_dir)
        filemanager.move_file(problem.output_file, src_dir, dest_dir)

        self.db.update(
                'problem_attempt',
                data={'status_id': problem.status.value},
                where={'problem_id': problem.problem_id,
                    'attempt_no': problem.attempt_no})

    def get_data_for_new(self, problem_id, language):
        problem = self.__get_problem_from_db(problem_id)

        if not problem:
            name = webinterface.get_problem_name(problem_id)
            problem = ProblemData(problem_id, name, None)

        problem.language = language

        result = self.db.read('problem_attempt', where={'problem_id': problem_id})
        problem.attempt_no = len(result) + 1
        problem.status = Status.TEMPORARY

        prefix = str(problem_id) + '.'
        problem.source_file = prefix + language_extensions[language]
        problem.input_file = prefix + 'in'
        problem.output_file = prefix + 'out'

        return problem

    def get_data(self, problem_id, attempt_no):
        problem = self.__get_problem_from_db(problem_id)

        result = self.db.read('problem_attempt',
                columns=['status_id', 'language_id'],
                where={'problem_id': problem_id, 'attempt_no': attempt_no})

        if not result:
            message = ' '.join('Problem:', problem_id, 'was not found on the database.')
            raise ProblemNotFound(message)

        problem.attempt_no = attempt_no
        problem.status = Status(result[0][0])
        problem.language = Language(result[0][1])

        prefix = str(problem_id) + '.'
        problem.source_file = prefix + language_extensions[language]
        problem.input_file = prefix + 'in'
        problem.output_file = prefix + 'out'

        return problem
