from enum import Enum

import settings
import filemanager
import os

class ProblemStatus(Enum):
    Working, Paused, Finished, Archived = range(4)

    @staticmethod
    def get_directory(status):
        return status.name.lower()

class Data(object):
    def __init__(self, problem_id, name, category_id=None):
        self.problem_id = problem_id
        self.name = name
        self.category_id = category_id

class Files(object):
    def __init__(self, source_file, input_file, output_file):
        self.source_file = source_file
        self.input_file = input_file
        self.output_file = output_file

class Problem(object):
    def __init__(self, data, files, status):
        self.data = data
        self.files = files
        self.status = status

    def __move_files(self, src, dest):
        app_dir = settings.get_app_dir()

        src = os.path.join([app_dir, src])
        dest = os.path.join([app_dir, dest])

        filemanager.move_files(self.files.values(), src, dest)

    def set_status(self, status):
        if status == ProblemStatus.Working:
            set_current(self)

        self.__move_files(ProblemStatus.get_directory(self.status), status)
        self.status = status

    def create_files(self):
        self.status = ProblemStatus.Working

        app_dir = settings.get_app_dir()
        working_path = ProblemStatus.get_directory(self.status)

        working_path = os.path.join([app_dir, working_path])

        filemanager.create_files(self.files.values(), working_path)
