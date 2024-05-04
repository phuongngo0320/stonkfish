from src.cell import Cell
from src.piece import Piece, PieceColor, PieceType

def parseBoard(fen: str): # not parsing
    
    newfen = ""
    for ch in fen:
        if ch.isnumeric():
            count = int(ch)
            newfen += "".join(["." for _ in range(count)])
        elif ch != "/":
            newfen += ch
    
    return newfen

def parsePiece(fen: str):
    if fen == ".":
        return Piece(PieceType.NONE)

    fen_color = PieceColor.BLACK if fen.islower() else PieceColor.WHITE
    
    fen = fen.lower()
    fen_type = None
    if fen == "p":      fen_type = PieceType.PAWN
    elif fen == "n":    fen_type = PieceType.KNIGHT
    elif fen == "b":    fen_type = PieceType.BISHOP
    elif fen == "r":    fen_type = PieceType.ROOK
    elif fen == "q":    fen_type = PieceType.QUEEN
    elif fen == "k":    fen_type = PieceType.KING
    else:
        raise Exception(f"Invalid piece FEN: {fen}")
    
    return Piece(fen_type, fen_color)

def parseCell(fen: str):
    
    row = 9 - int(fen[1])
    col = ord(fen[0]) - ord("a")
    
    return Cell(row, col)

