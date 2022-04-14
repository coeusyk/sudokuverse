"""
Functions and classes for creating variables required for the project to work
"""

"""
class Board:
    def __init__(self, size: int = 9):
        self.size = size
        self.cells = [[Cell("X") for _ in range(size)] for _ in range(size)]

    def print(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.cells[i][j].get_value(), end=" ")

            print()

    def set_cell_val(self, row: int, column: int, value: str):
        if not (0 <= row < self.size) and not(0 <= column < self.size):
            raise IndexError(f"invalid row and column [row: {row}, column: {column}]")

        self.cells[column][row].set_value(value)


class Cell:
    def __init__(self, position: str):
        self.pos = position
        self.note = None

    def __repr__(self):
        if self.note is None:
            return self.pos
        else:
            return f"{self.pos} (Note: {self.note})"

    def set_value(self, val: str):
        self.pos = val

    def set_note(self, note: str):
        self.note = note

    def get_value(self):
        return self.pos


b = Board()

b.print()
print()
b.set_cell_val(3, 5, "Y")
b.print()
"""


class 
