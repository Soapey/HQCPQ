from hqcpq.db.SQLiteUtil import SQLiteConnection


class ProductRate:
    def __init__(
        self, obj_id: int, product_id: int, rate_type_id: int, rate: float
    ):
        self.id = obj_id
        self.product_id = product_id
        self.rate_type_id = rate_type_id
        self.rate = rate

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)})"

    def insert(self):
        query = "INSERT INTO product_rate (product_id, rate_type_id, rate) VALUES (?, ?, ?)"
        with SQLiteConnection() as cur:
            cur.execute(query, (self.product_id, self.rate_type_id, self.rate))
            self.id = cur.lastrowid
        return self

    def update(self):
        query = "UPDATE product_rate SET product_id = ?, rate_type_id = ?, rate = ? WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (self.product_id, self.rate_type_id, self.rate, self.id))
        return self

    @classmethod
    def delete(cls, obj_id):
        query = "DELETE FROM product_rate WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (obj_id,))

    @classmethod
    def get(cls, obj_id):
        query = "SELECT * FROM product_rate WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (obj_id,))
            row = cur.fetchone()
            if row:
                return cls(*row)
        return None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM product_rate"
        with SQLiteConnection() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return {row[0]: cls(*row) for row in rows}
