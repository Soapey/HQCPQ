from hqcpq.db.SQLiteUtil import SQLiteConnection


class SpecialCondition:
    def __init__(self, obj_id: int, name: str, message: str, is_default: int):
        self.id = obj_id
        self.name = name
        self.message = message
        self.is_default = is_default

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)})"

    def insert(self):
        query = "INSERT INTO special_condition (name, message, is_default) VALUES (?, ?)"
        with SQLiteConnection() as cur:
            cur.execute(query, (self.name, self.message, self.is_default))
            self.id = cur.lastrowid
        return self

    def update(self):
        query = "UPDATE special_condition SET name = ?, message = ?, is_default = ? WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (self.name, self.message, self.is_default, self.id))
        return self

    @classmethod
    def delete(cls, obj_id):
        query = "DELETE FROM special_condition WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (obj_id,))

    @classmethod
    def get(cls, obj_id):
        query = "SELECT * FROM special_condition WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (obj_id,))
            row = cur.fetchone()
            if row:
                return cls(*row)
        return None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM special_condition"
        with SQLiteConnection() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return {row[0]: cls(*row) for row in rows}

    @classmethod
    def get_all_defaults(cls):
        query = "SELECT * FROM special_condition WHERE is_default = 1"
        with SQLiteConnection() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return {row[0]: cls(*row) for row in rows}
