import argparse
import category
import log
import problem
import subprocess
import tempfile
import settings

class Command(object):
    def __init__(self):
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
        category_manager = category.CategoryManager()
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
        category_manager = category.CategoryManager()
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
        if settings.get('category') == namespace.id:
            print('The category is set as default. Set another category as default before delete it.')
            return

        category_manager = category.CategoryManager()
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
        category_manager = category.CategoryManager()
        cat = category_manager.get(namespace.id)
        settings.set('category', namespace.id)
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
        category = namespace.category if namespace.category else settings.get('category')

        if namespace.language:
            language = problem.Language(namespace.language)
        else:
            language = settings.get('language')

        manager = problem.ProblemManager()

        p = manager.get_data_for_new(problem_id, language)
        manager.create_files(p)
        manager.create_data(p)

        current_problem = settings.get('current_problem')
        if current_problem:
            manager.set_status(problem.Status.PAUSED, current_problem)

        manager.set_status(problem.Status.WORKING, p)
        settings.set('current_problem', p)

        l = log.Log(log.Action.CREATE, p.problem_id, p.name, p.category_id)
        lm = log.LogManager()
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

        manager = problem.ProblemManager()

        p = manager.get_data(problem_id, attempt_no)
        manager.set_status(problem.Status.PAUSED, p)

        current_problem = settings.get('current_problem')
        if current_problem == p:
            current_problem = settings.set('current_problem', None)

        l = log.Log(log.Action.PAUSE, p.problem_id, p.name, p.category_id)
        lm = log.LogManager()
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

        manager = problem.ProblemManager()
        p = manager.get_data(problem_id, attempt_no)

        current_problem = settings.get('current_problem')
        if current_problem == p:
            current_problem = settings.set('current_problem', None)

        manager.set_status(problem.Status.FINISHED, p)

        l = log.Log(log.Action.FINISH, p.problem_id, p.name, p.category_id)
        lm = log.LogManager()
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

        manager = problem.ProblemManager()

        p = manager.get_data(problem_id, attempt_no)
        manager.set_status(problem.Status.ARCHIVED, p)

        current_problem = settings.get('current_problem')
        if current_problem == p:
            current_problem = settings.set('current_problem', None)

        l = log.Log(log.Action.PAUSE, p.problem_id, p.name, p.category_id)
        lm = log.LogManager()
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

        manager = problem.ProblemManager()

        p = manager.get_data(problem_id, attempt_no)
        manager.delete_files(p)
        manager.delete_data(p)

        current_problem = settings.get('current_problem')
        if current_problem == p:
            settings.set('current_problem', None)

        l = log.Log(log.Action.DELETE, p.problem_id, p.name, p.category_id)
        lm = log.LogManager()
        lm.insert(l)
        print(l)


class CommitCommand(Command):
    def fill_properties(self):
        self._name = 'commit'
        self._description = 'Commit to the repository the problem attempt'
        self._parser = \
        parser = argparse.ArgumentParser()

    def execute(self, namespace):
        lm = log.LogManager()
        logs = lm.read()

        # message = '\n'.join([str(log_line) for log_line in logs])
        # message = 'Items modified:\n' + message

        subprocess.call(['git', 'add', '.'])
        # subprocess.call(['git', 'commit', '-m', '$"' + message + '"'])
        subprocess.call(['git', 'commit'])


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

        manager = problem.ProblemManager()

        p = manager.get_data(problem_id, attempt_no)

        current_problem = settings.get('current_problem')
        if current_problem:
            manager.set_status(problem.Status.PAUSED, current_problem)

        if current_problem != p:
            manager.set_status(problem.Status.WORKING, p)
            settings.set('current_problem', p)

        l = log.Log(log.Action.WORK, p.problem_id, p.name, p.category_id)
        lm = log.LogManager()
        lm.insert(l)
        print(l)
