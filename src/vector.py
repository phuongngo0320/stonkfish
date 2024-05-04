from enum import Enum
    
class Vector:    
    
    def __init__(self, rowax: int, colax: int) -> None:
        self.rowax = rowax
        self.colax = colax
        
    @staticmethod
    def up(weight = 1):
        return Vector(-weight, 0)
    
    @staticmethod
    def down(weight = 1):
        return Vector(weight, 0)
    
    @staticmethod
    def left(weight = 1):
        return Vector(0, -weight)
    
    @staticmethod
    def right(weight = 1):
        return Vector(0, weight)
    
    @staticmethod
    def up_left(weight = 1):
        return Vector(-weight, -weight)
    
    @staticmethod
    def up_right(weight = 1):
        return Vector(-weight, weight)
    
    @staticmethod
    def down_left(weight = 1):
        return Vector(weight, -weight)
    
    @staticmethod
    def down_right(weight = 1):
        return Vector(weight, weight)
    
UNIT_VECTORS = [
    Vector.up(),
    Vector.down(),
    Vector.left(),
    Vector.right(),
    Vector.up_left(),
    Vector.up_right(),
    Vector.down_left(),
    Vector.down_right()
]

ORTHOGONAL_UNIT_VECTORS = [
    Vector.up(),
    Vector.down(),
    Vector.left(),
    Vector.right()
]

DIAGONAL_UNIT_VECTORS = [
    Vector.up_left(),
    Vector.up_right(),
    Vector.down_left(),
    Vector.down_right()
]