class VehicleCombination():

    def __init__(self, id: int, name: str, net: float) -> None:
        self.id = id
        self.name = name
        self.net = net
        
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({vars(self)})'