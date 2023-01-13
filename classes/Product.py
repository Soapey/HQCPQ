class Product():

    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return f'{self.__class__.name}({vars(self)})'