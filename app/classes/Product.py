from app.db.SQLCursor import SQLCursor


class Product:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)})"

    def insert(self):

        with SQLCursor() as cur:

            if not cur:
                return

            cur.execute(
                """
                INSERT INTO product (name) 
                VALUES (?);""",
                (self.name,),
            )
            last_record = cur.execute(
                "SELECT id FROM product WHERE ROWID = last_insert_rowid();"
            ).fetchall()
            self.id = last_record[0][0]

    def update(self):

        with SQLCursor() as cur:

            if not cur:
                return

            cur.execute(
                """
                UPDATE product 
                SET name = ? 
                WHERE id = ?;""",
                (
                    self.name,
                    self.id,
                ),
            )

    def delete(self):

        with SQLCursor() as cur:

            if not cur:
                return

            cur.execute(
                """
                DELETE FROM product 
                WHERE id = ?;""",
                (self.id,),
            )

    @classmethod
    def get(cls, id: int = None) -> list:

        records = list()

        with SQLCursor() as cur:

            if not cur:
                return list()

            if not id:
                records = cur.execute(
                    """
                    SELECT id, name 
                    FROM product;"""
                ).fetchall()
            else:
                records = cur.execute(
                    """
                    SELECT id, name 
                    FROM product 
                    WHERE id = ?;""",
                    (id,),
                ).fetchall()

        return [Product(*r) for r in records]
