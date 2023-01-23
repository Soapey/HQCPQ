from db.SQLCursor import SQLCursor


class SuburbCombinationCharge:
    def __init__(
        self, id: int, suburb_id: int, vehicle_combination_id: int, rate: float
    ) -> None:
        self.id = id
        self.suburb_id = suburb_id
        self.vehicle_combination_id = vehicle_combination_id
        self.rate = rate

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)})"

    def insert(self):

        with SQLCursor() as cur:

            if not cur:
                return

            cur.execute(
                """
                INSERT INTO suburb_combination_charge (suburb_id, vehicle_combination_id, rate) 
                VALUES (?, ?, ?);""",
                (
                    self.suburb_id,
                    self.vehicle_combination_id,
                    self.rate,
                ),
            )
            last_record = cur.execute(
                "SELECT id FROM suburb_combination_charge WHERE ROWID = last_insert_rowid();"
            ).fetchall()
            self.id = last_record[0][0]

    def update(self):

        with SQLCursor() as cur:

            if not cur:
                return

            cur.execute(
                """
                UPDATE suburb_combination_charge 
                SET suburb_id = ?, vehicle_combination_id = ?, rate = ?, 
                WHERE id = ?;""",
                (
                    self.suburb_id,
                    self.vehicle_combination_id,
                    self.rate,
                    self.id,
                ),
            )

    def delete(self):

        with SQLCursor() as cur:

            if not cur:
                return

            cur.execute(
                """
                DELETE FROM suburb_combination_charge 
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
                    SELECT id, suburb_id, vehicle_combination_id, rate 
                    FROM suburb;"""
                ).fetchall()
            else:
                records = cur.execute(
                    """
                    SELECT id, suburb_id, vehicle_combination_id, rate 
                    FROM suburb_combination_charge 
                    WHERE id = ?;""",
                    (id,),
                ).fetchall()

        return [SuburbCombinationCharge(*r) for r in records]
