MIN_NUMBER = 0
MAX_NUMBER = 9

GAME_NAME = "SudokuVerse"

GRID_SIZE = 3
ROWS = range(MIN_NUMBER, MAX_NUMBER)
COLS = range(MIN_NUMBER, MAX_NUMBER)
GRIDS = range(MIN_NUMBER, MAX_NUMBER)

POSITIONS = [(j // 10, j % 10) for j in range(90) if (j % 10 != 9)]


PATH = "game/core/"

SIMPLE = range(31, 36)
MEDIUM = range(26, 31)
COMPLEX = range(21, 26)

CELL_ATTRIBUTES = [[] for _ in range(81)]


def create_cell_attributes():

    # Adding row number for all cells:
    temp = 1
    for i in range(1, 82):
        CELL_ATTRIBUTES[i - 1] += [temp]
        
        if i % 9 == 0:
            temp += 1

    # Adding column number for all cells:
    temp = 0
    for i in range(9):
        for j in range(1, 10):
            CELL_ATTRIBUTES[temp] += [j]

            temp += 1

    # Adding grid number for all cells:
    temp, g_num, row_grid_times = 0, 1, 0
    for i in range(1, 10):
        for j in range(3):
            CELL_ATTRIBUTES[temp] += [g_num]; CELL_ATTRIBUTES[temp + 1] += [g_num]; CELL_ATTRIBUTES[temp + 2] += [g_num]

            temp += 3; g_num += 1
        else:
            if i % 3 == 0:
                row_grid_times += 1
            
            g_num = (3 * row_grid_times) + 1
    
    # Adding div type number for all cells:
    temp = 0
    for i in range(1, 10):
        for j in range(1, 10):
            if i not in (4, 7):
                if (j % 3 == 0) and (j < 7):
                    CELL_ATTRIBUTES[temp] += [1]
                else:
                    CELL_ATTRIBUTES[temp] += [0]

            else:
                if (j % 3 == 0) and (j < 7):
                    CELL_ATTRIBUTES[temp] += [3]
                else:
                    CELL_ATTRIBUTES[temp] += [2]

            temp += 1


def get_grids():
    box_combinations, temp_b_combinations = [], []
    box_times, index, column_times = 0, 2, 2
    for _ in range(3):
        for _ in range(9):
            temp_b_combinations += [POSITIONS[index - 2], POSITIONS[index - 1], POSITIONS[index]]

            box_times += 1
            if box_times == 3:
                box_combinations += [temp_b_combinations]
                temp_b_combinations, box_times = [], 0

            index += 9
        else:
            index = (3 * column_times) - 1

        column_times += 1

    del temp_b_combinations, index, box_times, column_times

    return box_combinations


POS_GRIDS = get_grids()

create_cell_attributes()
