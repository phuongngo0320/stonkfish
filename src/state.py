from copy import deepcopy
from src.fen import parseBoard, parseCell, parsePiece
from src.move import Move
from src.piece import Piece, PieceColor
from src.result import Result, ResultType

class State:
    BOARD_SIZE = 8
    START_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    EMPTY_CELL = Piece()
    
    def __init__(self, fen=START_FEN) -> None:
        
        self.result = Result(ResultType.NONE)
        
        # board
        self.board: list[list[Piece]] = [
            [
                State.EMPTY_CELL
                for _ in range(State.BOARD_SIZE)
            ]
            for _ in range(State.BOARD_SIZE)
        ]
        
        self.to_move = PieceColor.WHITE
        self.castling_rights = (None, None, None, None) # KQkq
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.piecemap = dict()
        self.move_stack = [] 
        self.parseFEN(fen)
        
    def out_of_board(self, row, col):
        if 0 <= row < State.BOARD_SIZE and 0 <= col < State.BOARD_SIZE:
            return False
        return True
    
    def at(self, row, col) -> Piece:
        
        if self.out_of_board(row, col):
            # return None
            raise Exception(f"Out of board")
        
        return self.board[row][col]
    
    def setPiece(self, row, col, piece: Piece):
        
        if self.out_of_board(row, col):
            raise Exception(f"Out of board")
        
        self.board[row][col] = piece
    
    def move(self, move: Move):
        
        fromCell = move.fromCell
        toCell = move.toCell
        
        if not self.at(*fromCell) or not self.at(*toCell):
            raise Exception(f"Invalid move: {fromCell} -> {toCell}")
        
        state = deepcopy(self)
    
        piece = state.at(*fromCell)
        state.setPiece(*fromCell, State.EMPTY_CELL)
        state.setPiece(*toCell, piece)
        state.move_stack.append(move)
        
        self.to_move = PieceColor(1 - self.to_move.value)
        
        # ...
        return state
        
    def possible_moves(self) -> list[Move]:
        pass
    
    # -----------------------------------------------
    # check cell
    def is_empty_cell(self, cell: tuple):
        pass
    
    # -----------------------------------------------
    # check move
    def is_capture(self, move: Move):
        pass
    
    def is_check(self, move: Move):
        pass
    
    def is_castling(self, move: Move):
        pass
    
    def is_en_passant(self, move: Move):
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
    
    def parseFEN(self, fen: str):
        tokens = fen.split()

        fen_board = parseBoard(tokens[0])
        fen_turn = tokens[1]
        fen_castling_rights = tokens[2]
        fen_en_passant = tokens[3]
        fen_halfmove = tokens[4]
        fen_fullmove = tokens[5]
        
        for row in range(State.BOARD_SIZE):
            for col in range(State.BOARD_SIZE):
                fen_piece = fen_board[row*State.BOARD_SIZE + col]
                self.board[row][col] = parsePiece(fen_piece)
                
                if fen_piece != ".":
                    if fen_piece in self.piecemap:
                        self.piecemap[fen_piece] += [(row, col)]
                    else:
                        self.piecemap[fen_piece] = [(row, col)]
                
        self.to_move = PieceColor.WHITE if fen_turn == "w" else PieceColor.BLACK
        
        self.castling_rights = (
            "K" in fen_castling_rights,
            "Q" in fen_castling_rights,
            "k" in fen_castling_rights,
            "q" in fen_castling_rights
        )
        
        if fen_en_passant == "-":
            self.en_passant_target = None
        else:
            self.en_passant_target = parseCell(fen_en_passant)
        
        
        self.halfmove_clock = int(fen_halfmove)
        self.fullmove_number = int(fen_fullmove)
    
    def getFEN(self) -> str:
        pass
    
    def __repr__(self) -> str:
        
        board = "\n".join([
            " ".join([str(8 - row)] + [
                self.at(row, col).getFEN()
                for col in range(State.BOARD_SIZE)
            ])
            for row in range(State.BOARD_SIZE)
        ] + [" ".join([" "] + [
            chr(ord("a") + col)
            for col in range(State.BOARD_SIZE)
        ])]) + "\n"
        
        return board
    
    
    
    
    