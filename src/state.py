from copy import deepcopy
from src.move import Move
from src.piece import Piece
from src.player import Side
from src.result import Result, ResultType

class State:
    BOARD_SIZE = 8
    START_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    
    def __init__(self, fen=START_FEN) -> None:
        
        self.to_move = Side.WHITE
        self.fullmove_number = 1
        self.halfmove_clock = 0
        
        self.status = Result(ResultType.NONE)
        self.board: list[list[Piece]] = self.parseFEN(fen)
        
    def out_of_board(self, row, col):
        if 0 <= row < State.BOARD_SIZE and 0 <= col < State.BOARD_SIZE:
            return False
        return True
    
    def at(self, row, col):
        
        if self.out_of_board(row, col):
            return None
        
        return self.board[row][col]
    
    def move(self, fromCell, toCell):
        
        if not self.at(*fromCell) or not self.at(*toCell):
            raise Exception(f"Invalid move: {fromCell} -> {toCell}")
        
        state = deepcopy(self)
        
        r1, c1 = fromCell
        r2, c2 = toCell
        
        piece = state.board[r1][c1]
        state.board[r1][c1] = Piece.NONE
        state.board[r2][c2] = piece
        
        # TODO: state switch
        
        return state
        
    def possible_moves(self) -> list[Move]:
        pass
    
    # -----------------------------------------------
    def is_checkmate(self):
        pass
    
    def is_stalemate(self):
        pass
    
    def is_insufficient_material(self):
        pass
    
    def is_75_moves(self):
        pass
    
    def is_50_moves(self):
        pass
    
    def is_fivefold_repetition(self):
        pass
    
    def is_threefold_repetition(self):
        pass
    
    # -----------------------------------------------
    
    def parseFEN(self, fen):
        pass
    
    def getFEN(self) -> str:
        pass
    
    def __repr__(self) -> str:
        pass
    
    
    
    
    