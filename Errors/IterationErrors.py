
class IterationNotConverged(Exception):
    """Exception raised when function didn't converge

        Attributes:
            valueOfError -- Error after maximal number of calculations
            lastCalculatedValue -- value which was calculated in last iteration
            numberOfIterations -- Number of iteration after this error was raised
        """

    def __init__(self, valueOfError: float, lastCalculatedValue: float, numberOfIterations: int) -> None:
        self.valueOfError: float = valueOfError
        self.lastCalculatedValue: float = lastCalculatedValue;
        self.numberOfIterations: int = numberOfIterations;
        super().__init__("Function didn't converge;\n"
                         f"value of Error: {self.valueOfError}\n"
                         f"last calculated value: {self.lastCalculatedValue}\n"
                         f"number of calculations: {self.numberOfIterations}")
