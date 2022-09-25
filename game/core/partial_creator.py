import random

from constants import SIMPLE, MEDIUM, COMPLEX, POSITIONS
from solver import solution


def convert_to_board_pos(position: str):
    return


def create_partial(input_sudoku: list[list[int]], difficulty: int):
    if difficulty == 1:
        num_of_clues = random.choice(SIMPLE)
    
    elif difficulty == 2:
        num_of_clues = random.choice(MEDIUM)
    
    elif difficulty == 3:
        num_of_clues = random.choice(COMPLEX)
    
    else:
        param_error = "invalid parameter difficulty: expected number from 1 to 3"
        raise ValueError(param_error)
    
    
