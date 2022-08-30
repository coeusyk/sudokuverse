import pulp as lp
import random

from constants import GRID_SIZE, MIN_NUMBER, MAX_NUMBER, GAME_NAME
from generator import generate_partial


class Sudoku:
    rows = range(MIN_NUMBER, MAX_NUMBER)
    cols = range(MIN_NUMBER, MAX_NUMBER)
    grids = range(MIN_NUMBER, MAX_NUMBER)
    values = range(1, 10)

    # Construct the board, with rows/columns and constraints
    def __init__(self):
        self.problem = lp.LpProblem(GAME_NAME)
        self.grid_vars = lp.LpVariable.dicts("grid_value", (self.rows, self.cols, self.values), cat='Binary')
        objective = lp.lpSum(0)

        self.problem.setObjective(objective)

        # 1: ensure only one value is filled for a cell
        for row in self.rows:
            for col in self.cols:
                values_ = [self.grid_vars[row][col][value] for value in self.values]
                constraint1 = lp.LpConstraint(e=lp.lpSum(values_), 
                    sense=lp.LpConstraintEQ, 
                    rhs=1, 
                    name=f"constraint_sum_{row}_{col}")

                self.problem.addConstraint(constraint1)

        # 2: ensure values from 1 to 9 is filled only once in a row
        for row in self.rows:
            for value in self.values:
                cols_ = [self.grid_vars[row][col][value] * value for col in self.cols]
                constraint2 = lp.LpConstraint(
                    e=lp.lpSum(cols_),
                    sense=lp.LpConstraintEQ, rhs=value,
                    name=f"constraint_uniq_row_{row}_{value}")

                self.problem.addConstraint(constraint2)

        # 3: ensure values from 1 to 9 is filled only once in a column
        for col in self.cols:
            for value in self.values:
                rows_ = [self.grid_vars[row][col][value] * value for row in self.rows]
                constraint3 = lp.LpConstraint(
                    e=lp.lpSum(rows_),
                    sense=lp.LpConstraintEQ, rhs=value,
                    name=f"constraint_uniq_col_{col}_{value}")

                self.problem.addConstraint(constraint3)

        # 4: ensure values from 1 to 9 is filled only once in the 3x3 grid
        for grid in self.grids:
            grid_row = int(grid / GRID_SIZE)
            grid_col = int(grid % GRID_SIZE)

            for value in self.values:
                number_ = [self.grid_vars[grid_row * GRID_SIZE + row][grid_col * GRID_SIZE + col][value] * value for col
                           in
                           range(MIN_NUMBER, GRID_SIZE) for row in range(MIN_NUMBER, GRID_SIZE)]

                constraint4 = lp.LpConstraint(e=lp.lpSum(number_),
                    sense=lp.LpConstraintEQ, rhs=value,
                    name=f"constraint_uniq_grid_{grid}_{value}")

                self.problem.addConstraint(constraint4)

    # Initialize puzzle with sample data (based on complexity)
    def init_puzzle(self, input_sudoku):
        for row in self.rows:
            for col in self.cols:
                if input_sudoku[row][col] != 0:
                    values_ = [self.grid_vars[row][col][value] * value for value in self.values]
                    pre_constraint = lp.LpConstraint(e=lp.lpSum(values_),
                                                     sense=lp.LpConstraintEQ, rhs=input_sudoku[row][col],
                                                     name=f"constraint_prefilled_{row}_{col}")
                                                     
                    self.problem.addConstraint(pre_constraint)

    # Attempt to solve, with supplied inputs and return solution; None otherwise
    def solve_puzzle(self):
        self.problem.solve()
        solution_status = lp.LpStatus[self.problem.status]

        if solution_status == 'Optimal':
            result = [[0 for col in self.cols] for row in self.rows]
            for row in self.rows:
                for col in self.cols:
                    for value in self.values:
                        if lp.value(self.grid_vars[row][col][value]):
                            result[row][col] = value
                            
            return result

        return None

    # Return the status of problem solved
    def status(self):
        return lp.LpStatus[self.problem.status]


# Print solution to console
def console_print_solution(matrix, rows, cols):
    print(f"\nFinal result:")

    if matrix is None:
        print("Nothing to print. Matrix is empty. Check 'status' on board.\n")
        return

    print("\n+ ----------- + ----------- + ----------- +", end="")
    for row in rows:
        print("\n", end="|  ")
        for col in cols:
            num_end = "  |  " if ((col + 1) % GRID_SIZE == 0) else "   "
            print(matrix[row][col], end=num_end)

        if (row + 1) % GRID_SIZE == 0:
            print("\n+ ----------- + ----------- + ----------- +", end="")

    print("\n")


file_path = generate_partial(max_filled = random.randint(0, 9))

with open(file_path, "r") as f:
    partial = [[int(t) for t in line.split()] for line in f]

board = Sudoku()
board.init_puzzle(input_sudoku=partial)

solution = board.solve_puzzle()
console_print_solution(solution, board.rows, board.cols)
