import random

from constants import MAX_NUMBER, PATH


def generate_partial(max_filled: int = 9):
    if not (-1 < max_filled < 10):
        msg = "invalid max_filled: expected number in 0 to 9"
        raise ValueError(msg)

    current_path = PATH + "partial_sudoku.txt"
    with open(current_path, "w") as f:
        positions = [i for i in range(MAX_NUMBER)]
        values = [i for i in range(1, 10)]

        for i in range(MAX_NUMBER):
            if i <= max_filled:
                pos, value = random.choice(positions), random.choice(values)
                row = []

                for j in range(MAX_NUMBER):
                    if j == pos:
                        row += [str(value)]
                    else:
                        row += ["0"]
                else:
                    positions.remove(pos); values.remove(value)
            
            else:
                row = ["0" for _ in range(MAX_NUMBER)]
            
            f.write(f"{' '.join(row)}\n")
    
    return current_path
