from cmd import Cmd

command_classes = {
        'create': None,
        'pause': None,
        'finish': None,
        'archive': None,
        'work': None,
        'delete': None,
        'commit': None
        }

command_descriptions = {
        'create': 'Creates a new instance for a problem',
        'pause': 'Mark a problem as paused',
        'finish': 'Mark a problem as finished',
        'archive': 'Mark a problem as archived',
        'work': 'Define the current problem',
        'delete': 'Delete a problem attempt',
        'commit': 'Commit to the git repository'
        }

class Interpreter(Cmd):
    prompt = '>>> '

    def do_foo(self, args):
        print('doing foo...')

    def help_foo(self):
        print('this is the foo\'s help')

    def do_help(self, args):
        if args:
            Cmd.do_help(self, args)
        else:
            print('The commands available are: (type help [command] to see detailed documentation for individual commands)\n')

            for command, description in command_descriptions.iteritems():
                print(command + ': ' + description)

            print('')

m = Interpreter()
m.cmdloop()

