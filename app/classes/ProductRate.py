class ProductRate():

    def __init__(self, id, product_id, rate_type_id, rate) -> None:
        self.id = id
        self.product_id = product_id
        self.charge_type_id = rate_type_id
        self.rate = rate

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({vars(self)})'