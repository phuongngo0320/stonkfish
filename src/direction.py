from enum import Enum

class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UPLEFT = (-1, -1)
    UPRIGHT = (-1, 1)
    DOWNLEFT = (1, -1)
    DOWNRIGHT = (1, 1)
    
DIRECTIONS = [ Direction(i) for i in range(len(Direction)) ]