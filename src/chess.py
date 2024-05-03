from src.move import Move
from src.piece import PieceColor
from src.result import ResultType
from src.state import State
from src.game import Game

class Chess(Game):
    MAXPL = PieceColor.WHITE
    MINPL = PieceColor.BLACK

    def actions(self, state: State):
        return state.possible_moves()
    
    def result(self, state: State, move: Move):
        return state.move(move.fromCell, move.toCell)
    
    def utility(self, state: State, player: PieceColor):
        
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
    
    def terminal_test(self, state: State):
        return state.result.type != ResultType.NONE
    
    def to_move(self, state: State):
        return state.to_move
        