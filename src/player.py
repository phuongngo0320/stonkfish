import random
from src.evaluation import evaluate_material
from src.game import Game
from src.state import State
from src.strategy import alpha_beta_cutoff_search

def random_player(game: Game, state: State):
    actions = game.actions(state)
    if actions:
        return random.choice(game.actions(state))
    return None

def leveled_player(level=1):
    
    def player(game: Game, state: State):
        return alpha_beta_cutoff_search(
            game, 
            state, 
            d=(level-1)*2 + 1, 
            cutoff_test=None, 
            eval_fn=evaluate_material
        )
    
    return player