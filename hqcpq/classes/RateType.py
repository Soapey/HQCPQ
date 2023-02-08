from hqcpq.db.db import get_cursor_type


class RateType:
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
                INSERT INTO rate_type (name) 
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
                UPDATE rate_type 
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
                DELETE FROM rate_type 
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
                    FROM rate_type;
                    """
                ).fetchall()

            else:
                records = cur.execute(
                    """
                    SELECT id, name 
                    FROM rate_type 
                    WHERE id = ?;
                    """,
                    [id],
                ).fetchall()

        return {rt.id: rt for rt in [RateType(*r) for r in records]}
