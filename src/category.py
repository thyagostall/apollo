import dbaccess


class CategoryNotFound(Exception):
    pass


class Category(object):
    def __init__(self, name, id=None):
        self.category_id = id
        self.name = name


class CategoryManager(object):
    def insert(self, category):
        rowid = dbaccess.insert('category', data={'name': category.name})
        category.category_id = rowid


    def get(self, category_id):
        record = dbaccess.read('category', where={'id': category_id})

        if not record:
            raise CategoryNotFound()

        record = record[0]
        result = Category(id=record[0], name=record[1])
        return result


    def delete(self, category):
        dbaccess.delete('category', where={'id': category.category_id})


    def update(self, category):
        dbaccess.update('category', data={'name': category.name}, where={'id': category.category_id})
