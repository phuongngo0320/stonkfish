from enum import Enum

class PieceType(Enum):
    NONE = 0
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6
    
class PieceColor(Enum):
    WHITE = 0
    BLACK = 1
    
def opponent_piece_color(color: PieceColor):
    return PieceColor(1 - color.value)

PIECE_NAMES = [None, 'pawn', 'knight', 'bishop', 'rook', 'queen', 'king']

class Piece:
    
    
    def __init__(self, type: PieceType = PieceType.NONE, color: PieceColor = PieceColor.WHITE) -> None:
        self.type = type
        self.color = color
        
    def getFEN(self) -> str:
        if self.type == PieceType.NONE:
            return "."
        
        fen = None
        if self.type == PieceType.PAWN:        fen = "p"
        elif self.type == PieceType.KNIGHT:    fen = "n"
        elif self.type == PieceType.BISHOP:    fen = "b"
        elif self.type == PieceType.ROOK:      fen = "r"
        elif self.type == PieceType.QUEEN:     fen = "q"
        elif self.type == PieceType.KING:      fen = "k"
        else:
            raise Exception(f"Invalid piece type: {self.type}")
        
        if self.color == PieceColor.WHITE:
            fen = fen.upper()
            
        return fen
    
    def getName(self) -> str:
        return (
            "black " if self.color == PieceColor.BLACK else "white " + PIECE_NAMES[self.type.value]
        )
        
    def __repr__(self) -> str:
        return self.getFEN()

