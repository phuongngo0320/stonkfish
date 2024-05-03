from enum import Enum

class Piece(Enum):
    NONE = 0
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6
    
PIECE_SYMBOLS = ['.', 'n', 'b', 'r', 'q', 'k']
PIECE_NAMES = ['empty', 'pawn', 'knight', 'bishop', 'rook', 'queen', 'king']