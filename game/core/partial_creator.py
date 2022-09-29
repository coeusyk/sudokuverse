import random

from game.core.constants import SIMPLE, MEDIUM, COMPLEX, POSITIONS
from game.core.solver import solution


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
    

    pos_for_partial = []
    for _ in range(num_of_clues):
        index = random.choice([i for i in POSITIONS if i not in pos_for_partial])

        pos_for_partial += [index]

    partial = [[0 for _ in range(9)] for _ in range(9)]
    for pos in pos_for_partial:
        partial[pos[0]][pos[1]] = input_sudoku[pos[0]][pos[1]]


    return partial


partial_board = create_partial(solution, difficulty=1)
