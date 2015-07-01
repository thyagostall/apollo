from settings import SettingTranslator
from problem import Language


class Translator(SettingTranslator):
    def __init__(self, problem_mananager):
        self.problem_mananager = problem_mananager
        self.functions = {
            'problem': (self.get_problem, self.set_problem),
            'language': (self.get_language, self.set_language)
            }

    def get_problem(self, string):
        if string == '0|0':
            return None
        else:
            manager = self.problem_mananager
            problem_id, attempt_no = string.split('|')
            problem_id = int(problem_id)
            attempt_no = int(attempt_no)

            problem = manager.get_data(problem_id, attempt_no)
            return problem

    def set_problem(self, data):
        return '|'.join([str(data.problem_id), str(data.attempt_no)])

    def get_language(self, string):
        language = int(string)
        language = Language(language)
        return language

    def set_language(self, data):
        return str(data.value)

    def fromstring(self, name, value):
        function = self.functions[name][0]
        return function(value)

    def tostring(self, name, value):
        function = self.functions[name][1]
        return function(value)
