from hqcpq.db.SQLiteUtil import SQLiteConnection


class RateType:
    def __init__(self, obj_id: int, name: str):
        self.id = obj_id
        self.name = name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)})"

    def insert(self):
        query = "INSERT INTO rate_type (name) VALUES (?)"
        with SQLiteConnection() as cur:
            cur.execute(query, (self.name,))
            self.id = cur.lastrowid
        return self

    def update(self):
        query = "UPDATE rate_type SET name = ? WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (self.name, self.id))
        return self

    @classmethod
    def delete(cls, obj_id):
        query = "DELETE FROM rate_type WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (obj_id,))

    @classmethod
    def get(cls, obj_id):
        query = "SELECT * FROM rate_type WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (obj_id,))
            row = cur.fetchone()
            if row:
                return cls(*row)
        return None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM rate_type"
        with SQLiteConnection() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return {row[0]: cls(*row) for row in rows}
