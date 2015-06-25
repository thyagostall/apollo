from enum import Enum

import settings
import filemanager
import os

class ProblemStatus(Enum):
    Working, Paused, Finished, Archived, Temporary = range(5)

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

    def create_files(self, problem):
        file_list = [problem.source_file, problem.input_file, problem.output_file]
        base_dir = settings.get_app_dir()

        status_dir = ProblemStatus.get_directory(problem.status)
        base_dir = os.path.join([base_dir, status_dir])

        filemanager.create_files(file_list, base_dir)

    def create_data(self, problem):
        pass

    def delete_files(self, problem):
        pass

    def delete_data(self, problem):
        pass

    def set_status(self, status, problem):
        file_list = [problem.source_file, problem.input_file, problem.output_file]
        base_dir = settings.get_app_dir()

        src_dir = ProblemStatus.get_directory(problem.status)
        src_dir = os.path.join([base_dir, src_dir])
        
        problem.status = status
        dest_dir = ProblemStatus.get_directory(problem.status)
        dest_dir = os.path.join([base_dir, dest_dir])

        filemanager.move_files(file_list, src_dir, dest_dir)
        db.update('problem_attempt', data={'status_id': problem.status_id}, where={'problem_id': problem.problem_id, 'attempt_no': problem.attempt_no})
