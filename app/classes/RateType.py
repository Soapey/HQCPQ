from app.db.SQLCursor import SQLCursor


class RateType:
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
                INSERT INTO rate_type (name) 
                VALUES (?);""",
                (self.name,),
            )
            last_record = cur.execute(
                "SELECT id FROM rate_type WHERE ROWID = last_insert_rowid();"
            ).fetchall()
            self.id = last_record[0][0]

    def update(self):

        with SQLCursor() as cur:

            if not cur:
                return

            cur.execute(
                """
                UPDATE rate_type 
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
                DELETE FROM rate_type 
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
                    FROM rate_type;"""
                ).fetchall()
            else:
                records = cur.execute(
                    """
                    SELECT id, name 
                    FROM rate_type 
                    WHERE id = ?;""",
                    (id,),
                ).fetchall()

        return [RateType(*r) for r in records]
