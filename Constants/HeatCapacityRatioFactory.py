from Constants.HeatCapacityRatio import CO2HeatCapacityRatio


class HeatCapacityRatioFactory:
    def getCO2HeatCapacityRatio(self) -> CO2HeatCapacityRatio:
        return CO2HeatCapacityRatio()
