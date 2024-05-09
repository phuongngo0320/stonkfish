from copy import deepcopy
from src.cell import Cell
from src.fen import parseBoard, parseCell, parseMove, parsePiece
from src.move import Move
from src.piece import Piece, PieceColor, PieceType, opponent
from src.result import Result, ResultType

class State:
    BOARD_SIZE = 8
    START_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    EMPTY_CELL = Piece()
    
    def __init__(self, fen=START_FEN) -> None:
        
        self.result = None
        
        # board
        self.board: list[list[Piece]] = [
            [
                State.EMPTY_CELL
                for _ in range(State.BOARD_SIZE)
            ]
            for _ in range(State.BOARD_SIZE)
        ]
        
        self.to_move = PieceColor.WHITE
        self.castling_rights = [None, None, None, None] # KQkq
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        
        # helper states
        self.piecemap = dict([
            (p, [])
            for p in ['p', 'n', 'b', 'r', 'q', 'k', 'P', 'N', 'B', 'R', 'Q', 'K']
        ])
        self.move_stack = [] 
        self.check_stack = []
        self.check = False # check if current state is a check
        self.promo = False # check if a player should promote a pawn
        
        self.temp_castling_revoked = [False, False, False, False]
        
        # parse input
        self.parseFEN(fen)
        
    def game_over(self):
        return self.result is not None
        
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
            self.piecemap[old_piece.getFEN()].remove(cell)
        
        self.board[cell.row][cell.col] = new_piece
        
        if new_piece != State.EMPTY_CELL:
            self.piecemap[new_piece.getFEN()].append(cell)
    
    def move(self, move: Move, update=True):
        
        fromCell = move.fromCell
        toCell = move.toCell
        
        if not self.at(fromCell) or not self.at(toCell):
            raise Exception(f"Invalid move: {fromCell} -> {toCell}")
        
        state = deepcopy(self)
        
        # promo move
        isPromoMove = move.is_promotion()
        
        if isPromoMove:
            if not self.promo:
                print(self.getFEN())
                raise Exception(f"Invalid promotion: not a promo state")
            if fromCell != toCell:
                raise Exception(f"Invalid promotion: {move}")
            state.set_piece(fromCell, Piece(move.promotion, self.to_move))
            state.promo = False
            if update:
                state.to_move = opponent(self.to_move)
        
        # not promo
        else:            
            piece = self.at(fromCell)
            state.set_piece(fromCell, State.EMPTY_CELL)
            state.set_piece(toCell, piece)
            
            # add rook move for castling
            if self.is_kingside_castling(move):
                
                rookCell = None
                if self.to_move == PieceColor.WHITE:
                    rookCell = parseCell("h1")
                else:
                    rookCell = parseCell("h8")
                    
                rook = self.at(rookCell)
                state.set_piece(rookCell, State.EMPTY_CELL)
                state.set_piece(toCell.toLeft(), rook)
                    
            elif self.is_queenside_castling(move):
                
                rookCell = None
                if self.to_move == PieceColor.WHITE:
                    rookCell = parseCell("a1")
                else:
                    rookCell = parseCell("a8")
                
                rook = self.at(rookCell)
                state.set_piece(rookCell, State.EMPTY_CELL)
                state.set_piece(toCell.toRight(), rook)
        
        state.move_stack.append(move)
        
        if self.is_pawn_promo_move(move):
            state.promo = True # let player choose which one to promo
        else:
            if update:
                state.to_move = opponent(self.to_move)
        
        if not update:    
            return state   
        
        # if not update:    
        #     return state
        
        if self.is_check(move, promo_piece=(Piece(move.promotion, self.to_move) if isPromoMove else None)): 
            state.check_stack.append(True)
            state.check = True
            
            if state.is_checkmate():
                state.result = Result(ResultType.CHECKMATE, opponent(self.to_move))
                return state
        else:
            state.check_stack.append(False)
            state.check = False
            
            if state.is_stalemate():
                state.result = Result(ResultType.STALEMATE)
                return state 
            
        # if self.is_checkmate():
        #     state.result = Result(ResultType.CHECKMATE, opponent(self.to_move))
        #     return state
        # if self.is_stalemate():
        #     state.result = Result(ResultType.STALEMATE)
        #     return state 
        # state.to_move = opponent(self.to_move)
        
        # castling right state switch -----------------------------------------------
        
        # TODO
        # CASE: gain castling right after temporary revoke, if no more check
        if not self.is_checking():
            if self.at(parseCell("e8")).getFEN() == "k":
                if self.temp_castling_revoked[2]:   
                    state.castling_rights[2] = True
                    state.temp_castling_revoked[2] = False
                if self.temp_castling_revoked[3]:   
                    state.castling_rights[3] = True
                    state.temp_castling_revoked[3] = False
            if self.at(parseCell("e1")).getFEN() == "K":
                if self.temp_castling_revoked[0]:   
                    state.castling_rights[0] = True
                    state.temp_castling_revoked[0] = False
                if self.temp_castling_revoked[1]:   
                    state.castling_rights[1] = True    
                    state.temp_castling_revoked[1] = False
        
        # check castling move
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
                
        # check disabled castling rights
        
        # CASE: moved king/rook
        if self.is_empty_cell(fromCell): raise Exception("Moving nothing!")
        moved_piece = self.at(fromCell)
        
            # case: K moved
        if fromCell.getFEN() == "e1" and moved_piece.getFEN() == "K":
            
            if self.castling_rights[0]:
                state.castling_rights[0] = False
            if self.castling_rights[1]:
                state.castling_rights[1] = False
            
            # case: left R moved
        if fromCell.getFEN() == "a1" and moved_piece.getFEN() == "R" and self.castling_rights[1]:
            state.castling_rights[1] = False
            
            # case right R moved
        if fromCell.getFEN() == "h1" and moved_piece.getFEN() == "R" and self.castling_rights[0]:
            state.castling_rights[0] = False
            
            # case: k moved
        if fromCell.getFEN() == "e8" and moved_piece.getFEN() == "k":
            
            if self.castling_rights[2]:
                state.castling_rights[2] = False
            if self.castling_rights[3]:
                state.castling_rights[3] = False
                
            # case: left r moved
        if fromCell.getFEN() == "a8" and moved_piece.getFEN() == "r" and self.castling_rights[3]:
            state.castling_rights[3] = False
            
            # case: right r moved
        if fromCell.getFEN() == "h8" and moved_piece.getFEN() == "r" and self.castling_rights[2]:
            state.castling_rights[2] = False
        
        # TODO
        # CASE: check opponent king --> disabled opponent's castling right (temporary revoke)
        if state.check:
            if self.to_move == PieceColor.WHITE:
                if self.castling_rights[2]:
                    state.castling_rights[2] = False
                    state.temp_castling_revoked[2] = True
                if self.castling_rights[3]:
                    state.castling_rights[3] = False
                    state.temp_castling_revoked[3] = True
            else:
                if self.castling_rights[0]:
                    state.castling_rights[0] = False
                    state.temp_castling_revoked[0] = True
                if self.castling_rights[1]:
                    state.castling_rights[1] = False
                    state.temp_castling_revoked[1] = True
        
        # en passant target state switch ---------------------------------
        if self.en_passant_target:
            state.en_passant_target = None
        else:
            if self.is_pawn_double_move(move):
                pawn_cell = move.toCell
                
                left = pawn_cell.toLeft()
                right = pawn_cell.toRight()
                
                if not self.out_of_board(left):
                    if self.at(left) == Piece(PieceType.PAWN, opponent(self.to_move)):
                        if self.to_move == PieceColor.WHITE:
                            state.en_passant_target = pawn_cell.toDown()
                        else:
                            state.en_passant_target = pawn_cell.toUp()
                
                if not self.out_of_board(right):
                    if self.at(right) == Piece(PieceType.PAWN, opponent(self.to_move)):
                        if self.to_move == PieceColor.WHITE:
                            state.en_passant_target = pawn_cell.toDown()
                        else:
                            state.en_passant_target = pawn_cell.toUp()
                
        if self.is_half_move(move):
            state.halfmove_clock += 1
        if self.to_move == PieceColor.BLACK:
            state.fullmove_number += 1
    
        return state
    # -----------------------------------------------
    # piece rule
    # def is_typ(self, piece: str):
    #     if piece.islower():    
    #         if str == ''
        
    def possible_moves(self) -> list[Move]:
        return self.possible_moves_color(self.to_move) 

    def possible_moves_color(self, color:PieceColor, to_move_check = True):
        moves =[]
        for piece, curr_cell in self.piecemap.items():
            curr_piece = parsePiece(piece)
            if curr_piece.color == color:
                for cell in curr_cell:
                    moves += self.possible_piece_moves(curr_piece,cell, to_move_check)
        return moves
    
    def to_direction (self, curr_cell:Cell, direc, distance) -> Cell:
        if direc == 'toUp':
            return curr_cell.toUp(distance)
        elif direc == 'toDown':
            return curr_cell.toDown(distance)
        elif direc == 'toLeft':
            return curr_cell.toLeft(distance)
        elif direc == 'toRight':
            return curr_cell.toRight(distance)
        elif direc == 'toUpRight':
            return curr_cell.toUpRight(distance)
        elif direc == 'toUpLeft':
            return curr_cell.toUpLeft(distance)
        elif direc == 'toDownRight':
            return curr_cell.toDownRight(distance)
        elif direc == 'toDownLeft':
            return curr_cell.toDownLeft(distance)
        
    def all_danger_zone_move(self, color:PieceColor):
        moves =[]
        for piece, curr_cell in self.piecemap.items():
            curr_piece = parsePiece(piece)
            if curr_piece.color == color:
                for cell in curr_cell:
                    moves += self.danger_zone_move(curr_piece,cell)
        return moves

    def danger_zone_move(self, piece:Piece, curr_cell:Cell):
        moves = []
        none = State.EMPTY_CELL

        if self.result is not None: return moves
        # WHITE PAWN
        if piece == Piece(PieceType.PAWN, PieceColor.WHITE):
            next_cell_capture = [curr_cell.toUpLeft(1), curr_cell.toUpRight(1)]
            for next_cell in next_cell_capture:
                if self.out_of_board(next_cell) is True: continue
                if self.at(next_cell) != none:
                    moves.append(Move(curr_cell,next_cell))

        # BLACK PAWN
        elif piece == Piece(PieceType.PAWN, PieceColor.BLACK):
            next_cell_capture = [curr_cell.toDownLeft(1), curr_cell.toDownRight(1)]
            for next_cell in next_cell_capture:
                if self.out_of_board(next_cell) is True: continue
                if self.at(next_cell) != none:
                    moves.append(Move(curr_cell,next_cell))

        elif piece.type == PieceType.KNIGHT: 
            next_cells = [curr_cell.toUp(2).toRight(1), curr_cell.toUp(2).toLeft(1),
                         curr_cell.toUp(1).toRight(2), curr_cell.toUp(1).toLeft(2),
                         curr_cell.toDown(2).toRight(1), curr_cell.toDown(2).toLeft(1),
                         curr_cell.toDown(1).toRight(2), curr_cell.toDown(1).toLeft(2)]
            for next_cell in next_cells:

                if self.out_of_board(next_cell) is True: continue

                moves.append(Move(curr_cell,next_cell))

        elif piece.type == PieceType.BISHOP:
            directions = ['toUpRight', 'toUpLeft', 'toDownRight', 'toDownLeft']
            for direct in directions:
                for i in range(1,8):
                    next_cell = self.to_direction(curr_cell, direct, i)
                    if self.out_of_board(next_cell) is True: break 
                    if self.at(next_cell) != none:
                        if self.at(next_cell).color != piece.color:
                            moves.append(Move(curr_cell,next_cell))
                            moves.append(Move(curr_cell,self.to_direction(next_cell, direct, 1)))
                            break
                        else:
                            moves.append(Move(curr_cell,next_cell))
                            break

                    moves.append(Move(curr_cell,next_cell))

        elif piece.type == PieceType.ROOK:
            directions = ['toUp', 'toDown', 'toLeft', 'toRight']
            for direct in directions:
                for i in range(1,8):
                    next_cell = self.to_direction(curr_cell, direct, i) 
                    if self.out_of_board(next_cell) is True: break
                    if self.at(next_cell) != none:
                        if self.at(next_cell).color != piece.color:
                            moves.append(Move(curr_cell,next_cell))
                            moves.append(Move(curr_cell,self.to_direction(next_cell, direct, 1)))
                            break
                        else:
                            moves.append(Move(curr_cell,next_cell))
                            break
                    moves.append(Move(curr_cell,next_cell))
                    
        elif piece.type == PieceType.QUEEN:
            directions = ['toUp', 'toDown', 'toLeft', 'toRight',
                          'toUpRight', 'toUpLeft', 'toDownRight', 'toDownLeft']
            for direct in directions:
                for i in range(1,8):
                    next_cell = self.to_direction(curr_cell, direct, i)
                    if self.out_of_board(next_cell) is True: break
                    if self.at(next_cell) != none:
                        if self.at(next_cell).color != piece.color:
                            moves.append(Move(curr_cell,next_cell))
                            moves.append(Move(curr_cell,self.to_direction(next_cell, direct, 1)))
                            break
                        else:
                            moves.append(Move(curr_cell,next_cell))
                            break
                    moves.append(Move(curr_cell,next_cell))

        return moves

    
    def possible_piece_moves(self, piece:Piece, curr_cell:Cell, to_move_check = True) -> list[Move]:
        piece_color = piece.color
        moves = []
        none = State.EMPTY_CELL
        # print(moves)
        # if piece.color != self.to_move: raise Exception('Not your turn!!!')
        if self.result is not None: return moves
        # print(str(curr_cell) + ' ' + str(self.promo))
        if self.promo == True and piece.type != PieceType.PAWN and piece.color == self.to_move: return moves
        elif self.promo == True and piece.type == PieceType.PAWN and piece.color == self.to_move:
            if curr_cell.row != 7 and curr_cell.row != 0: return moves 

        # WHITE PAWN
        if piece == Piece(PieceType.PAWN, PieceColor.WHITE):
            if curr_cell.row == 0:
                curr_cell_str = str(curr_cell)
                moves.append(parseMove(curr_cell_str+curr_cell_str+'Q'))
                moves.append(parseMove(curr_cell_str+curr_cell_str+'N'))
                moves.append(parseMove(curr_cell_str+curr_cell_str+'B'))
                moves.append(parseMove(curr_cell_str+curr_cell_str+'R'))
            if self.out_of_board(curr_cell.toUp()): return moves
            if self.at(curr_cell.toUp()) == none:
                moves.append(Move(curr_cell,curr_cell.toUp()))
            
            if curr_cell.row == 6:
                if self.at(curr_cell.toUp(2)) == none:
                    moves.append(Move(curr_cell,curr_cell.toUp(2)))
            next_cell_capture = [curr_cell.toUpLeft(1), curr_cell.toUpRight(1)]
            for next_cell in next_cell_capture:
                if self.out_of_board(next_cell) is True: continue

                if self.at(next_cell) != none:
                    if self.at(next_cell).color == piece_color: 
                        continue
                    moves.append(Move(curr_cell,next_cell))
                else:
                    if self.en_passant_target is not None and self.en_passant_target == next_cell:
                        moves.append(Move(curr_cell,next_cell))
        # BLACK PAWN
        elif piece == Piece(PieceType.PAWN, PieceColor.BLACK):
            if curr_cell.row == 7:
                curr_cell_str = str(curr_cell)
                moves.append(parseMove(curr_cell_str+curr_cell_str+'q'))
                moves.append(parseMove(curr_cell_str+curr_cell_str+'n'))
                moves.append(parseMove(curr_cell_str+curr_cell_str+'b'))
                moves.append(parseMove(curr_cell_str+curr_cell_str+'r'))    
            if self.out_of_board(curr_cell.toDown()): return moves
            if self.at(curr_cell.toDown()) == none:
                moves.append(Move(curr_cell,curr_cell.toDown()))
            if curr_cell.row == 1:
                if self.at(curr_cell.toDown(2)) == none:
                    moves.append(Move(curr_cell,curr_cell.toDown(2)))
            next_cell_capture = [curr_cell.toDownLeft(1), curr_cell.toDownRight(1)]
            for next_cell in next_cell_capture:
                if self.out_of_board(next_cell) is True: continue
                if self.at(next_cell) != none:
                    if self.at(next_cell).color == piece_color: 
                        continue
                    moves.append(Move(curr_cell,next_cell))
                else:
                    if self.en_passant_target is not None and self.en_passant_target == next_cell:
                        moves.append(Move(curr_cell,next_cell))

        elif piece.type == PieceType.KNIGHT: 
            next_cells = [curr_cell.toUp(2).toRight(1), curr_cell.toUp(2).toLeft(1),
                         curr_cell.toUp(1).toRight(2), curr_cell.toUp(1).toLeft(2),
                         curr_cell.toDown(2).toRight(1), curr_cell.toDown(2).toLeft(1),
                         curr_cell.toDown(1).toRight(2), curr_cell.toDown(1).toLeft(2)]
            for next_cell in next_cells:

                if self.out_of_board(next_cell) is True: continue
                if self.at(next_cell) != none:
                    if self.at(next_cell).color == piece_color: continue
                
                moves.append(Move(curr_cell,next_cell))

        elif piece.type == PieceType.BISHOP:
            directions = ['toUpRight', 'toUpLeft', 'toDownRight', 'toDownLeft']
            for direct in directions:
                for i in range(1,8):
                    next_cell = self.to_direction(curr_cell, direct, i)
                    if self.out_of_board(next_cell) is True: break
                    if self.at(next_cell) != none:
                        if self.at(next_cell).color == piece_color: break
                        else:
                            moves.append(Move(curr_cell,next_cell))
                            break
                    moves.append(Move(curr_cell,next_cell))

        elif piece.type == PieceType.ROOK:
            directions = ['toUp', 'toDown', 'toLeft', 'toRight']
            for direct in directions:
                for i in range(1,8):
                    next_cell = self.to_direction(curr_cell, direct, i) 
                    if self.out_of_board(next_cell) is True: break
                    if self.at(next_cell) != none:
                        if self.at(next_cell).color == piece_color: break
                        else:
                            moves.append(Move(curr_cell,next_cell))
                            break
                    moves.append(Move(curr_cell,next_cell))
                    
        elif piece.type == PieceType.QUEEN:
            directions = ['toUp', 'toDown', 'toLeft', 'toRight',
                          'toUpRight', 'toUpLeft', 'toDownRight', 'toDownLeft']
            for direct in directions:
                for i in range(1,8):
                    next_cell = self.to_direction(curr_cell, direct, i)
                    if self.out_of_board(next_cell) is True: break
                    if self.at(next_cell) != none:
                        if self.at(next_cell).color == piece_color: break
                        else:
                            moves.append(Move(curr_cell,next_cell))
                            break
                    moves.append(Move(curr_cell,next_cell))

        elif piece.type == PieceType.KING:
            directions = ['toUp', 'toDown', 'toLeft', 'toRight',
                          'toUpRight', 'toUpLeft', 'toDownRight', 'toDownLeft']
            for direct in directions:
                next_cell = self.to_direction(curr_cell, direct, 1)
                if self.out_of_board(next_cell) is True: continue
                if self.at(next_cell) != none:
                    if self.at(next_cell).color == piece_color: continue
                
                moves.append(Move(curr_cell,next_cell))
            #Castling
            if piece.color == PieceColor.WHITE:
                if self.castling_rights[0] == True:
                    next_cell = curr_cell.toRight(2)
                    if Move(curr_cell,curr_cell.toRight()) in moves:
                        if self.at(next_cell) == none:
                            moves.append(Move(curr_cell,curr_cell.toRight(2)))
                if self.castling_rights[1] == True:
                    next_cell = curr_cell.toLeft(2)
                    if Move(curr_cell,curr_cell.toLeft()) in moves:
                        if self.at(next_cell) == none:
                            moves.append(Move(curr_cell,curr_cell.toLeft(2)))
            else:
                if self.castling_rights[2] == True:
                    next_cell = curr_cell.toRight(2)
                    if Move(curr_cell,curr_cell.toRight()) in moves:
                        if self.at(next_cell) == none:
                            moves.append(Move(curr_cell,curr_cell.toRight(2)))
                if self.castling_rights[3] == True:
                    next_cell = curr_cell.toLeft(2)
                    if Move(curr_cell,curr_cell.toLeft()) in moves:
                        if self.at(next_cell) == none:
                            moves.append(Move(curr_cell,curr_cell.toLeft(2)))

        remove_move = []
        # King must not kill itseft
        # print(moves)
        if to_move_check:
            if piece.type == PieceType.KING:
                for check_move in moves:
                    enemy_moves = self.all_danger_zone_move(opponent(self.to_move))
                    for enemy_move in enemy_moves:
                        if check_move.toCell == enemy_move.toCell:
                            remove_move.append(check_move)
                            break
            else:
                for check_move in moves:
                    check_state = self.move(check_move, False)
                    check_state.to_move = opponent(self.to_move)
                    enemy_moves = check_state.possible_moves_color(opponent(self.to_move),False)
                    for enemy_move in enemy_moves:
                        if check_state.is_capture_king(enemy_move):
                            remove_move.append(check_move)
                            break
                
        for i in remove_move:
            moves.remove(i)

        return moves


    
    # -----------------------------------------------
    # check cell
    def is_empty_cell(self, cell: Cell):
        return self.at(cell) == State.EMPTY_CELL
    
    # -----------------------------------------------
    # check move
    def is_capture_king(self, move:Move):
        if self.is_capture(move) is True:
            if self.at(move.toCell).type == PieceType.KING: return True
        return False

    def is_capture(self, move: Move):
        # if self.is_empty_cell(move.toCell) is True: return False
        if self.out_of_board(move.toCell): raise Exception(str(self.at(move.fromCell).color)+ " " + str(move))
        if self.at(move.toCell) == State.EMPTY_CELL: return False
        
        to_cell_piece = self.at(move.toCell)
        if self.to_move != to_cell_piece.color: return True
        return False
    
    def is_check(self, move: Move, promo_piece: Piece = None) -> bool:
        typ = self.at(move.fromCell) if promo_piece is None else promo_piece
        next_moves = self.possible_piece_moves(typ, move.toCell)
        for next_move in next_moves:
            if self.is_capture_king(next_move): return True
        return False
     
    def is_castling(self, move: Move):
        pass
    
    def check_castling_color(self, move:Move, color:PieceColor, is_kingside: True):
        if self.at(move.fromCell).type == PieceType.KING:
            if color == PieceColor.WHITE:
                if is_kingside is True:
                    if self.castling_rights[0] is True:
                        if move.fromCell.toRight(2) == move.toCell: return True
                    return False
                else:
                    if self.castling_rights[1] is True:
                        if move.fromCell.toLeft(2) == move.toCell: return True
                    return False
            if color == PieceColor.BLACK:
                if is_kingside is True:
                    if self.castling_rights[2] is True:
                        if move.fromCell.toRight(2) == move.toCell: return True
                    return False
                else:
                    if self.castling_rights[3] is True:
                        if move.fromCell.toLeft(2) == move.toCell: return True
                    return False
        return False
    
    def is_kingside_castling(self, move: Move):
        return self.check_castling_color(move,self.at(move.fromCell).color,True)
    
    def is_queenside_castling(self, move: Move):
        return self.check_castling_color(move,self.at(move.fromCell).color,False)
    

    # def last_state(self, last_move: Move):
        

    def is_en_passant(self, move: Move):
        # last_move = self.move_stack[-1]
        

        if self.at(move.fromCell).type != PieceType.PAWN: return False
        if self.en_passant_target is not None:
            if self.at(self.en_passant_target) ==  State.EMPTY_CELL:
                if self.en_passant_target == move.toCell:
                # if self.at(last_move.toCell).color != self.to_move:
                #     if move.fromCell == last_move.toCell.toRight(1) or move.fromCell == last_move.toCell.toLeft(1):
                #         if move.toCell == last_move.toCell.toUp() or move.toCell == last_move.toCell.toDown(): 
                            if self.at(move.toCell) == State.EMPTY_CELL: 
                                return True
                    
        return False

    
    def is_pawn_double_move(self, move: Move):
        curr_piece = self.at(move.fromCell)
        if curr_piece.type != PieceType.PAWN: return False
        else:
            if curr_piece.color == PieceColor.BLACK:
                if move.fromCell.toDown(2) != move.toCell: return False
                else:
                    # if self.is_empty_cell(move.toCell) is False: return False
                    if self.at(move.toCell) != State.EMPTY_CELL: return False

            else:
                if move.fromCell.toUp(2) != move.toCell: return False
                else:
                    # if self.is_empty_cell(move.toCell) is False: return False
                    if self.at(move.toCell) != State.EMPTY_CELL: return False
        return True

    def is_pawn_promo_move(self, move: Move):
        
        if self.at(move.fromCell).type != PieceType.PAWN:
            return False
        
        toCell = move.toCell
        
        if self.to_move == PieceColor.WHITE:
            return toCell.row == 0
        
        return toCell.row == 7
    
    def is_half_move(self, move: Move):
        
        if self.is_capture(move) or self.at(move.fromCell).type == PieceType.PAWN:
            return False
        return True
    
    # -----------------------------------------------
    # check state
    
    # case: game over
    def is_checkmate(self):
        # enemy_color = opponent(self.to_move)
        if self.is_checking():
            own_moves = self.possible_moves_color(self.to_move)
            
            # print(own_moves)
            # for move in own_moves:
            #     check_state = self.move(move,False)
            #     enemy_moves = check_state.possible_moves_color(enemy_color)
            #     for enemy_move in enemy_moves:
            #         if check_state.is_capture_king(enemy_move): 
            #             # self.result = Result(ResultType.CHECKMATE, opponent(self.to_move))
            #             return True
            if len(own_moves) == 0 : return True
        return False
    
    
    def is_stalemate(self):
        # enemy_color = opponent(self.to_move)
        if not self.is_checking():
            own_moves = self.possible_moves_color(self.to_move)
            # for move in own_moves:
            #     check_state = self.move(move,False)
            #     enemy_moves = check_state.possible_moves_color(enemy_color)
            #     for enemy_move in enemy_moves:
            #         if check_state.is_capture_king(enemy_move): 
            #             # self.result = Result(ResultType.STALEMATE)
                        
            if len(own_moves) ==0: return True
        return False
    
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
    
    def is_checking(self):
        return self.check
    
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
        
        self.castling_rights = [
            "K" in fen_castling_rights,
            "Q" in fen_castling_rights,
            "k" in fen_castling_rights,
            "q" in fen_castling_rights
        ]
        
        if fen_en_passant == "-":
            self.en_passant_target = None
        else:
            self.en_passant_target = parseCell(fen_en_passant)
        
        self.halfmove_clock = int(fen_halfmove)
        self.fullmove_number = int(fen_fullmove)
        # TODO: parse check state
        # TODO: parse game over state
    
    def getFEN(self) -> str:
        
        fen_board = ""
        count = 0
        for row in range(State.BOARD_SIZE):
            for col in range(State.BOARD_SIZE):
                piece = self.at(Cell(row, col))
                
                if piece == State.EMPTY_CELL:
                    if fen_board and fen_board[-1].isnumeric():
                        fen_board = fen_board[:-1] + str(int(fen_board[-1]) + 1)
                    else:
                        fen_board += "1"
                else:
                    fen_board += piece.getFEN()
                
                count += 1
                if count % 8 == 0 and count != 64:
                    fen_board += "/"
        
        fen_turn = "w" if self.to_move == PieceColor.WHITE else "b"
        
        fen_castling_rights = ""
        if self.castling_rights[0]:     fen_castling_rights += "K"
        if self.castling_rights[1]:     fen_castling_rights += "Q"
        if self.castling_rights[2]:     fen_castling_rights += "k"
        if self.castling_rights[3]:     fen_castling_rights += "q"
        if fen_castling_rights == "":   fen_castling_rights = "-"
        
        fen_en_passant = "-"
        if self.en_passant_target:
            fen_en_passant = self.en_passant_target.getFEN()
            
        fen_halfmove = str(self.halfmove_clock)
        fen_fullmove = str(self.fullmove_number)
        
        return " ".join([
            fen_board,
            fen_turn,
            fen_castling_rights,
            fen_en_passant,
            fen_halfmove,
            fen_fullmove
        ])    
    
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
        
        return board + "\n\nFEN: " + self.getFEN() + "\n"
    
    
    
    
    