var eraseButton = document.getElementById("erase-button");
var hintButton = document.getElementById("hint-button");
var undoButton = document.getElementById("undo-button");

var hintsUsedDisplay = document.getElementById("hints-used");

var usedHints = 0;
var maxHints = parseInt(hintsUsedDisplay.innerText[hintsUsedDisplay.innerText.length - 1]);
var hintsUsedIdentifier = document.getElementById("h-u-span");


function eraseFunctionality(cellAttr=null, undo=false) {
    if (cellAttr == null) {
        var currentCellAttr = getCurCell();
    } else {
        var currentCellAttr = cellAttr;
    };

    if (currentCellAttr != null) {
        if (!(undo)) {
            addWork(currentCellAttr, "-");  // From numbers_functionalites.js
        };

        var selectedCell = currentCellAttr[0];

        selectedCell.classList.remove("filled");
        selectedCell.classList.add("unfilled");

        activateRowColGrid(selectedCell);  // From grid_functionalities.js
        activateNumCells(selectedCell);  // From grid_functionalites.js

        checkNumCompletion(selectedCell.innerHTML);
    };

};


function hintFunctionality(cellAttr=null, undo=false) {
    if (usedHints < maxHints) {
        if (cellAttr == null) {
            var selectedCellAttr = getCurCell();
        } else {
            var selectedCellAttr = cellAttr;
        };

        if (selectedCellAttr != null) {
            if (!undo) {
                addWork(selectedCellAttr, "+");  // From numbers_functionalites.js
            };

            var selectedCell = selectedCellAttr[0];
            var rowIndex = selectedCellAttr[1];
            var colIndex = selectedCellAttr[2];

            if (selectedCell.className.includes("unfilled")) {
                selectedCell.classList.remove("unfilled");
                selectedCell.classList.add("filled");
                
                selectedCell.innerText = solution_[rowIndex][colIndex]
                selectedCell.style.color = "rgb(233, 130, 39)";

                checkNumCompletion(selectedCell.innerText);
                activateNumCells(selectedCell);  // From grid_functionalities.js

                if (!(undo)) {
                    usedHints += 1;
                    hintsUsedIdentifier.innerText = usedHints;
                };
            };
        };
    };

};


function undoFunctionality() {
    if (cellWorkOrder.length > 0) {
        if (cellWorkOrder.length == 1) {
            var action = cellWorkOrder[0][1];
            var cellAttr = cellWorkOrder[0][0];
        } else {
            var action = cellWorkOrder[cellWorkOrder.length - 1][1];
            var cellAttr = cellWorkOrder[cellWorkOrder.length - 1][0];
        };

        if (action == "+") {
            eraseFunctionality(cellAttr, undo=true);
        } else {
            hintFunctionality(cellAttr, undo=true);
        };

        cellWorkOrder = cellWorkOrder.slice(0, (cellWorkOrder.length - 1));
    };

};


eraseButton.addEventListener('click', function() { eraseFunctionality(cellAttr=null, undo=false); });
hintButton.addEventListener('click', function() { hintFunctionality(cellAttr=null, undo=false); });
undoButton.addEventListener('click', undoFunctionality);
