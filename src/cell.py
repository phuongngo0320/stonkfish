class Cell:
    
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
          
    def toLeft(self, distance: int = 1):
        return Cell(self.row, self.col - distance)
    
    def toRight(self, distance: int = 1):
        return Cell(self.row, self.col + distance)
    
    def toUp(self, distance: int = 1):
        return Cell(self.row - distance, self.col)
    
    def toDown(self, distance: int = 1):
        return Cell(self.row + distance, self.col)
    
    def getFEN(self):
        fen1 = str(9 - self.row)
        fen2 = chr(ord("a") + self.col)
        return fen1 + fen2
    
    def __repr__(self) -> str:
        pass
        