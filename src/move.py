from src.cell import Cell
from src.piece import PieceType

class Move:
    
    def __init__(self, fromCell: Cell, toCell: Cell, promotion: PieceType = PieceType.NONE) -> None:
        self.fromCell = fromCell
        self.toCell = toCell
        self.promotion = promotion
        
    def is_promotion(self):
        return self.promotion != PieceType.NONE
        
    def getFEN(self) -> str:
        return self.fromCell.getFEN() + self.toCell.getFEN()
    
    def __eq__(self, value: object) -> bool:
        return (
            self.fromCell == value.fromCell and
            self.toCell == value.toCell and 
            self.promotion == value.promotion
        )
    
    def __repr__(self) -> str:
        return self.getFEN()