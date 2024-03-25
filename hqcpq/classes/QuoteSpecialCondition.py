from hqcpq.db.SQLiteUtil import SQLiteConnection


class QuoteSpecialCondition:
    def __init__(self, obj_id: int, quote_id: int, special_condition_id: int):
        self.id = obj_id
        self.quote_id = quote_id
        self.special_condition_id = special_condition_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)})"

    def insert(self):
        query = "INSERT INTO quote_special_condition (quote_id, special_condition_id) VALUES (?, ?)"
        with SQLiteConnection() as cur:
            cur.execute(query, (self.quote_id, self.special_condition_id))
            self.id = cur.lastrowid
        return self

    def update(self):
        query = "UPDATE quote_special_condition SET quote_id = ?, special_condition_id = ? WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (self.quote_id, self.special_condition_id, self.id))
        return self

    @classmethod
    def delete(cls, obj_id):
        query = "DELETE FROM quote_special_condition WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (obj_id,))

    @classmethod
    def get(cls, obj_id):
        query = "SELECT * FROM quote_special_condition WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (obj_id,))
            row = cur.fetchone()
            if row:
                return cls(*row)
        return None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM quote_special_condition"
        with SQLiteConnection() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return {row[0]: cls(*row) for row in rows}

    @classmethod
    def get_by_quote(cls, quote_id):
        query = "SELECT * FROM quote_special_condition WHERE quote_id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (quote_id,))
            rows = cur.fetchall()
            return {row[0]: cls(*row) for row in rows}

    @classmethod
    def get_by_quote_and_special_condition(cls, quote_id, special_condition_id):
        query = "SELECT * FROM quote_special_condition WHERE quote_id = ? AND special_condition_id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (quote_id, special_condition_id))
            row = cur.fetchone()
            if row:
                return cls(*row)
            return None
