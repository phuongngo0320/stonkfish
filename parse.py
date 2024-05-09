# Player 1 move: a7a5.
# Player 2 move: f7f6.
# Player 1 move: e7e5.
# Player 2 move: a2a4.
# Player 1 move: h7h5.
# Player 2 move: f8a3.
# Player 1 move: b7b5.
# Player 2 move: g8e7.
# Player 1 move: c7c5.
# Player 2 move: b2b3.
# Player 1 move: h8f8.
# Player 2 move: e2e4.
# Player 1 move: b5a4.
# Player 2 move: f8h8.
# Player 1 move: h8h6.
# Player 2 move: d1e2.
# Player 1 move: h6h7.
# Player 2 move: c5c4.
# Player 1 move: a1a2.
# Player 2 move: e2d1.
# Player 1 move: g1h3.
# Player 2 move: c1b2.
# Player 1 move: d7d5.
# Player 2 move: b3a4.
# Player 1 move: f1c4.
# Player 2 move: e7c6.
# Player 1 move: b2a3.
# Player 2 move: c4d5.
# Player 1 move: e1g1.

cmd = [
    'from src.fen import parseMove',
    'from src.state import State',
    'board = State()'
]

with open("output.txt", "r") as f:
    
    while True:
        line = f.readline()
        if "Player" not in line: break
        move = line[15:-1]
        cmd += [f'board = board.move(parseMove("{move}"))']

cmd += ['print(board)', 'print(board.getFEN())']

with open("test.py", "w") as f:
    for c in cmd:
        f.write(c + "\n")

