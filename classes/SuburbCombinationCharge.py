class SuburbCombinationCharge():

    def __init__(self, id, suburb_id, vehicle_combination_id, rate) -> None:
        self.id = id
        self.suburb_id = suburb_id
        self.vehicle_combination_id = vehicle_combination_id
        self.rate = rate

    def __repr__(self) -> str:
        return f'{self.__class__.name}({vars(self)})'