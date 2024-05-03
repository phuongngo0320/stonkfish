from src.cell import Cell

class Move:
    
    def __init__(self, fromCell: Cell, toCell: Cell) -> None:
        self.fromCell = fromCell
        self.toCell = toCell
        
    def getFEN(self) -> str:
        pass
    
    def __str__(self) -> str:
        raise NotImplementedError