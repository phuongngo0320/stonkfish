# stonkfish

## Source Code

### Model

| File | Description |
|-|-|
| `cell.py` | Chess board square (FEN: a1, b2, f8...) |
| `chess.py` | Chess game model |
| `fen.py`| Parsing FEN strings into objects |
| `game.py` | Base game model |
| `move.py` | Chess move (FEN: a1a2, b1b8, ...) |
| `piece.py` | Chess piece (FEN: p, n, b, r, k, q) |
| `result.py` | Chess game result |
| `state.py` | Chess game state (FEN: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1)
| `vector.py` | Support direction abstraction (up, down, left, right...) |

### Algorithm

| File | Description |
|-|-|
| `evaluation.py` | Evaluation functions |
| `player.py` | Players (random, alpha-beta 1-10) |
| `strategy.py` | Search algorithm (alpha-beta cutoff) |

## Examples

### Overall

- The type of the board:
```py
state.board: list[list[Piece]]
```
See `piece.py` for piece format.

- Empty cells are stored as `Piece(PieceType.NONE)`. You can check for empty cells using:

```py
piece = State.EMPTY_CELL
state.is_empty_cell(piece) # True
```

- You can use `state.to_move` to get the turn (it is `PieceColor.WHITE` or `PieceColor.BLACK`)

### Get all legal moves

```py
state = State()
legal_moves = state.possible_moves()
```

### Chess move

WARNING: `state.move()` does not check for legal moves, you must use one of the moves from `state.possible_moves()`

```py
from src.state import State

# P1 moves pawn from e2 -> e4
# you can also use: move = parseMove("e2e4")
move = Move(Cell(6, 4), Cell(4, 4))

if move in legal_moves:
    state = state.move(move) # returns new state
```

### Check game status

```py
# check if game is over
if state.game_over():
    print(state.result) # check result.py for format
else:
    print("Game is not over yet")
```