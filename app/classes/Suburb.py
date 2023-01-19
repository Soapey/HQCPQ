from db.SQLCursor import SQLCursor


class Suburb():

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({vars(self)})'

    def insert(self):

        with SQLCursor() as cur:
            cur.execute('''
                INSERT INTO suburb (name) 
                VALUES (?);''', 
                (self.name,))
            last_record = cur.execute('SELECT id FROM suburb WHERE ROWID = last_insert_rowid();').fetchall()
            self.id = last_record[0][0]

    def update(self):

        with SQLCursor() as cur:
            cur.execute('''
                UPDATE suburb 
                SET name = ? 
                WHERE id = ?;''', 
                (self.name, self.id,))

    def delete(self):

        with SQLCursor() as cur:
            cur.execute('''
                DELETE FROM suburb 
                WHERE id = ?;''', 
                (self.id,))

    @classmethod
    def get(id: int = None) -> list:

        records = list()

        with SQLCursor() as cur:

            if id:
                records = cur.execute('''
                    SELECT id, name 
                    FROM suburb;''').fetchall()
            else:
                records = cur.execute('''
                    SELECT id, name 
                    FROM suburb 
                    WHERE id = ?;''', 
                    (id,)).fetchall()
            
        return [Suburb(*r) for r in records]