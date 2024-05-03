class Move:
    
    def __init__(self, fromCell: tuple, toCell: tuple) -> None:
        self.fromCell = fromCell
        self.toCell = toCell
        
    def getFEN(self) -> str:
        pass
    
    def __str__(self) -> str:
        raise NotImplementedError