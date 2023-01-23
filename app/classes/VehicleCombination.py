from db.SQLCursor import SQLCursor


class VehicleCombination:
    def __init__(self, id: int, name: str, net: float) -> None:
        self.id = id
        self.name = name
        self.net = net

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)})"

    def insert(self):

        with SQLCursor() as cur:

            if not cur:
                return

            cur.execute(
                """
                INSERT INTO vehicle_combination (name, net) 
                VALUES (?, ?);""",
                (
                    self.name,
                    self.net,
                ),
            )
            last_record = cur.execute(
                "SELECT id FROM vehicle_combination WHERE ROWID = last_insert_rowid();"
            ).fetchall()
            self.id = last_record[0][0]

    def update(self):

        with SQLCursor() as cur:

            if not cur:
                return

            cur.execute(
                """
                UPDATE vehicle_combination 
                SET name = ?, net = ?  
                WHERE id = ?;""",
                (
                    self.name,
                    self.net,
                    self.id,
                ),
            )

    def delete(self):

        with SQLCursor() as cur:

            if not cur:
                return

            cur.execute(
                """
                DELETE FROM vehicle_combination 
                WHERE id = ?;""",
                (self.id,),
            )

    @classmethod
    def get(cls, id: int = None) -> list:

        records = list()

        with SQLCursor() as cur:

            if not cur:
                return list()

            if not id:
                records = cur.execute(
                    """
                    SELECT id, name, net 
                    FROM vehicle_combination;"""
                ).fetchall()
            else:
                records = cur.execute(
                    """
                    SELECT id, name, net 
                    FROM vehicle_combination 
                    WHERE id = ?;""",
                    (id,),
                ).fetchall()

        return [VehicleCombination(*r) for r in records]
