from datetime import date
from .QuoteItem import QuoteItem
from db.SQLCursor import SQLCursor


class Quote():

    def __init__(self, id: int, date_created: date, date_required: date, name: str, address: str, suburb: str, contact_number: str) -> None:
        self.id = id
        self.date_created = date_created
        self.date_required = date_required
        self.name = name
        self.address = address
        self.suburb = suburb
        self.contact_number = contact_number
        
    def items(self, all_quote_items: list[QuoteItem] = None) -> list[QuoteItem]:
        '''Returns all QuoteItem objects that belong to this Quote's id.'''
        
        if all_quote_items:
            return list(filter(lambda qi: qi.quote_id == self.id, all_quote_items))

        with SQLCursor() as cur:
            records = cur.execute('''
            SELECT id, quote_id, vehicle_combination_name, vehicle_combination_net, product_name, product_rate_ex_gst 
            FROM quoteitem 
            WHERE quote_id = ?;''', (self.id,)).fetchall()
            
            return [QuoteItem(*r) for r in records]

    @classmethod
    def get_all():

        with SQLCursor() as cur:
            records = cur.execute('''
            SELECT id, date_created, date_required, name, address, suburb, contact_number
            FROM quote;''').fetchall()
            
            return [Quote(*r) for r in records]



        