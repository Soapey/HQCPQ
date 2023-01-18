from .Product import Product
from .RateType import RateType


class ProductRate():

    def __init__(self, id, product: Product, rate_type: RateType, rate) -> None:
        self.id = id
        self.product = product
        self.rate_type = rate_type
        self.rate = rate

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({vars(self)})'