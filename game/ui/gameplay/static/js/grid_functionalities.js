const rows = Array.from({ length: 9 }, (_, i) => document.getElementsByClassName(`row-${i + 1}`));
const cols = Array.from({ length: 9 }, (_, i) => document.getElementsByClassName(`col-${i + 1}`));
const grids = Array.from({ length: 9 }, (_, i) => document.getElementsByClassName(`grid-${i + 1}`));

const rowMap = new Map(rows.map((row, i) => [`row-${i + 1}`, row]));
const colMap = new Map(cols.map((col, i) => [`col-${i + 1}`, col]));
const gridMap = new Map(grids.map((grid, i) => [`grid-${i + 1}`, grid]));

const gridContainer = document.getElementById("grid-container-1");

const GridElements = gridContainer.getElementsByTagName("div");
const Maps = [rowMap, colMap, gridMap];


function getCurAttributes(div) {
    const currentAttributes = [];

    for (let map of Maps) {
        for (let [key, value] of map.entries()) {
            if (div.className.includes(key)) {
                currentAttributes.push(value)
                break;
            }
        }
    }

    return currentAttributes;
}


function getCurCell() {
    let rowIndex = -1;
    let colIndex = -1;

    for (let row of rows) {
        rowIndex += 1;

        for (let cell of row) {
            colIndex += 1;

            if (cell.className.includes("active")) {
                return [cell, rowIndex, colIndex];
            }
        }

        if (colIndex === 8) colIndex = -1;
    }

    return null;
}


function activateRowColGrid(div) {
    const curRowColGrid = getCurAttributes(div);

    // Turning all cells to white bg initially:
    Array.from(GridElements).forEach(_div => {
        _div.style.backgroundColor = "white";
        _div.classList.remove("active");

        if (_div.className.includes("unfilled")) {
            _div.style.color = "white";
        }
    });

    for (let elem of curRowColGrid) {
        Array.from(elem).forEach(_div => {
            _div.style.backgroundColor = "rgb(255, 236, 185)";

            if (_div.className.includes("unfilled")) {
                _div.style.color = "rgb(255, 236, 185)";
            }
        });
    }
}


/**
 * Colourises all cells of the same number as of the selected cell
 * @param [div] The selected cell on the board
 */
function activateNumCells(div) {
    // Updating the current cell:
    div.style.backgroundColor = "#FFDD86";
    if (div.className.includes("unfilled")) {
        div.style.color = "#FFDD86";
    }

    if (div.className.includes("unfilled") || div.className.includes("filled")) {
        div.classList.add("active");
    }

    // Updating all the other cells (having the same number) row-wise:
    if (!(div.className.includes("unfilled")) || (div.style.color === "rgb(255, 0, 0)")) {
        let num = div.innerHTML;

        for (let i = 0; i < rows.length; i++) {
            Array.from(rows[i]).forEach(_div => {
                if ((_div.innerHTML === num) && (!(_div.className.includes("unfilled")))) {
                    _div.style.backgroundColor = "#FFDD86";
                }
            });
        }
    }
}


for (let div_ of GridElements) {
    div_.addEventListener('click', function() {
        activateRowColGrid(div_);
        activateNumCells(div_);
    });
}
