from hqcpq.classes.Product import Product
from hqcpq.db.SQLiteUtil import SQLiteConnection


class ProductRate:
    def __init__(
        self, obj_id: int, weighbridge_product_rate_id: int, name: str, rate: float, product_id: int
    ):
        self.id = obj_id
        self.weighbridge_product_rate_id = weighbridge_product_rate_id
        self.name = name
        self.rate = rate
        self.product_id = product_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)})"

    def insert(self):
        query = "INSERT INTO product_rate (weighbridge_product_rate_id, name, rate, product_id) VALUES (?, ?, ?, ?)"
        with SQLiteConnection() as cur:
            cur.execute(query, (self.weighbridge_product_rate_id, self.name, self.rate, self.product_id))
            self.id = cur.lastrowid
        return self

    def update(self):
        query = "UPDATE product_rate SET weighbridge_product_rate_id = ?, name = ?, rate = ?, product_id = ? WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (self.weighbridge_product_rate_id, self.name, self.rate, self.product_id, self.id))
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

    @classmethod
    def get_by_product_id(cls, product_id):
        query = "SELECT * FROM product_rate WHERE product_id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (product_id,))
            rows = cur.fetchall()
            return {row[0]: cls(*row) for row in rows}

    @classmethod
    def get_by_productname_and_name(cls, product_name, name):
        product = Product.get_by_name(product_name)
        if not product:
            return None

        query = "SELECT * FROM product_rate WHERE product_id = ? AND name = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (product.id, name))
            row = cur.fetchone()
            if row:
                return cls(*row)
        return None

    @classmethod
    def update_by_weighbridge_product_rate_id(cls, name, rate, weighbridge_product_rate_id):
        query = "UPDATE product_rate SET name = ?, rate = ? WHERE weighbridge_product_rate_id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (name, rate, weighbridge_product_rate_id))


