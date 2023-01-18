class RateType():

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({vars(self)})'