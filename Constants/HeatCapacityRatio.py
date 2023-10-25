from Constants.IHeatCapacityRatio import IHeatCapacityRatio


class CO2HeatCapacityRatio(IHeatCapacityRatio):

    def getHeatCapacityRatio(self, temperature: float) -> float:
        """Return heat capacity ratio of CO2 based on its temperature"""
        return 1.3  # It should interpolate from table but for now im to lazy
