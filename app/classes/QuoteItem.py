class QuoteItem():

    def __init__(self, id: int, quote_id: int, vehicle_combination_name: str, vehicle_combination_net: int, product_name: str, product_rate_ex_gst: float) -> None:
        self.id = id
        self.quote_id = quote_id
        self.vehicle_combination_name = vehicle_combination_name
        self.vehicle_combination_net = vehicle_combination_net
        self.product_name = product_name
        self.product_rate_ex_gst = product_rate_ex_gst

    