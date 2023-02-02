from app.db.config import get_cursor_type


class Product:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)})"

    def insert(self):

        with get_cursor_type() as cur:

            if not cur:
                return

            self.id = cur.execute(
                """
                INSERT INTO product (name) 
                OUTPUT INSERTED.id
                VALUES (?);
                """,
                [self.name],
            ).fetchone()[0]

    def update(self):

        with get_cursor_type() as cur:

            if not cur:
                return

            cur.execute(
                """
                UPDATE product 
                SET name = ? 
                WHERE id = ?;
                """,
                [self.name, self.id],
            )

    def delete(self):

        with get_cursor_type() as cur:

            if not cur:
                return

            cur.execute(
                """
                DELETE FROM product 
                WHERE id = ?;
                """,
                [self.id],
            )

    @classmethod
    def get(cls, id: int = None) -> dict:

        records: list[tuple] = None

        with get_cursor_type() as cur:

            if not cur:
                return dict()

            if not id:
                records = cur.execute(
                    """
                    SELECT id, name 
                    FROM product;
                    """
                ).fetchall()

            else:
                records = cur.execute(
                    """
                    SELECT id, name 
                    FROM product 
                    WHERE id = ?;
                    """,
                    [id],
                ).fetchall()

        return {p.id: p for p in [Product(*r) for r in records]}
