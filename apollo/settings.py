import configparser

class Settings(object):
    repo_dir = '/Users/thyago/Dropbox/Temp'
    
    def __init__(self, configfile):
        self.configfile = configfile
