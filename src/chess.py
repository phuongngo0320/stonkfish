from src.move import Move
from src.player import Side
from src.state import State
from src.game import Game

class Chess(Game):
    MAXPL = Side.WHITE
    MINPL = Side.BLACK

    def actions(self, state: State):
        return state.possible_moves()
    
    def result(self, state: State, move: Move):
        return state.move(move.fromCell, move.toCell)
    
    def utility(self, state: State, player):
        pass
    
    def terminal_test(self, state):
        pass
    
    def to_move(self, state):
        pass
        