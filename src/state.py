from copy import deepcopy
from src.cell import Cell
from src.fen import parseBoard, parseCell, parsePiece
from src.move import Move
from src.piece import Piece, PieceColor, PieceType, opponent
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
        self.piecemap = dict([
            (p, [])
            for p in ['p', 'n', 'b', 'r', 'q', 'k', 'P', 'N', 'B', 'R', 'Q', 'K']
        ])
        self.move_stack = [] 
        self.parseFEN(fen)
        
    def out_of_board(self, cell: Cell):
        if 0 <= cell.row < State.BOARD_SIZE and 0 <= cell.col < State.BOARD_SIZE:
            return False
        return True
        
    def get_piece_locations(self, piece: Piece) -> list[Cell]:
        return self.piecemap[piece.getFEN()]
    
    def count_pieces(self, piece: Piece):
        return len(self.piecemap[piece.getFEN()])
    
    def at(self, cell: Cell) -> Piece:
        
        if self.out_of_board(cell):
            # return None
            raise Exception(f"Out of board")
        
        return self.board[cell.row][cell.col]
    
    def set_piece(self, cell: Cell, new_piece: Piece):
        
        if self.out_of_board(cell):
            raise Exception(f"Out of board")
        
        old_piece = self.at(cell)
        if old_piece != State.EMPTY_CELL:
            self.piecemap[old_piece].remove(cell)
        
        self.board[cell.row][cell.col] = new_piece
        
        if new_piece != State.EMPTY_CELL:
            self.piecemap[new_piece.getFEN()].append(cell)
    
    def move(self, move: Move):
        
        fromCell = move.fromCell
        toCell = move.toCell
        
        if not self.at(fromCell) or not self.at(toCell):
            raise Exception(f"Invalid move: {fromCell} -> {toCell}")
        
        state = deepcopy(self)
        
        # promo move
        if move.promotion != State.EMPTY_CELL:
            if fromCell != toCell:
                raise Exception(f"Invalid promotion: {move}")
            state.set_piece(fromCell, move.promotion)
        
        else:
            piece = self.at(fromCell)
            state.set_piece(fromCell, State.EMPTY_CELL)
            state.set_piece(toCell, piece)
            
        state.move_stack.append(move)
        state.to_move = opponent(self.to_move)
        
        if self.is_kingside_castling(move):
            if self.to_move == PieceColor.WHITE:
                state.castling_rights[0] = False
            else:
                state.castling_rights[2] = False
        elif self.is_queenside_castling(move):
            if self.to_move == PieceColor.WHITE:
                state.castling_rights[1] = False
            else:
                state.castling_rights[3] = False
                
        if self.en_passant_target:
            if self.is_en_passant(move):
                state.en_passant_target = None
        else:
            if self.is_pawn_double_move(move):
                pawn_cell = move.toCell
                
                left = pawn_cell.toLeft()
                right = pawn_cell.toRight()
                
                if not self.out_of_board(left):
                    if self.at(left) == Piece(PieceType.PAWN, opponent(self.to_move)):
                        if self.to_move == PieceColor.WHITE:
                            self.en_passant_target = left.toUp()
                        else:
                            self.en_passant_target = left.toDown()
                
                if not self.out_of_board(right):
                    if self.at(right) == Piece(PieceType.PAWN, opponent(self.to_move)):
                        if self.to_move == PieceColor.WHITE:
                            self.en_passant_target = right.toUp()
                        else:
                            self.en_passant_target = right.toDown()
                
        if self.is_half_move(move):
            self.halfmove_clock += 1
        if self.to_move == PieceColor.BLACK:
            self.fullmove_number += 1
    
        return state
    # -----------------------------------------------
    # piece rule
        
    def possible_moves(self) -> list[Move]:
        pass
    
    # -----------------------------------------------
    # check cell
    def is_empty_cell(self, cell: Cell):
        return self.at(cell) == State.EMPTY_CELL
    
    # -----------------------------------------------
    # check move
    def is_capture(self, move: Move):
        pass
    
    def is_check(self, move: Move):
        pass
    
    def is_castling(self, move: Move):
        pass
    
    def is_kingside_castling(self, move: Move):
        pass
    
    def is_queenside_castling(self, move: Move):
        pass
    
    def is_en_passant(self, move: Move):
        pass
    
    def is_pawn_double_move(self, move: Move):
        pass
    
    def is_half_move(self, move: Move):
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
                    self.piecemap[fen_piece].append(Cell(row, col))
                
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
                self.at(Cell(row, col)).getFEN()
                for col in range(State.BOARD_SIZE)
            ])
            for row in range(State.BOARD_SIZE)
        ] + [" ".join([" "] + [
            chr(ord("a") + col)
            for col in range(State.BOARD_SIZE)
        ])]) + "\n"
        
        return board
    
    
    
    
    