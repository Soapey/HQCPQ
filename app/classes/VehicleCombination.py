from app.db.config import get_cursor_type


class VehicleCombination:
    def __init__(self, id: int, name: str, net: float, charge_type: str) -> None:
        self.id = id
        self.name = name
        self.net = net
        self.charge_type = charge_type

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)})"

    def insert(self):

        cur_type = get_cursor_type()

        with cur_type() as cur:

            if not cur:
                return

            self.id = cur.execute(
                """
                INSERT INTO vehicle_combination (name, net, charge_type) 
                OUTPUT INSERTED.id
                VALUES (?, ?, ?);
                """,
                [self.name, self.net, self.charge_type],
            ).fetchone()[0]

    def update(self):

        cur_type = get_cursor_type()

        with cur_type() as cur:

            if not cur:
                return

            cur.execute(
                """
                UPDATE vehicle_combination 
                SET name = ?, net = ?, charge_type = ?
                WHERE id = ?;
                """,
                [self.name, self.net, self.charge_type, self.id],
            )

    def delete(self):

        cur_type = get_cursor_type()

        with cur_type() as cur:

            if not cur:
                return

            cur.execute(
                """
                DELETE FROM vehicle_combination 
                WHERE id = ?;
                """,
                [self.id],
            )

    @classmethod
    def get(cls, id: int = None) -> dict:

        records: list[tuple] = None

        cur_type = get_cursor_type()

        with cur_type() as cur:

            if not cur:
                return dict()

            if not id:
                records = cur.execute(
                    """
                    SELECT id, name, net, charge_type 
                    FROM vehicle_combination;
                    """
                ).fetchall()

            else:
                records = cur.execute(
                    """
                    SELECT id, name, net, charge_type 
                    FROM vehicle_combination 
                    WHERE id = ?;
                    """,
                    [id],
                ).fetchall()

        return {vc.id: vc for vc in [VehicleCombination(*r) for r in records]}
