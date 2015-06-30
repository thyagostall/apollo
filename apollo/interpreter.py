from cmd import Cmd

import shlex
import command

class Interpreter(Cmd):
    prompt = '>>> '

    def do_create_category(self, args):
        self.execute(command.CreateCategoryCommand, args)

    def help_create_category(self):
        self.do_create_category('--help')

    def do_update_category(self, args):
        self.execute(command.UpdateCategoryCommand, args)

    def help_update_category(self):
        self.do_update_category('--help')

    def do_delete_category(self, args):
        self.execute(command.DeleteCategoryCommand, args)

    def help_delete_category(self):
        self.do_delete_category('--help')

    def do_set_default_category(self, args):
        self.execute(command.SetDefaultCategoryCommand, args)

    def help_set_default_category(self):
        self.do_set_default_category('--help')

    def do_show_categories(self, args):
        self.execute(command.ShowCategoriesCommand, args)

    def help_show_categories(self):
        self.do_show_categories('--help')

    def do_create(self, args):
        self.execute(command.CreateCommand, args)

    def help_create(self):
        self.do_create('--help')

    def do_pause(self, args):
        self.execute(command.PauseCommand, args)

    def help_pause(self):
        self.do_pause('--help')

    def do_finish(self, args):
        self.execute(command.FinishCommand, args)

    def help_finish(self):
        self.do_finish('--help')

    def do_archive(self, args):
        self.execute(command.ArchiveCommand, args)

    def help_archive(self):
        self.do_archive('--help')

    def do_delete(self, args):
        self.execute(command.DeleteCommand, args)

    def help_delete(self):
        self.do_delete('--help')

    def do_commit(self, args):
        self.execute(command.CommitCommand, args)

    def help_commit(self):
        self.do_commit('--help')

    def execute(self, class_name, args):
        args = shlex.split(args)

        command = class_name()
        parser = command.parser
        parser.prog = command.name
        parser.description = command.description

        try:
            namespace = parser.parse_args(args)
            command.execute(namespace)
        except SystemExit:
            pass

        print('')
