from datetime import datetime
from .QuoteItem import QuoteItem
from app.db.SQLCursor import SQLCursor


class Quote():

    def __init__(self, id: int, date_created: datetime, date_required: datetime, name: str, address: str, suburb: str, contact_number: str) -> None:
        self.id = id
        self.date_created = date_created
        self.date_required = date_required
        self.name = name
        self.address = address
        self.suburb = suburb
        self.contact_number = contact_number

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({vars(self)})'
        
    def items(self, all_quote_items: list[QuoteItem] = None) -> list[QuoteItem]:
        '''Returns all QuoteItem objects that belong to this Quote's id.'''
        
        if all_quote_items:
            return list(filter(lambda qi: qi.quote_id == self.id, all_quote_items))

        return QuoteItem.get_by_quote_id(self.id)

    def total_inc_gst(self, all_quote_items: list[QuoteItem] = None) -> float:

        items = self.items(all_quote_items)

        return 1.1 * sum([((qi.transport_rate_ex_gst + qi.product_rate_ex_gst) * qi.vehicle_combination_net) for qi in items])


    def insert(self):

        with SQLCursor() as cur:
            cur.execute('''
                INSERT INTO quote (date_created, date_required, name, address, suburb, contact_number) 
                VALUES (?, ?, ?, ?, ?, ?);''', 
                (self.date_created.date(), self.date_required.date(), self.name, self.address, self.suburb, self.contact_number,))
            last_record = cur.execute('SELECT id FROM quote WHERE ROWID = last_insert_rowid();').fetchall()
            self.id = last_record[0][0]

    def update(self):

        with SQLCursor() as cur:
            cur.execute('''
                UPDATE quote 
                SET date_created = ?, date_required = ?, name = ?, address = ?, suburb = ?, contact_number = ? 
                WHERE id = ?;''', 
                (self.date_created.date(), self.date_required.date(), self.name, self.address, self.suburb, self.contact_number, self.id,))

    def delete(self):

        with SQLCursor() as cur:
            cur.execute('DELETE FROM quote WHERE id = ?;', (self.id,))

    @classmethod
    def get(cls, id: int = None) -> list:

        records = list()

        with SQLCursor() as cur:

            if not id:
                records = cur.execute('''
                    SELECT id, date_created, date_required, name, address, suburb, contact_number 
                    FROM quote;''').fetchall()
            else:
                records = cur.execute('''
                    SELECT id, date_created, date_required, name, address, suburb, contact_number 
                    FROM quote WHERE id = ?;''', 
                    (id,)).fetchall()
            
        return [Quote(r[0], datetime.strptime(r[1], '%Y-%m-%d'), datetime.strptime(r[2], '%Y-%m-%d'), r[3], r[4], r[5], r[6]) for r in records]