from DragForces import SimpleDragForce


class ForceFactory:

    def getSimpleDragForce(self, dragCoefficient: float, referenceArea: float) -> SimpleDragForce:
        return SimpleDragForce(dragCoefficient, referenceArea);
