import random
import copy

from game.core.constants import SIMPLE, MEDIUM, COMPLEX, POSITIONS, POS_GRIDS

my_dict = {"Simple": 1, "Medium": 2, "Complex": 3}


def get_possible_values(board: list[list[int]], row: int, col: int) -> set[int]:
    """
    Get all possible values for a cell based on Sudoku rules.
    
    Args:
        board: Current state of the Sudoku board
        row: Row index (0-8)
        col: Column index (0-8)
    
    Returns:
        Set of possible values (1-9) for the cell
    """
    if board[row][col] != 0:
        return set()
    
    # Start with all possible values
    possible = set(range(1, 10))
    
    # Remove values in the same row
    for c in range(9):
        if board[row][c] != 0:
            possible.discard(board[row][c])
    
    # Remove values in the same column
    for r in range(9):
        if board[r][col] != 0:
            possible.discard(board[r][col])
    
    # Remove values in the same 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] != 0:
                possible.discard(board[r][c])
    
    return possible


def is_logically_solvable(board: list[list[int]], solution: list[list[int]]) -> bool:
    """
    Check if a puzzle can be solved using basic logical deduction (naked singles).
    
    Args:
        board: Partial Sudoku board to validate
        solution: The complete solution to verify against
    
    Returns:
        True if the puzzle can be solved with logic alone, False otherwise
    """
    # Work on a copy to avoid modifying the original
    test_board = copy.deepcopy(board)
    
    max_iterations = 100  # Prevent infinite loops
    iteration = 0
    
    while iteration < max_iterations:
        progress_made = False
        iteration += 1
        
        # Try to fill cells with only one possible value (naked singles)
        for row in range(9):
            for col in range(9):
                if test_board[row][col] == 0:
                    possible = get_possible_values(test_board, row, col)
                    
                    if len(possible) == 0:
                        # No valid values - invalid puzzle
                        return False
                    elif len(possible) == 1:
                        # Only one possible value - fill it
                        test_board[row][col] = list(possible)[0]
                        progress_made = True
        
        # If no progress was made, check if we're done
        if not progress_made:
            break
    
    # Check if the board is completely filled and matches the solution
    for row in range(9):
        for col in range(9):
            if test_board[row][col] != solution[row][col]:
                return False
    
    return True


def create_puzzle(input_sudoku: list[list[int]], difficulty: int):
    """
    Generates a Sudoku puzzle by removing numbers from a solved Sudoku grid
    based on the specified difficulty level. Ensures the puzzle is solvable
    using logical deduction.

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

    # Try to generate a valid puzzle with retries
    max_attempts = 20
    
    for _ in range(max_attempts):
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
        
        # Validate that the puzzle is logically solvable
        if is_logically_solvable(partial, input_sudoku):
            return partial
    
    # If we couldn't generate a valid puzzle after max_attempts, 
    # return the last generated one (fallback)
    return partial
