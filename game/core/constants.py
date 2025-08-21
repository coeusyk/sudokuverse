"""
All project constants are defined here to make any changes done here 
to be reflected everywhere
"""

import datetime
import json
import pathlib

from flask import Response


MAX_NUMBER = 9

GAME_NAME = "SudokuVerse"

GRID_SIZE = 3
ROWS = range(MAX_NUMBER)
COLS = range(MAX_NUMBER)
GRIDS = range(MAX_NUMBER)
NUMBERS = range(1, MAX_NUMBER + 1)

POSITIONS = [(j // 10, j % 10) for j in range(90) if (j % 10 != 9)]

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
PATH = "game/core/"

NUM_OF_DIFFICULTIES = 3
SIMPLE = range(35, 39)
MEDIUM = range(29, 33)
COMPLEX = range(23, 27)

DIFFICULTY_DICT = {"SIMPLE": 1, "MEDIUM": 2, "COMPLEX": 3}

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
            CELL_ATTRIBUTES[temp] += [g_num]
            CELL_ATTRIBUTES[temp + 1] += [g_num]
            CELL_ATTRIBUTES[temp + 2] += [g_num]

            temp += 3
            g_num += 1

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
            temp_b_combinations += [
                POSITIONS[index - 2], POSITIONS[index - 1], POSITIONS[index]
            ]

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

# Responses:
DIFF_RESP = Response(json.dumps({"redirect": True}), status=302)  # Start game

# Cookie names:
USER_IDENTIFIER = "__uuid"
DIFF_CHOSEN = "__diff"

COOKIE_EXPIRATION_TIME = datetime.timedelta(days=30)
