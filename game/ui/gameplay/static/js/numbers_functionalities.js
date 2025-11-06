const numButtons = document.getElementsByClassName("numbers");
let cellWorkOrder = Array();


function addWork(cellAttr, action) {
    if (cellWorkOrder.length > 0) {
        const last = cellWorkOrder[cellWorkOrder.length - 1];

        const isSameEntry = (entryA, entryB) => {
            if (!Array.isArray(entryA) || !Array.isArray(entryB)) return entryA === entryB;

            const [cellA, actA] = entryA;
            const [cellB, actB] = entryB;

            if (actA !== actB) return false;

            // If the cell attributes are arrays (e.g. [cell, row, col]), compare elements
            if (Array.isArray(cellA) && Array.isArray(cellB)) {
                if (cellA.length !== cellB.length) return false;
                for (let i = 0; i < cellA.length; i++) {
                    if (cellA[i] !== cellB[i]) return false;
                }
                return true;
            }

            // Fallback to reference equality for non-array cell attributes (e.g. DOM element)
            return cellA === cellB;
        };

        if (!isSameEntry(last, [cellAttr, action])) {
            cellWorkOrder.push([cellAttr, action]);
        }
    }

    else {
        cellWorkOrder.push([cellAttr, action]);
    }
}


function checkNumCompletion(num) {
    /*
    Checks if the entered number has been used in every grid or not, and changes the styles of the number button accordingly
    */

    let count = 0;

    for (const grid of grids) {
        for (const cell of grid) {
            if (!(cell.className.includes("unfilled"))) {
                if (cell.innerHTML === num) {
                    count += 1;
                    break;
                }
            }
        }
    }

    let selectedButton = numButtons[parseInt(num) - 1];

    if (count === 9) {
        selectedButton.classList.remove("enabled")
        selectedButton.classList.add("disabled");

        selectedButton.disabled = true;
    }

    else {
        selectedButton.classList.remove("disabled")
        selectedButton.classList.add("enabled");

        selectedButton.disabled = false;
    }
}


function addNumber(button) {
    const selectedCellAttr_ = getCurCell();

    if (selectedCellAttr_ != null) {
        addWork(selectedCellAttr_, "+");

        const selectedCell = selectedCellAttr_[0];
        const rowIndex = selectedCellAttr_[1];
        const colIndex = selectedCellAttr_[2];

        selectedCell.classList.remove("unfilled");
        selectedCell.classList.add("filled");

        if (`${solution_[rowIndex][colIndex]}` === button.innerText) {
            selectedCell.innerHTML = solution_[rowIndex][colIndex]
            selectedCell.style.color = "rgb(233, 130, 39)";

            checkNumCompletion(selectedCell.innerText);
        }

        else {
            selectedCell.innerText = button.innerText;
            selectedCell.style.color = "rgb(255, 0, 0)";

            let mistakes = document.getElementById("mistakes").getElementsByClassName("coloured-text")[0];
            mistakes.innerText = `${parseInt(mistakes.innerText) + 1}`;

            if (mistakes.innerText === '3') {
                let gameOverBG = document.getElementsByClassName("game-over-bg")[0];
                gameOverBG.classList.add("shown");

                clearInterval(time);
            }
        }

        activateRowColGrid(selectedCell);  // From grid_functionalities.js
        activateNumCells(selectedCell);  // From grid_functionalities.js
        
        // Save game state after action
        if (typeof saveOnAction !== 'undefined') {
            saveOnAction();
        }
    }
}


for (let _num of numButtons) {
    _num.addEventListener('click', function() {checkNumCompletion(_num.innerHTML); addNumber(_num)})
}


// Initial Check:
for (let i = 1; i < 10; i++) {
    checkNumCompletion(i.toString());
}
