from .Suburb import Suburb
from .VehicleCombination import VehicleCombination


class SuburbCombinationCharge():

    def __init__(self, id: int, suburb: Suburb, vehicle_combination: VehicleCombination, rate: float) -> None:
        self.id = id
        self.suburb = suburb
        self.vehicle_combination = vehicle_combination
        self.rate = rate

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({vars(self)})'