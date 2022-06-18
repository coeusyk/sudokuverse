const difficultyLevelCategory = document.getElementsByClassName("button-category")[0];
const typeOfGameCategory = document.getElementsByClassName("button-category")[1];

// Getting the buttons inside each category:
const dLButtons = difficultyLevelCategory.getElementsByTagName("button");
const tOGButtons = typeOfGameCategory.getElementsByTagName("button");
const buttonArray = [dLButtons, tOGButtons];

const colorAfterClick = "#E36950";
const colorBeforeClick = "#2B2B2B";


function buttonClick(category, button_) {
    let index = Array.from(category).indexOf(button_);

    for (let i = 0; i < category.length; i++) {
        if (i != index) {
            category[i].className = "inactive-button";
        } 

        else {
            button_.className = "active-button";
        };
    };

};


// Looping through the elements of each collection:
for (let buttons of buttonArray) {
    for (let button of buttons) {
        button.addEventListener('click', function() {buttonClick(buttons, button)});
    };
};
