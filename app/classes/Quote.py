from datetime import datetime
from app.classes.QuoteItem import QuoteItem
from app.classes.QuotePDF import QuotePDF
from app.db.config import get_cursor_type


class Quote:
    def __init__(
        self,
        id: int,
        date_created: datetime,
        date_required: datetime,
        name: str,
        address: str,
        suburb: str,
        contact_number: str,
        kilometres: int,
        completed: bool,
    ) -> None:
        self.id = id
        self.date_created = date_created
        self.date_required = date_required
        self.name = name
        self.address = address
        self.suburb = suburb
        self.contact_number = contact_number
        self.kilometres = kilometres
        self.completed = completed

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)})"

    def items(
        self, all_quote_items: dict[int, QuoteItem] = None
    ) -> dict[int, QuoteItem]:

        if all_quote_items:
            return {
                qi.id: qi for qi in all_quote_items.values() if qi.quote_id == self.id
            }

        return QuoteItem.get(quote_id=self.id)

    def total_inc_gst(self, all_quote_items: dict[int, QuoteItem] = None) -> float:

        quote_items: dict[int, QuoteItem] = None
        if all_quote_items:
            quote_items = self.items(all_quote_items)
        else:
            quote_items = self.items()

        return 1.1 * sum(
            [
                (
                    (qi.transport_rate_ex_gst + qi.product_rate_ex_gst)
                    * qi.vehicle_combination_net
                )
                for qi in quote_items.values()
            ]
        )

    def insert(self):

        with get_cursor_type() as cur:

            if not cur:
                return

            self.id = cur.execute(
                """
                INSERT INTO quote (date_created, date_required, name, address, suburb, contact_number, kilometres, completed) 
                OUTPUT INSERTED.id
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                [
                    self.date_created.date(),
                    self.date_required.date(),
                    self.name,
                    self.address,
                    self.suburb,
                    self.contact_number,
                    self.kilometres,
                    int(self.completed),
                ],
            ).fetchone()[0]

    def update(self):

        with get_cursor_type() as cur:

            if not cur:
                return

            cur.execute(
                """
                UPDATE quote 
                SET date_created = ?, date_required = ?, name = ?, address = ?, suburb = ?, contact_number = ?, kilometres = ?, completed = ? 
                WHERE id = ?;
                """,
                [
                    self.date_created.date(),
                    self.date_required.date(),
                    self.name,
                    self.address,
                    self.suburb,
                    self.contact_number,
                    self.kilometres,
                    int(self.completed),
                    self.id,
                ],
            )

    def delete(self):

        with get_cursor_type() as cur:

            if not cur:
                return

            cur.execute(
                """
                DELETE FROM quote 
                WHERE id = ?;
                """,
                [self.id],
            )

    def export(self):

        QuotePDF(self).export()

    @classmethod
    def get(cls, id: int = None) -> dict:

        records: list[tuple] = None

        with get_cursor_type() as cur:

            if not cur:
                return dict()

            if not id:
                records = cur.execute(
                    """
                    SELECT id, date_created, date_required, name, address, suburb, contact_number, kilometres, completed  
                    FROM quote;
                    """
                ).fetchall()

            else:
                records = cur.execute(
                    """
                    SELECT id, date_created, date_required, name, address, suburb, contact_number, kilometres, completed 
                    FROM quote 
                    WHERE id = ?;
                    """,
                    [id],
                ).fetchall()

        return {
            q.id: q
            for q in [
                Quote(
                    r[0],
                    datetime.strptime(r[1], "%Y-%m-%d"),
                    datetime.strptime(r[2], "%Y-%m-%d"),
                    r[3],
                    r[4],
                    r[5],
                    r[6],
                    r[7],
                    bool(r[8]),
                )
                for r in records
            ]
        }
