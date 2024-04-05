const eraseButton = document.getElementById("erase-button");
const hintButton = document.getElementById("hint-button");
const undoButton = document.getElementById("undo-button");

const hintsUsedDisplay = document.getElementById("hints-used");

let usedHints = 0;
const maxHints = parseInt(hintsUsedDisplay.innerText[hintsUsedDisplay.innerText.length - 1]);
const hintsUsedIdentifier = document.getElementById("h-u-span");


function eraseFunctionality(cellAttr=null, undo=false) {
    let currentCellAttr;

    if (cellAttr == null) {
        currentCellAttr = getCurCell();
    } else {
        currentCellAttr = cellAttr;
    }

    if (currentCellAttr != null) {
        if (!(undo)) {
            addWork(currentCellAttr, "-");  // From numbers_functionalities.js
        }

        const selectedCell = currentCellAttr[0];

        selectedCell.classList.remove("filled");
        selectedCell.classList.add("unfilled");

        activateRowColGrid(selectedCell);  // From grid_functionalities.js
        activateNumCells(selectedCell);  // From grid_functionalities.js

        checkNumCompletion(selectedCell.innerText);
    }
}


function hintFunctionality(cellAttr=null, undo=false) {
    let selectedCellAttr;

    if (usedHints < maxHints) {
        if (cellAttr == null) {
            selectedCellAttr = getCurCell();
        } else {
            selectedCellAttr = cellAttr;
        }

        if (selectedCellAttr != null) {
            if (!undo) {
                addWork(selectedCellAttr, "+");  // From numbers_functionalities.js
            }

            const [selectedCell, rowIndex, colIndex] = selectedCellAttr;

            if (selectedCell.className.includes("unfilled")) {
                selectedCell.classList.remove("unfilled");
                selectedCell.classList.add("filled");
                
                if (!undo) {
                    selectedCell.innerText = solution_[rowIndex][colIndex]  
                }

                if (selectedCell.innerText === `${solution_[rowIndex][colIndex]}`) {
                    selectedCell.style.color = "rgb(233, 130, 39)";
                } else {
                    selectedCell.style.color = "rgb(255, 0, 0)";
                }

                checkNumCompletion(selectedCell.innerText);
                activateNumCells(selectedCell);  // From grid_functionalities.js

                if (!(undo)) {
                    hintsUsedIdentifier.innerText = `${++usedHints}`;
                }
            }
        }
    }
}


function undoFunctionality() {
    let cellAttr;
    let action;

    if (cellWorkOrder.length > 0) {
        if (cellWorkOrder.length === 1) {
            action = cellWorkOrder[0][1];
            cellAttr = cellWorkOrder[0][0];
        } else {
            action = cellWorkOrder[cellWorkOrder.length - 1][1];
            cellAttr = cellWorkOrder[cellWorkOrder.length - 1][0];
        }

        let undo;

        if (action === "+") {
            eraseFunctionality(cellAttr, undo = true);
        } else {
            hintFunctionality(cellAttr, undo = true);
        }

        cellWorkOrder = cellWorkOrder.slice(0, (cellWorkOrder.length - 1));
    }

}


eraseButton.addEventListener('click', function() { eraseFunctionality(cellAttr=null, undo=false); });
hintButton.addEventListener('click', function() { hintFunctionality(cellAttr=null, undo=false); });
undoButton.addEventListener('click', undoFunctionality);
