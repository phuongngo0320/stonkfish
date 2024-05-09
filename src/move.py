from src.cell import Cell
from src.piece import Piece, PieceType

class Move:
    
    def __init__(self, fromCell: Cell, toCell: Cell, promotion: PieceType = PieceType.NONE) -> None:
        self.fromCell = fromCell
        self.toCell = toCell
        self.promotion = promotion
        
    def is_promotion(self):
        return self.promotion != PieceType.NONE
        
    def getFEN(self) -> str:
        fen_from = self.fromCell.getFEN()
        fen_to = self.toCell.getFEN()
        
        if self.promotion != PieceType.NONE:
            return fen_from + fen_to + Piece(self.promotion).getFEN()
        
        return fen_from + fen_to
    
    def __eq__(self, value: object) -> bool:
        return (
            self.fromCell == value.fromCell and
            self.toCell == value.toCell and 
            self.promotion == value.promotion
        )
    
    def __repr__(self) -> str:
        return self.getFEN()