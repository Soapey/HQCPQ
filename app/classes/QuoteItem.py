from app.db.config import get_cursor_type


class QuoteItem:
    def __init__(
        self,
        id: int,
        quote_id: int,
        vehicle_combination_name: str,
        vehicle_combination_net: int,
        transport_rate_ex_gst: float,
        product_name: str,
        product_rate_ex_gst: float,
        charge_type_name: str,
    ) -> None:
        self.id = id
        self.quote_id = quote_id
        self.vehicle_combination_name = vehicle_combination_name
        self.vehicle_combination_net = vehicle_combination_net
        self.transport_rate_ex_gst = transport_rate_ex_gst
        self.product_name = product_name
        self.product_rate_ex_gst = product_rate_ex_gst
        self.charge_type_name = charge_type_name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)})"

    def total_inc_gst(self) -> float:

        return 1.1 * (
            (self.transport_rate_ex_gst + self.product_rate_ex_gst)
            * self.vehicle_combination_net
        )

    def insert(self):

        with get_cursor_type() as cur:

            if not cur:
                return

            self.id = cur.execute(
                """
                INSERT INTO quote_item (quote_id, vehicle_combination_name, vehicle_combination_net, transport_rate_ex_gst, product_name, product_rate_ex_gst, charge_type_name) 
                OUTPUT INSERTED.id
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                [
                    self.quote_id,
                    self.vehicle_combination_name,
                    self.vehicle_combination_net,
                    self.transport_rate_ex_gst,
                    self.product_name,
                    self.product_rate_ex_gst,
                    self.charge_type_name,
                ],
            ).fetchone()[0]

    def update(self):

        with get_cursor_type() as cur:

            if not cur:
                return

            cur.execute(
                """
                UPDATE quote_item 
                SET quote_id = ?, vehicle_combination_name = ?, vehicle_combination_net = ?, transport_rate_ex_gst = ?, product_name = ?, product_rate_ex_gst = ?, charge_type_name = ?
                WHERE id = ?;
                """,
                [
                    self.quote_id,
                    self.vehicle_combination_name,
                    self.vehicle_combination_net,
                    self.transport_rate_ex_gst,
                    self.product_name,
                    self.product_rate_ex_gst,
                    self.charge_type_name,
                    self.id,
                ],
            )

    def delete(self):

        with get_cursor_type() as cur:

            if not cur:
                return

            cur.execute(
                """
                DELETE FROM quote_item 
                WHERE id = ?;
                """,
                [self.id],
            )

    @classmethod
    def get(cls, id: int = None, quote_id: int = None) -> dict:

        records: list[tuple] = None

        with get_cursor_type() as cur:

            if not cur:
                return dict()

            if not id:
                records = cur.execute(
                    """
                    SELECT id, quote_id, vehicle_combination_name, vehicle_combination_net, transport_rate_ex_gst, product_name, product_rate_ex_gst, charge_type_name 
                    FROM quote_item;
                    """
                ).fetchall()

            else:
                records = cur.execute(
                    """
                    SELECT id, quote_id, vehicle_combination_name, vehicle_combination_net, transport_rate_ex_gst, product_name, product_rate_ex_gst, charge_type_name 
                    FROM quote_item 
                    WHERE id = ?;
                    """,
                    [id],
                ).fetchall()

        quote_item_list: list[QuoteItem] = [QuoteItem(*r) for r in records]
        if quote_id:
            quote_item_list = list(
                filter(lambda qi: qi.quote_id == quote_id, quote_item_list)
            )

        return {qi.id: qi for qi in quote_item_list}
