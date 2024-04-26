import random
from src.game import Game

def random_player(game: Game, state):
    actions = game.actions(state)
    if actions:
        return random.choice(game.actions(state))
    return None

# TODO: AI players with different levels (1-10)