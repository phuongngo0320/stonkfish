from src.vector import Vector

class Cell:
    
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
            
    def translate(self, vec: Vector):
        return Cell(self.row + vec.rowax, self.col + vec.colax)
    
    def toLeft(self, distance: int = 1):
        return self.translate(Vector.left(distance))
    
    def toRight(self, distance: int = 1):
        return self.translate(Vector.right(distance))
    
    def toUp(self, distance: int = 1):
        return self.translate(Vector.up(distance))
    
    def toDown(self, distance: int = 1):
        return self.translate(Vector.down(distance))
    
    def toDownLeft(self, distance: int = 1):
        return self.translate(Vector.down_left(distance))
    
    def toDownRight(self, distance: int = 1):
        return self.translate(Vector.down_right(distance))

    def toUpLeft(self, distance: int = 1):
        return self.translate(Vector.up_left(distance))
    
    def toUpRight(self, distance: int = 1):
        return self.translate(Vector.up_right(distance))

    def getFEN(self):
        fen1 = str(8 - self.row)
        fen2 = chr(ord("a") + self.col)
        return fen2 + fen1
    
    def __repr__(self) -> str:
        pass
    
    def __eq__(self, value: object) -> bool:
        return self.row == value.row and self.col == value.col
    
    def __str__(self) -> str:
        return self.getFEN()
        