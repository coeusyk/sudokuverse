var eraseButton = document.getElementById("erase-button");
var hintButton = document.getElementById("hint-button");
var undoButton = document.getElementById("undo-button");
var notesButton = document.getElementById("notes-button");

var usedHints = 0;
const totalHints = 3;


function eraseFunctionality(cellAttr=null, undo=false) {
    if (cellAttr == null) {
        var currentCellAttr = getCurCell();
        console.log(true);
        console.log(currentCellAttr);
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
    if (usedHints < totalHints) {
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
                
                selectedCell.innerHTML = solution_[rowIndex][colIndex]
                selectedCell.style.color = "rgb(233, 130, 39)";

                checkNumCompletion(selectedCell.innerHTML);
                activateNumCells(selectedCell);  // From grid_functionalities.js

                if (!(undo)) {
                    usedHints += 1;
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


function notesFunctionality() {
    // Changing the notes identifier (OFF to ON and vice-versa):
    var nISpan = document.getElementById("n-i-span");
    if (nISpan.innerHTML == "OFF") {
        nISpan.innerHTML = "ON";
    } else {
        nISpan.innerHTML = "OFF";
    };

    // Changing the font size of all unfilled cells:
    for (i = 0; i < rows.length; i++) {
        Array.from(rows[i]).forEach(_div => {
            if (_div.className.includes("unfilled")) {
                _div.classList.toggle("notes");
            };
        });
    };

};


eraseButton.addEventListener('click', function() { eraseFunctionality(cellAttr=null, undo=false); });
hintButton.addEventListener('click', function() { hintFunctionality(cellAttr=null, undo=false); });
undoButton.addEventListener('click', undoFunctionality);
notesButton.addEventListener('click', notesFunctionality);
