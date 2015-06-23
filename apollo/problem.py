class Data(object):
    def __init__(self, problem_id, name, category_id=None):
        self.problem_id = problem_id
        self.name = name
        self.category_id = category_id

class Files(object):
    def __init__(self, source_file, input_file, output_file):
        self.file_list = {'source': source_file, 'input': input_file, 'output': output_file}

class Problem(object):
    def __init__(self, data, files, status_id):
        self.data = data
        self.files = files
        self.status_id = status_id
