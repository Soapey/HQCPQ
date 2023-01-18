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
            last_record = cur.execute('SELECT id FROM product WHERE ROWID = last_insert_rowid();').fetchall()
            self.id = last_record[0][0]

    def update(self, build_name='production'):

        with SQLCursor(builds[build_name]) as cur:
            cur.execute('UPDATE product SET name = ? WHERE id = ?', (self.name, self.id,))

    def delete(self, build_name='production'):

        with SQLCursor(builds[build_name]) as cur:
            cur.execute('DELETE FROM product WHERE id = ?', (self.id,))