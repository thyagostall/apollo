import argparse
import category
import log
import problem
import subprocess
import tempfile

class Command(object):
    def __init__(self, settings, database):
        self.settings = settings
        self.database = database

        self.fill_properties()

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def parser(self):
        return self._parser

    def fill_properties(self):
        pass

    def execute(self, namespace):
        pass


class CreateCategoryCommand(Command):
    def fill_properties(self):
        self._name = 'create_category'
        self._description = 'Creates a category on the database'
        self._parser = \
        parser = argparse.ArgumentParser()
        parser.add_argument('name', type=str, help='name for the category (max 20 characters)')

    def execute(self, namespace):
        category_manager = category.CategoryManager(self.database)
        new_category = category.Category(namespace.name)

        category_manager.insert(new_category)
        print('Category inserted succesfully.')


class UpdateCategoryCommand(Command):
    def fill_properties(self):
        self._name = 'update_category'
        self._description = 'Updates a category from the database'
        self._parser = \
        parser = argparse.ArgumentParser()
        parser.add_argument('id', type=int, help='id of the existing category')
        parser.add_argument('name', type=str, help='new name for the category (max 20 characters)')

    def execute(self, namespace):
        category_manager = category.CategoryManager(self.database)
        cat = category_manager.get(namespace.id)
        cat.name = namespace.name
        category_manager.update(cat)
        print('Category updated succesfully.')


class DeleteCategoryCommand(Command):
    def fill_properties(self):
        self._name = 'delete_category'
        self._description = 'Deletes a category from the database'
        self._parser = \
        parser = argparse.ArgumentParser()
        parser.add_argument('id', type=int, help='id of the existing category')

    def execute(self, namespace):
        if self.settings.get('category_id') == namespace.id:
            print('The category is set as default. Set another category as default before delete it.')
            return

        category_manager = category.CategoryManager(self.database)
        cat = category_manager.get(namespace.id)
        category_manager.delete(cat)
        print('Category deleted succesfully.')


class SetDefaultCategoryCommand(Command):
    def fill_properties(self):
        self._name = 'set_default_category'
        self._description = 'Sets a category as default when creating new problems without category_id specified'
        self._parser = \
        parser = argparse.ArgumentParser()
        parser.add_argument('id', type=int, help='id of the existing category')

    def execute(self, namespace):
        category_manager = category.CategoryManager(self.database)
        cat = category_manager.get(namespace.id)
        self.settings.set('category_id', namespace.id)
        print('Category id set default succesfully.')


class ShowCategoriesCommand(Command):
    def fill_properties(self):
        self._name = 'show_categories'
        self._description = 'Show all the categories on the database'
        self._parser = \
        parser = argparse.ArgumentParser()

    def execute(self, namespace):
        print('Not implemented yet. Coming up next.')


class CreateCommand(Command):
    def fill_properties(self):
        self._name = 'create'
        self._description = 'Create a new problem attempt'
        self._parser = \
        parser = argparse.ArgumentParser()
        parser.add_argument('id', type=int, help='problem id')
        parser.add_argument('-l', '--language', type=int, help='programming language (default is used)', metavar='language')
        parser.add_argument('-c', '--category', type=int, help='category for the problem (default is used)', metavar='category')

    def execute(self, namespace):
        problem_id = namespace.id
        category = namespace.category if namespace.category else self.settings.get('category_id')

        if namespace.language:
            language = problem.Language(namespace.language)
        else:
            language = self.settings.get('language')

        manager = problem.ProblemManager(settings=self.settings, db=self.database)

        p = manager.get_data_for_new(problem_id, language)
        manager.create_files(p)
        manager.create_data(p)

        current_problem = self.settings.get('current_problem')
        if current_problem:
            manager.set_status(problem.Status.PAUSED, current_problem)

        manager.set_status(problem.Status.WORKING, p)
        self.settings.set('current_problem', p)

        l = log.Log(log.Action.CREATE, p.problem_id, p.name, p.category_id)
        lm = log.LogManager(self.database)
        lm.insert(l)
        print(l)


class PauseCommand(Command):
    def fill_properties(self):
        self._name = 'pause'
        self._description = 'Mark a problem attempt as paused'
        self._parser = \
        parser = argparse.ArgumentParser()
        parser.add_argument('id', type=int, help='problem id')
        parser.add_argument('-a', '--attempt', type=int, default=1, help='attempt # for the problem (default is 1)', metavar='attempt')

    def execute(self, namespace):
        problem_id = namespace.id
        attempt_no = namespace.attempt

        manager = problem.ProblemManager(settings=self.settings, db=self.database)

        p = manager.get_data(problem_id, attempt_no)
        manager.set_status(problem.Status.PAUSED, p)

        current_problem = self.settings.get('current_problem')
        if current_problem == p:
            current_problem = self.settings.set('current_problem', None)

        l = log.Log(log.Action.PAUSE, p.problem_id, p.name, p.category_id)
        lm = log.LogManager(self.database)
        lm.insert(l)
        print(l)


class FinishCommand(Command):
    def fill_properties(self):
        self._name = 'pause'
        self._description = 'Mark a problem attempt as finished'
        self._parser = \
        parser = argparse.ArgumentParser()
        parser.add_argument('id', type=int, help='problem id')
        parser.add_argument('-a', '--attempt', type=int, default=1, help='attempt # for the problem (default is 1)', metavar='attempt')

    def execute(self, namespace):
        problem_id = namespace.id
        attempt_no = namespace.attempt

        manager = problem.ProblemManager(settings=self.settings, db=self.database)

        current_problem = self.settings.get('current_problem')
        if current_problem == p:
            current_problem = self.settings.set('current_problem', None)

        p = manager.get_data(problem_id, attempt_no)
        manager.set_status(problem.Status.FINISHED, p)

        l = log.Log(log.Action.PAUSE, p.problem_id, p.name, p.category_id)
        lm = log.LogManager(self.database)
        lm.insert(l)
        print(l)


class ArchiveCommand(Command):
    def fill_properties(self):
        self._name = 'pause'
        self._description = 'Archive a problem attempt'
        self._parser = \
        parser = argparse.ArgumentParser()
        parser.add_argument('id', type=int, help='problem id')
        parser.add_argument('-a', '--attempt', type=int, default=1, help='attempt # for the problem (default is 1)', metavar='attempt')

    def execute(self, namespace):
        problem_id = namespace.id
        attempt_no = namespace.attempt

        manager = problem.ProblemManager(settings=self.settings, db=self.database)

        p = manager.get_data(problem_id, attempt_no)
        manager.set_status(problem.Status.ARCHIVED, p)

        current_problem = self.settings.get('current_problem')
        if current_problem == p:
            current_problem = self.settings.set('current_problem', None)

        l = log.Log(log.Action.PAUSE, p.problem_id, p.name, p.category_id)
        lm = log.LogManager(self.database)
        lm.insert(l)
        print(l)


class DeleteCommand(Command):
    def fill_properties(self):
        self._name = 'delete'
        self._description = 'Delete a problem attempt'
        self._parser = \
        parser = argparse.ArgumentParser()
        parser.add_argument('id', type=int, help='problem id')
        parser.add_argument('attempt', type=int, help='attempt # for the problem', metavar='attempt')

    def execute(self, namespace):
        problem_id = namespace.id
        attempt_no = namespace.attempt

        manager = problem.ProblemManager(settings=self.settings, db=self.database)

        p = manager.get_data(problem_id, attempt_no)
        manager.delete_files(p)
        manager.delete_data(p)

        current_problem = self.settings.get('current_problem')
        if current_problem == p:
            self.settings.set('current_problem', None)

        l = log.Log(log.Action.DELETE, p.problem_id, p.name, p.category_id)
        lm = log.LogManager(self.database)
        lm.insert(l)
        print(l)


class CommitCommand(Command):
    def fill_properties(self):
        self._name = 'commit'
        self._description = 'Commit to the repository the problem attempt'
        self._parser = \
        parser = argparse.ArgumentParser()

    def execute(self, namespace):
        lm = log.LogManager(self.database)
        logs = lm.read()

        message = '\n'.join([str(log_line) for log_line in logs])
        message = 'Items modified:\n'

        subprocess.call(['git', 'add', '.'])
        subprocess.call(['git', 'commit', '-m', message])


class WorkCommand(Command):
    def fill_properties(self):
        self._name = 'work'
        self._description = 'Work on a problem attempt and set it as current'
        self._parser = \
        parser = argparse.ArgumentParser()
        parser.add_argument('id', type=int, help='problem id')
        parser.add_argument('-a', '--attempt', type=int, default=1, help='attempt # for the problem (default is 1)', metavar='attempt')

    def execute(self, namespace):
        problem_id = namespace.id
        attempt_no = namespace.attempt

        manager = problem.ProblemManager(settings=self.settings, db=self.database)

        p = manager.get_data(problem_id, attempt_no)

        current_problem = self.settings.get('current_problem')
        if current_problem:
            manager.set_status(problem.Status.PAUSED, current_problem)

        if current_problem != p:
            manager.set_status(problem.Status.WORKING, p)
            self.settings.set('current_problem', p)

        l = log.Log(log.Action.WORK, p.problem_id, p.name, p.category_id)
        lm = log.LogManager(self.database)
        lm.insert(l)
        print(l)
