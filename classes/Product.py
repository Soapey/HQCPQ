from db.SQLCursor import SQLCursor
from db.config import builds


class Product():

    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({vars(self)})'

    def insert(self, build_name='production'):

        with SQLCursor(builds[build_name]) as cur:
            cur.execute('INSERT INTO product (name) VALUES (?);', (self.name,))
            last_record = cur.execute('SELECT id FROM product WHERE ROWID = last_insert_rowid();')
            print(last_record)
            self.id = last_record[0]

