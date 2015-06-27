import configparser

class Settings(object):
    def __init__(self, configfile, func_lang, func_problem):
        self.configfile = configfile
        self.get_default_language = func_lang
        self.get_current_problem = func_problem

    def load(self):
        config = configparser.ConfigParser()
        config.read(self.configfile)

        self.repo_dir = config['defaults']['repo_dir']
        self.default_language = \
                self.get_default_language(config['defaults']['language'])
        self.current_problem = self.get_current_problem(config['current_problem']['id'],
                config['current_problem']['attempt_no'])
    
    def save(self):
        config = configparser.ConfigParser()
        config.read(self.configfile)

        config['defaults']['repo_dir'] = self.repo_dir
        config['defaults']['language'] = self.default_language.value
        
        config['current_problem']['problem_id'] = self.current_problem.problem_id
        config['current_problem']['attempt_no'] = self.current_problem.attempt_no
