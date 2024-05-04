from src.piece import PIECE_TYPES, Piece, PieceColor, PieceType, opponent
from src.result import ResultType
from src.state import State

# MOBILITY_WEIGHT = 0.1

def evaluate_piece_type(piece_type: PieceType):
    
    if piece_type == PieceType.PAWN:    return 1
    if piece_type == PieceType.KNIGHT:  return 3
    if piece_type == PieceType.BISHOP:  return 3
    if piece_type == PieceType.ROOK:    return 5
    if piece_type == PieceType.QUEEN:   return 9
    if piece_type == PieceType.KING:    return 200
    raise Exception(f"Invalid piece type: {piece_type}")

def evaluate_goal(state: State, player: PieceColor):
    if state.result.type in [
        ResultType.STALEMATE,
        ResultType.INSUFFICIENT_MATERIAL,
        ResultType.FIFTY_MOVES,
        ResultType.SEVENTYFIVE_MOVES,
        ResultType.THREEFOLD_REPETITION,
        ResultType.FIVEFOLD_REPETITION
    ]:
        return 0
    
    if state.result.type == ResultType.CHECKMATE:
        if state.result.winner == player:
            return 1
        else:
            return -1
        
    raise Exception(f"Invalid leaf node state: {state}")

def evaluate_material(state: State, player: PieceColor):
    
    score = sum([
        (
            evaluate_piece_type(piece_type) * 
            (
                state.count_pieces(Piece(piece_type, player)) - 
                state.count_pieces(Piece(piece_type, opponent(player)))
            )
        )
        for piece_type in PIECE_TYPES
    ])
    
    return score

def evaluate_mobility(state: State, player: PieceColor):
    pass
    
    
    
