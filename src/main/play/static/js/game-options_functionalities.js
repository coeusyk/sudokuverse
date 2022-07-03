const difficultyLevelCategory = document.getElementsByClassName("button-category")[0];
const typeOfGameCategory = document.getElementsByClassName("button-category")[1];

// Getting the buttons inside each category:
const dLButtons = difficultyLevelCategory.getElementsByTagName("button");
const tOGButtons = typeOfGameCategory.getElementsByTagName("button");
const buttonArray = [dLButtons, tOGButtons];

const clickTimes1 = [0, 0, 0]; const clickTimes2 = [0, 0, 0];

function buttonClick(category, button_) {
    let index = Array.from(category).indexOf(button_);
    if (category === dLButtons) {
        var clickT = clickTimes1;
    } else {
        var clickT = clickTimes2;
    };

    for (let i = 0; i < category.length; i++) {
        if (i != index) {
            category[i].className = "inactive-button";
            clickT[i] = 0;
        } 

        else {
            if (clickT[i] > 0) {
                category[i].className = "inactive-button";
                clickT[i] = 0;
            } else {
                category[i].className = "active-button";
                clickT[i]++;
            }
        };
    };

};


// Looping through the elements of each collection:
for (let buttons of buttonArray) {
    for (let button of buttons) {
        button.addEventListener('click', function() {buttonClick(buttons, button)});
    };
};
