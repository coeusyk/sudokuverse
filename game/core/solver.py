import pulp as lp
import random

from game.core.constants import GRID_SIZE, GAME_NAME, ROWS, COLS, GRIDS
from game.core.solve_initialiser import gen_for_solve


class Sudoku:
    values = range(1, 10)

    # Constructing the board with rows/columns and constraints
    def __init__(self):
        self.problem = lp.LpProblem(GAME_NAME)
        self.grid_vars = lp.LpVariable.dicts("grid_value", (ROWS, COLS, self.values), cat='Binary')
        objective = lp.lpSum(0)

        self.problem.setObjective(objective)

        # 1: Ensuring only one value is filled for a cell:
        for row in ROWS:
            for col in COLS:
                values_ = [self.grid_vars[row][col][value] for value in self.values]
                constraint_1 = lp.LpConstraint(
                    e=lp.lpSum(values_), 
                    sense=lp.LpConstraintEQ, 
                    rhs=1, 
                    name=f"constraint_sum_{row}_{col}"
                )

                self.problem.addConstraint(constraint_1)

        # 2: Ensuring values from 1 to 9 are filled only once in a row:
        for row in ROWS:
            for value in self.values:
                cols_ = [self.grid_vars[row][col][value] * value for col in COLS]
                constraint_2 = lp.LpConstraint(
                    e=lp.lpSum(cols_),
                    sense=lp.LpConstraintEQ, rhs=value,
                    name=f"constraint_uniq_row_{row}_{value}"
                )

                self.problem.addConstraint(constraint_2)

        # 3: Ensuring values from 1 to 9 are filled only once in a column:
        for col in COLS:
            for value in self.values:
                rows_ = [self.grid_vars[row][col][value] * value for row in ROWS]
                constraint_3 = lp.LpConstraint(
                    e=lp.lpSum(rows_),
                    sense=lp.LpConstraintEQ, rhs=value,
                    name=f"constraint_uniq_col_{col}_{value}"
                )

                self.problem.addConstraint(constraint_3)

        # 4: Ensuring values from 1 to 9 are filled only once in the 3 x 3 grid:
        for grid in GRIDS:
            grid_row = int(grid / GRID_SIZE)
            grid_col = int(grid % GRID_SIZE)

            for value in self.values:
                number_ = [self.grid_vars[grid_row * GRID_SIZE + row][grid_col * GRID_SIZE + col][value] * value for col
                           in
                           range(GRID_SIZE) for row in range(GRID_SIZE)]

                constraint_4 = lp.LpConstraint(
                    e=lp.lpSum(number_),
                    sense=lp.LpConstraintEQ, rhs=value,
                    name=f"constraint_uniq_grid_{grid}_{value}"
                )

                self.problem.addConstraint(constraint_4)

    # Initializing puzzle with sample data (based on complexity):
    def init_puzzle(self, input_sudoku):
        for row in ROWS:
            for col in COLS:
                try:
                    if input_sudoku[row][col] != 0:
                        values_ = [self.grid_vars[row][col][value] * value for value in self.values]
                        pre_constraint = lp.LpConstraint(
                            e=lp.lpSum(values_),
                            sense=lp.LpConstraintEQ, rhs=input_sudoku[row][col],
                            name=f"constraint_prefilled_{row}_{col}"
                        )

                        self.problem.addConstraint(pre_constraint)
                except IndexError:
                    print(row, col)

    # Attempting to solve with supplied inputs, and return solution; None otherwise
    def solve_puzzle(self):
        self.problem.solve(lp.apis.PULP_CBC_CMD(msg=False))
        solution_status = lp.LpStatus[self.problem.status]

        if solution_status == 'Optimal':
            result = [[0 for _ in COLS] for _ in ROWS]
            for row in ROWS:
                for col in COLS:
                    for value in self.values:
                        if lp.value(self.grid_vars[row][col][value]):
                            result[row][col] = value
                            
            return result

        return None

    # Returning the status of problem solved:
    def status(self):
        return lp.LpStatus[self.problem.status]


def get_solution():
    file_path = gen_for_solve(max_filled=random.randint(0, 9))

    with open(file_path, "r") as f:
        lines = f.readlines()
        partial = [[int(t) for t in line.split()] for line in lines]

    board = Sudoku()
    board.init_puzzle(partial)

    solution = board.solve_puzzle()

    return solution
