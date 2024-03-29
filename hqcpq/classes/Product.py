from hqcpq.db.SQLiteUtil import SQLiteConnection


class Product:
    def __init__(self, obj_id: int, weighbridge_product_id: int, name: str):
        self.id = obj_id
        self.weighbridge_product_id = weighbridge_product_id
        self.name = name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)})"

    def insert(self):
        query = "INSERT INTO product (weighbridge_product_id, name) VALUES (?, ?)"
        with SQLiteConnection() as cur:
            cur.execute(query, (self.weighbridge_product_id, self.name))
            self.id = cur.lastrowid
        return self

    def update(self):
        query = "UPDATE product SET weighbridge_product_id = ?, name = ? WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (self.weighbridge_product_id, self.name, self.id))
        return self

    @classmethod
    def update_by_weighbridge_product_id(cls, name, weighbridge_product_id):
        query = "UPDATE product SET name = ? WHERE weighbridge_product_id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (name, weighbridge_product_id))

    @classmethod
    def get_by_weighbridge_product_id(cls, weighbridge_product_id):
        query = "SELECT * FROM product WHERE weighbridge_product_id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (weighbridge_product_id,))
            row = cur.fetchone()
            if row:
                return cls(*row)
        return None

    @classmethod
    def delete(cls, obj_id):
        query = "DELETE FROM product WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (obj_id,))

    @classmethod
    def get(cls, obj_id):
        query = "SELECT * FROM product WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (obj_id,))
            row = cur.fetchone()
            if row:
                return cls(*row)
        return None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM product"
        with SQLiteConnection() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return {row[0]: cls(*row) for row in rows}

    @classmethod
    def get_by_name(cls, name):
        query = "SELECT * FROM product WHERE name = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (name,))
            row = cur.fetchone()
            if row:
                return cls(*row)
        return None
