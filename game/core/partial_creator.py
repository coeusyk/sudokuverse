import random

from game.core.constants import SIMPLE, MEDIUM, COMPLEX, POSITIONS, POS_GRIDS

my_dict = {"Simple": 1, "Medium": 2, "Complex": 3}


def create_puzzle(input_sudoku: list[list[int]], difficulty: int):
    """
    Generates a Sudoku puzzle by removing numbers from a solved Sudoku grid
    based on the specified difficulty level.

    Args:
        input_sudoku (list[list[int]]): A 9x9 solved Sudoku grid.
        difficulty (int): Difficulty level (1 for Simple, 2 for Medium, 3 for Complex).

    Returns:
        list[list[int]]: A 9x9 partially filled Sudoku grid representing the puzzle.

    Raises:
        ValueError: If the difficulty parameter is not between 1 and 3.
    """

    # Difficulty validation:
    if difficulty == 1:
        num_of_clues = random.choice(SIMPLE)
        clues_per_grid = 3
    
    elif difficulty == 2:
        num_of_clues = random.choice(MEDIUM)
        clues_per_grid = 2
    
    elif difficulty == 3:
        num_of_clues = random.choice(COMPLEX)
        clues_per_grid = 1
    
    else:
        param_error = "invalid parameter difficulty: expected number from 1 to 3"
        raise ValueError(param_error)

    # Puzzle creation:
    pos_for_partial = []

    for i in range(9):
        for _ in range(clues_per_grid):
            index = random.choice([j for j in POS_GRIDS[i] if j not in pos_for_partial])

            pos_for_partial += [index]
    
    for _ in range(num_of_clues - (clues_per_grid * 9)):
        index = random.choice([j for j in POSITIONS if j not in pos_for_partial])

        pos_for_partial += [index]

    partial = [[0 for _ in range(9)] for _ in range(9)]
    for pos in pos_for_partial:
        partial[pos[0]][pos[1]] = input_sudoku[pos[0]][pos[1]]

    return partial
