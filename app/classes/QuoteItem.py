from app.db.SQLCursor import SQLCursor


class QuoteItem():

    def __init__(self, id: int, quote_id: int, vehicle_combination_name: str, vehicle_combination_net: int, transport_rate_ex_gst: float, product_name: str, product_rate_ex_gst: float) -> None:
        self.id = id
        self.quote_id = quote_id
        self.vehicle_combination_name = vehicle_combination_name
        self.vehicle_combination_net = vehicle_combination_net
        self.transport_rate_ex_gst = transport_rate_ex_gst
        self.product_name = product_name
        self.product_rate_ex_gst = product_rate_ex_gst

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({vars(self)})'

    def total_inc_gst(self) -> float:

        return 1.1 * ((self.transport_rate_ex_gst + self.product_rate_ex_gst) * self.vehicle_combination_net)

    def insert(self):

        with SQLCursor() as cur:
            cur.execute('''
                INSERT INTO quote_item (quote_id, vehicle_combination_name, vehicle_combination_net, transport_rate_ex_gst, product_name, product_rate_ex_gst) 
                VALUES (?, ?, ?, ?, ?, ?);''', 
                (self.quote_id, self.vehicle_combination_name, self.vehicle_combination_net, self.transport_rate_ex_gst, self.product_name, self.product_rate_ex_gst,))

            last_record = cur.execute('SELECT id FROM quote_item WHERE ROWID = last_insert_rowid();').fetchall()
            self.id = last_record[0][0]

    def update(self):

        with SQLCursor() as cur:
            cur.execute('''
                UPDATE quote_item 
                SET quote_id = ?, vehicle_combination_name = ?, vehicle_combination_net = ?, transport_rate_ex_gst = ?, product_name = ?, product_rate_ex_gst = ?
                WHERE id = ?;''',
                (self.quote_id, self.vehicle_combination_name, self.vehicle_combination_net, self.transport_rate_ex_gst, self.product_name, self.product_rate_ex_gst, self.id,))

    def delete(self):

        with SQLCursor() as cur:
            cur.execute('''
                DELETE FROM quote_item 
                WHERE id = ?;''', 
                (self.id,))

    @classmethod
    def get(cls, id: int = None) -> list:

        records = list()

        with SQLCursor() as cur:

            if not id:
                records = cur.execute('''
                    SELECT id, quote_id, vehicle_combination_name, vehicle_combination_net, transport_rate_ex_gst, product_name, product_rate_ex_gst 
                    FROM quote_item;''').fetchall()
            else:
                records = cur.execute('''
                    SELECT id, quote_id, vehicle_combination_name, vehicle_combination_net, transport_rate_ex_gst, product_name, product_rate_ex_gst 
                    FROM quote_item 
                    WHERE id = ?;''', 
                    (id,)).fetchall()
            
        return [QuoteItem(*r) for r in records]

    @classmethod
    def get_by_quote_id(cls, id: int):

        records = list()

        with SQLCursor() as cur:
            records = cur.execute('''
                SELECT id, quote_id, vehicle_combination_name, vehicle_combination_net, transport_rate_ex_gst, product_name, product_rate_ex_gst 
                FROM quote_item  
                WHERE quote_id = ?;''', 
                (id,)).fetchall()

        return [QuoteItem(*r) for r in records]