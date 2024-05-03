from src.cell import Cell
from src.piece import PieceType

class Move:
    
    def __init__(self, fromCell: Cell, toCell: Cell, promotion: PieceType = PieceType.NONE) -> None:
        self.fromCell = fromCell
        self.toCell = toCell
        self.promotion = promotion
        
    def getFEN(self) -> str:
        pass
    
    def __str__(self) -> str:
        raise NotImplementedError