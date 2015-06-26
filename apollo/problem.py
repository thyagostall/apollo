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

class ProblemManager(object):
    current_problem = None

    def __init__(self, db, settings):
        self.db = db
        self.settings = settings

    def get_problem_from_db(self, problem_id):
        result = self.db.read('problem', where={'id': problem_id})

        if result:
            problem = ProblemData(result[0], problem[1], problem[2])
            return problem
        else:
            return None

    def get_problem_files(self, problem_id, language, status):
        base_dir = os.path.join(self.settings.repo_dir, Status.get_directory(status))

        result = {}
        result['source'] = os.path.join(base_dir, str(problem_id) + '.' + language_extensions[language])
        result['input'] = os.path.join(base_dir, str(problem_id) + '.in')
        result['output'] = os.path.join(base_dir, str(problem_id) + '.out')

        return result

    def create_files(self, problem):
        file_list = self.get_problem_files(problem.problem_id, problem.language, problem.status)
        file_list = file_list.values()

        filemanager.create_files(file_list)

    def create_data(self, problem):
        result = self.db.read('problem', where={'id': problem.problem_id})
        
        if not result:
            self.db.insert('problem', data={'name': problem.name, 'category': problem.category})

        result = self.db.read('problem_attempt', where={'id': problem.problem_id})
        attempt_no = len(result)
        attempt_no += 1

        self.db.insert('problem_attempt', 
                data={'problem_id': problem.problem_id, 'attempt_no': attempt_no, 
                    'language_id': problem.language, 'status_id': problem.status})

    def delete_files(self, problem):
        file_list = self.__get_problem_files(problem.problem_id, problem.language, problem.status)

        filemanager.delete_files(file_list)

    def delete_data(self, problem):
        self.db.delete('problem_attempt', 
                where={'problem_id': problem.problem_id, 'attempt_no': problem.attempt_no})

        result = self.db.read('problem_attempt', where={'problem_id': problem.problem_id})
        if not result:
            self.db.delete('problem', where={'problem_id': problem.problem_id})

    def set_status(self, status, problem):
        file_list = [problem.source_file, problem.input_file, problem.output_file]
        base_dir = settings.get_app_dir()

        src_dir = Status.get_directory(problem.status)
        src_dir = os.path.join([base_dir, src_dir])
        
        problem.status = status
        dest_dir = Status.get_directory(problem.status)
        dest_dir = os.path.join([base_dir, dest_dir])

        filemanager.move_files(file_list, src_dir, dest_dir)
        db.update(
                'problem_attempt', 
                data={'status_id': problem.status_id}, 
                where={'problem_id': problem.problem_id, 'attempt_no': problem.attempt_no})

    def get_data_for_new(self, problem_id, language):
        problem = self.get_problem_from_db(problem_id)

        if not problem:
            name = webinterface.get_problem_name(problem_id)
            problem = ProblemData(problem_id, name, None)

        problem.language = language

        result = self.db.read('problem_attempt', where={'problem_id': problem_id})
        problem.attempt_no = len(result) + 1
        problem.status = Status.TEMPORARY

        files = self.get_problem_files(problem, language, problem.status)
        problem.source_file = files['source']
        problem.input_file = files['input']
        problem.output_file = files['output']

        return problem

    def get_data(self, problem_id, language, attempt_no):
        problem = self.__get_problem_from_db(problem_id)

        result = self.db.read('problem_attempt', 
                columns=['status_id'],
                where={'problem_id': problem_id, 'language_id': language, 'attempt_no': attempt_no})

        problem.attempt_no = attempt_no
        problem.language = language
        problem.status = Status.get_status(result[0][0])
