from datetime import date
from .QuoteItem import QuoteItem

class Quote():

    def __init__(self, 
    date_created: date, 
    name: str, 
    address: str, 
    suburb: str,
    contact_number: str,
    items: list[QuoteItem]
    ) -> None:
        pass