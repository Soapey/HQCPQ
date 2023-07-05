from hqcpq.db.SQLiteUtil import SQLiteConnection


class VehicleCombination:
    def __init__(self, obj_id: int, name: str, net: float, charge_type: str):
        self.id = obj_id
        self.name = name
        self.net = net
        self.charge_type = charge_type

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)})"

    def insert(self):
        query = "INSERT INTO vehicle_combination (name, net, charge_type) VALUES (?, ?, ?)"
        with SQLiteConnection() as cur:
            cur.execute(query, (self.name, self.net, self.charge_type))
            self.id = cur.lastrowid
        return self

    def update(self):
        query = "UPDATE vehicle_combination SET name = ?, net = ?, charge_type = ? WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (self.name, self.net, self.charge_type, self.id))
        return self

    @classmethod
    def delete(cls, obj_id):
        query = "DELETE FROM vehicle_combination WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (obj_id,))

    @classmethod
    def get(cls, obj_id):
        query = "SELECT * FROM vehicle_combination WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (obj_id,))
            row = cur.fetchone()
            if row:
                return cls(*row)
        return None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM vehicle_combination"
        with SQLiteConnection() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return {row[0]: cls(*row) for row in rows}
