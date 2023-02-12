const numButtons = document.getElementsByClassName("numbers");
var cellWorkOrder = Array();


function addWork(cellAttr, action) {
    if (cellWorkOrder.length > 0) {
        if (cellWorkOrder[-1] != [cellAttr, action]) {
            cellWorkOrder.push([cellAttr, action]);
        };
    }

    else {
        cellWorkOrder.push([cellAttr, action]);
    };

};


function checkNumCompletion(num) {
    /*
    Checks if the entered number has been used in every grid or not, and changes the styles of the number button accordingly
    */

    var count = 0;

    for (var grid of grids) {
        for (var cell of grid) {
            if (!(cell.className.includes("unfilled"))) {
                if (cell.innerHTML == num) {
                    count += 1;
                    break;
                };
            };
        };
    };

    selectedButton = numButtons[parseInt(num) - 1];

    if (count == 9) {
        selectedButton.classList.remove("enabled")
        selectedButton.classList.add("disabled");

        selectedButton.disabled = true;
    }

    else {
        selectedButton.classList.remove("disabled")
        selectedButton.classList.add("enabled");

        selectedButton.disabled = false;
    };

};


function addNumber(button) {
    var selectedCellAttr_ = getCurCell();

    if (selectedCellAttr_ != null) {
        addWork(selectedCellAttr_, "+");

        var selectedCell = selectedCellAttr_[0];
        var rowIndex = selectedCellAttr_[1];
        var colIndex = selectedCellAttr_[2];

        selectedCell.classList.remove("unfilled");
        selectedCell.classList.add("filled");

        if (solution_[rowIndex][colIndex] == button.innerText) {
            selectedCell.innerHTML = solution_[rowIndex][colIndex]
            selectedCell.style.color = "rgb(233, 130, 39)";

            checkNumCompletion(selectedCell.innerText);
        }

        else {
            selectedCell.innerText = button.innerText;
            selectedCell.style.color = "rgb(255, 0, 0)";

            let mistakes = document.getElementById("mistakes").getElementsByClassName("coloured-text")[0];
            mistakes.innerText = `${parseInt(mistakes.innerText) + 1}`;

            if (mistakes.innerText == '3') {
                let gameOverBG = document.getElementsByClassName("game-over-bg")[0];
                gameOverBG.classList.add("shown");

                clearInterval(time);
            };
        };

        activateRowColGrid(selectedCell);  // From grid_functionalities.js
        activateNumCells(selectedCell);  // From grid_functionalities.js
    };

};


for (let _num of numButtons) {
    _num.addEventListener('click', function() {checkNumCompletion(_num.innerHTML); addNumber(_num)})
};


// Initial Check:
for (let i = 1; i < 10; i++) {
    checkNumCompletion(i.toString());
};
