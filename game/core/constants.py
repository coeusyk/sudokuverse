MIN_NUMBER = 0
MAX_NUMBER = 9

GAME_NAME = "SudokuVerse"

GRID_SIZE = 3
ROWS = range(MIN_NUMBER, MAX_NUMBER)
COLS = range(MIN_NUMBER, MAX_NUMBER)
GRIDS = range(MIN_NUMBER, MAX_NUMBER)

POSITIONS = [f"{chr(65 + (j // 10))}{j % 10}" for j in range(1, 90) if j % 10 != 0]

PATH = "game/core/"

SIMPLE = range(30, 35)
MEDIUM = range(25, 30)
COMPLEX = range(20, 25)

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


create_cell_attributes()
