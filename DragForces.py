from IForce import IForce


class SimpleDragForce(IForce):

    def __init__(self, dragCoefficient: float) -> None:
        self._dragCoefficient: float = dragCoefficient;
        self._velocity: float = 0.0;
        self._airDensity: float = 0.0;
        self._referenceArea: float = 0.0

    def setVelocity(self, velocity: float) -> None:
        self._velocity = velocity;

    def setAirDensity(self, density: float) -> None:
        self._airDensity = density;

    def setReferenceArea(self, referenceArea: float) -> None:
        self._referenceArea = referenceArea;

    def getForce(self) -> float:
        drag_force: float = 0.5* self._airDensity * self._dragCoefficient * self._referenceArea * self._velocity**2;
        return drag_force