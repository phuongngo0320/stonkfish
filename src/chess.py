from src.evaluation import evaluate_goal
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
        return evaluate_goal(state, player)
    
    def terminal_test(self, state: State):
        return state.result.type != ResultType.NONE
    
    def to_move(self, state: State):
        return state.to_move
        