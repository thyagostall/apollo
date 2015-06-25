from cmd import Cmd

import shlex

class Interpreter(Cmd):
    prompt = '>>> '

    def execute(self, class_name, args):
        args = shlex.split(args)

        command = class_name()
        parser = command.get_parser()

        try:
            namespace = parser.parse_args(args)
            command.execute(namespace)
        except SystemExit:
            pass 
    
        print('')
