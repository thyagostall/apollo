import argparse

class Command(object):
    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def parser(self):
        return self._parser

    def execute(self, namespace):
        pass


class CreateCategoryCommand(Command):
    def __init__(self):
        self._name = 'create_category'
        self._description = 'Creates a category on the database'
        self._parser = \
        parser = argparse.ArgumentParser()
        parser.add_argument('name', type=str, help='name for the category (max 20 characters)')

    def execute(self, namespace):
        print('executed')


class UpdateCategoryCommand(Command):
    def __init__(self):
        self._name = 'update_category'
        self._description = 'Updates a category from the database'
        self._parser = \
        parser = argparse.ArgumentParser()
        parser.add_argument('id', type=int, help='id of the existing category')
        parser.add_argument('name', type=str, help='new name for the category (max 20 characters)')

    def execute(self, namespace):
        print('executed')


class DeleteCategoryCommand(Command):
    def __init__(self):
        self._name = 'delete_category'
        self._description = 'Deletes a category from the database'
        self._parser = \
        parser = argparse.ArgumentParser()
        parser.add_argument('id', type=int, help='id of the existing category')

    def execute(self, namespace):
        print('executed')


class SetDefaultCategoryCommand(Command):
    def __init__(self):
        self._name = 'set_default_category'
        self._description = 'Sets a category as default when creating new problems without category_id specified'
        self._parser = \
        parser = argparse.ArgumentParser()
        parser.add_argument('id', type=int, help='id of the existing category')

    def execute(self, namespace):
        print('executed')


class ShowCategoriesCommand(Command):
    def __init__(self):
        self._name = 'show_categories'
        self._description = 'Show all the categories on the database'
        self._parser = \
        parser = argparse.ArgumentParser()

    def execute(self, namespace):
        print('executed')


class CreateCommand(Command):
    def __init__(self):
        self._name = 'create'
        self._description = 'Create a new problem attempt'
        self._parser = \
        parser = argparse.ArgumentParser()
        parser.add_argument('id', type=int, help='problem id')
        parser.add_argument('-l', '--language', type=int, help='programming language (default is used)', metavar='language')
        parser.add_argument('-c', '--category', type=int, help='category for the problem (default is used)', metavar='category')

    def execute(self, namespace):
        print('executed')


class PauseCommand(Command):
    def __init__(self):
        self._name = 'pause'
        self._description = 'Mark a problem attempt as paused'
        self._parser = \
        parser = argparse.ArgumentParser()
        parser.add_argument('id', type=int, help='problem id')
        parser.add_argument('-a', '--attempt', type=int, default=1, help='attempt # for the problem (default is 1)', metavar='attempt')

    def execute(self, namespace):
        print('executed')


class FinishCommand(Command):
    def __init__(self):
        self._name = 'pause'
        self._description = 'Mark a problem attempt as finished'
        self._parser = \
        parser = argparse.ArgumentParser()
        parser.add_argument('id', type=int, help='problem id')
        parser.add_argument('-a', '--attempt', type=int, default=1, help='attempt # for the problem (default is 1)', metavar='attempt')

    def execute(self, namespace):
        print('executed')


class ArchiveCommand(Command):
    def __init__(self):
        self._name = 'pause'
        self._description = 'Archive a problem attempt'
        self._parser = \
        parser = argparse.ArgumentParser()
        parser.add_argument('id', type=int, help='problem id')
        parser.add_argument('-a', '--attempt', type=int, default=1, help='attempt # for the problem (default is 1)', metavar='attempt')

    def execute(self, namespace):
        print('executed')


class DeleteCommand(Command):
    def __init__(self):
        self._name = 'delete'
        self._description = 'Delete a problem attempt'
        self._parser = \
        parser = argparse.ArgumentParser()
        parser.add_argument('id', type=int, help='problem id')
        parser.add_argument('-a', '--attempt', type=int, default=1, help='attempt # for the problem (default is 1)', metavar='attempt')

    def execute(self, namespace):
        print('executed')


class CommitCommand(Command):
    def __init__(self):
        self._name = 'commit'
        self._description = 'Commit to the repository the problem attempt'
        self._parser = \
        parser = argparse.ArgumentParser()

    def execute(self, namespace):
        print('executed')
