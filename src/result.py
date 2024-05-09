from enum import Enum

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
        self.type = type
        self.winner = winner
        
    def __eq__(self, value: object) -> bool:
        return self.type == value.type and self.winner == value.winner
    
    def __str__(self) -> str:
        return RESULT_TYPE_NAMES[self.type.value]