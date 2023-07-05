from hqcpq.db.SQLiteUtil import SQLiteConnection


class QuoteItem:
    def __init__(
        self,
        obj_id: int,
        quote_id: int,
        vehicle_combination_name: str,
        vehicle_combination_net: int,
        transport_rate_ex_gst: float,
        product_name: str,
        product_rate_ex_gst: float,
        charge_type_name: str,
    ):
        self.id = obj_id
        self.quote_id = quote_id
        self.vehicle_combination_name = vehicle_combination_name
        self.vehicle_combination_net = vehicle_combination_net
        self.transport_rate_ex_gst = transport_rate_ex_gst
        self.product_name = product_name
        self.product_rate_ex_gst = product_rate_ex_gst
        self.charge_type_name = charge_type_name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)})"

    def total_inc_gst(self):

        return 1.1 * (
            (self.transport_rate_ex_gst + self.product_rate_ex_gst)
            * self.vehicle_combination_net
        )

    def insert(self):
        query = "INSERT INTO quote_item (quote_id, vehicle_combination_name, vehicle_combination_net, " \
                "transport_rate_ex_gst, product_name, product_rate_ex_gst, charge_type_name) VALUES (?, ?, ?, ?, ?, " \
                "?, ?)"
        with SQLiteConnection() as cur:
            cur.execute(query, (
                self.quote_id,
                self.vehicle_combination_name,
                self.vehicle_combination_net,
                self.transport_rate_ex_gst,
                self.product_name,
                self.product_rate_ex_gst,
                self.charge_type_name
            ))
            self.id = cur.lastrowid
        return self

    def update(self):
        query = "UPDATE quote_item SET quote_id = ?, vehicle_combination_name = ?, vehicle_combination_net = ?, " \
                "transport_rate_ex_gst = ?, product_name = ?, product_rate_ex_gst = ?, charge_type_name = ? WHERE id " \
                "= ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (
                self.quote_id,
                self.vehicle_combination_name,
                self.vehicle_combination_net,
                self.transport_rate_ex_gst,
                self.product_name,
                self.product_rate_ex_gst,
                self.charge_type_name,
                self.id
            ))
        return self

    @classmethod
    def delete(cls, obj_id):
        query = "DELETE FROM quote_item WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (obj_id,))

    @classmethod
    def get(cls, obj_id):
        query = "SELECT * FROM quote_item WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (obj_id,))
            row = cur.fetchone()
            if row:
                return cls(*row)
        return None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM quote_item"
        with SQLiteConnection() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return {row[0]: cls(*row) for row in rows}

    @classmethod
    def get_all_by_quote_id(cls, quote_id):
        query = "SELECT * FROM quote_item WHERE quote_id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (quote_id,))
            rows = cur.fetchall()
            return {row[0]: cls(*row) for row in rows}
