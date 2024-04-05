const row1 = document.getElementsByClassName("row-1");
const row2 = document.getElementsByClassName("row-2");
const row3 = document.getElementsByClassName("row-3");
const row4 = document.getElementsByClassName("row-4");
const row5 = document.getElementsByClassName("row-5");
const row6 = document.getElementsByClassName("row-6");
const row7 = document.getElementsByClassName("row-7")
const row8 = document.getElementsByClassName("row-8")
const row9 = document.getElementsByClassName("row-9");

const col1 = document.getElementsByClassName("col-1")
const col2 = document.getElementsByClassName("col-2")
const col3 = document.getElementsByClassName("col-3")
const col4 = document.getElementsByClassName("col-4")
const col5 = document.getElementsByClassName("col-5")
const col6 = document.getElementsByClassName("col-6")
const col7 = document.getElementsByClassName("col-7")
const col8 = document.getElementsByClassName("col-8")
const col9 = document.getElementsByClassName("col-9");

const grid1 = document.getElementsByClassName("grid-1")
const grid2 = document.getElementsByClassName("grid-2")
const grid3 = document.getElementsByClassName("grid-3")
const grid4 = document.getElementsByClassName("grid-4")
const grid5 = document.getElementsByClassName("grid-5")
const grid6 = document.getElementsByClassName("grid-6")
const grid7 = document.getElementsByClassName("grid-7")
const grid8 = document.getElementsByClassName("grid-8")
const grid9 = document.getElementsByClassName("grid-9");

const rows = [row1, row2, row3, row4, row5, row6, row7, row8, row9];
const grids = [grid1, grid2, grid3, grid4, grid5, grid6, grid7, grid8, grid9];

const rowMap = new Map([
    ["row-1", row1], ["row-2", row2], ["row-3", row3],
    ["row-4", row4], ["row-5", row5], ["row-6", row6],
    ["row-7", row7], ["row-8", row8], ["row-9", row9]
]);

const colMap = new Map([
    ["col-1", col1], ["col-2", col2], ["col-3", col3],
    ["col-4", col4], ["col-5", col5], ["col-6", col6],
    ["col-7", col7], ["col-8", col8], ["col-9", col9]
]);

const gridMap = new Map([
    ["grid-1", grid1], ["grid-2", grid2], ["grid-3", grid3],
    ["grid-4", grid4], ["grid-5", grid5], ["grid-6", grid6],
    ["grid-7", grid7], ["grid-8", grid8], ["grid-9", grid9]
]);

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
