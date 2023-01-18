from db.SQLCursor import SQLCursor


class Product():

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({vars(self)})'

    def insert(self):

        with SQLCursor() as cur:
            cur.execute('INSERT INTO product (name) VALUES (?);', (self.name,))
            last_record = cur.execute('SELECT id FROM product WHERE ROWID = last_insert_rowid();').fetchall()
            self.id = last_record[0][0]

    def update(self):

        with SQLCursor() as cur:
            cur.execute('UPDATE product SET name = ? WHERE id = ?', (self.name, self.id,))

    def delete(self):

        with SQLCursor() as cur:
            cur.execute('DELETE FROM product WHERE id = ?', (self.id,))