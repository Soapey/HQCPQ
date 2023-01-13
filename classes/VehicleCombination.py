class VehicleCombination():

    def __init__(self, id, name, net) -> None:
        self.id = id
        self.name = name
        self.net = net
        
    def __repr__(self) -> str:
        return f'{self.__class__.name}({vars(self)})'