from app.db.config import get_cursor_type


class ProductRate:
    def __init__(
        self, id: int, product_id: int, rate_type_id: int, rate: float
    ) -> None:
        self.id = id
        self.product_id = product_id
        self.rate_type_id = rate_type_id
        self.rate = rate

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)})"

    def insert(self):

        with get_cursor_type() as cur:

            if not cur:
                return

            self.id = cur.execute(
                """
                INSERT INTO product_rate (product_id, rate_type_id, rate) 
                OUTPUT INSERTED.id
                VALUES (?, ?, ?);
                """,
                [self.product_id, self.rate_type_id, self.rate],
            ).fetchone()[0]

    def update(self):

        with get_cursor_type() as cur:

            if not cur:
                return

            cur.execute(
                """
                UPDATE product_rate 
                SET product_id = ?, rate_type_id = ?, rate = ? 
                WHERE id = ?;
                """,
                [self.product_id, self.rate_type_id, self.rate, self.id],
            )

    def delete(self):

        with get_cursor_type() as cur:

            if not cur:
                return

            cur.execute(
                """
                DELETE FROM product_rate 
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
                    SELECT id, product_id, rate_type_id, rate 
                    FROM product_rate;
                    """
                ).fetchall()

            else:
                records = cur.execute(
                    """
                    SELECT id, product_id, rate_type_id, rate 
                    FROM product_rate 
                    WHERE id = ?;
                    """,
                    [id],
                ).fetchall()

        return {pr.id: pr for pr in [ProductRate(*r) for r in records]}
