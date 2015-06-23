import webinterface
import problem
import settings
import os

class DataManager(object):
    def __init__(self, data_access):
        self.data_access = data_access

    def get_problem_data(self, problem_id):
        problem_record = self.data_access.read('problem', where={'id': problem_id})
       
        if problem_record:
            problem_record = problem_record[0]
            problem_data = problem.Data(problem_id=problem_record[0], name=problem_record[1], category_id=problem_record[2])
        else:        
            name = webinterface.get_problem_name(problem_id)
            problem_data = problem.Data(problem_id, name)

            self.data_access.insert('problem', data={'id': problem_id, 'name': name})

        return problem_data

    def create_problem_attempt(self, problem_data, language_id):
        problem_id = problem_data.problem_id
        category_id = settings.get('working_status_id')

        attempt_no = len(self.data_access.read('problem_attempt', where={'problem_id': problem_id, 'language_id': language_id, 'status_id': status_id}))
        attempt_no += 1

        self.data_access.insert('problem_attempt', data={'problem_id': problem_id, 'language_id': language_id, 'status_id': status_id, 'attempt_no': attempt_no})

    def get_problem_attempt(self, problem_data, language_id, attempt_no=1):
        attempt_record = self.data_access.read('problem_attempt', columns=['status_id'], where={'problem_id': problem_data.problem_id, 'language_id': language_id, 'attempt_no': attempt_no})
        status_id = attempt_record[0][0]
        
        language_extension = self.data_access.read('language', columns=['extension'], where={'id': language_id})
        status_path = self.data_access.read('status', columns=['directory'], where={'id': status_id})

        language_extension = language_extension[0][0]
        status_path = status_path[0][0]

        file_prefix = ''.join([str(problem_data.problem_id), '.'])

        source_code_filename = os.path.join(status_path, file_prefix + language_extension)
        input_filename = os.path.join(status_path, file_prefix + 'in')
        output_filename = os.path.join(status_path, file_prefix + 'out')

        files = problem.Files(source_code_filename, input_filename, output_filename)

        return problem.Problem(problem_data, files, status_id)
