from enum import Enum
from src.player import Side

class ResultType(Enum):
    NONE = 0
    CHECKMATE = 1
    STALEMATE = 2
    INSUFFICIENT_MATERIAL = 3
    SEVENTYFIVE_MOVES = 4
    FIVEFOLD_REPETITION = 5
    FIFTY_MOVES = 6
    THREEFOLD_REPETITION = 7
    # VARIANT_WIN = 8
    # VARIANT_LOSS = 9
    # VARIANT_DRAW = 10
    
RESULT_TYPE_NAMES = [
    'none',
    'checkmate',
    'stalemate',
    'insufficient material',
    '75 moves',
    'threefold repetition',
    # 'variant win',
    # 'variant loss',
    # 'variant draw'
]    

class Result:
    
    def __init__(self, type, winner=None) -> None:
        if type not in range(len(RESULT_TYPE_NAMES)):
            raise Exception(f"Invalid result type: {type}")
        if winner not in [Side.BLACK, Side.WHITE]:
            raise Exception(f"Invalid side: {winner}")
        
        self.type = type
        self.winner = winner