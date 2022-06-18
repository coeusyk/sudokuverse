const menuButton = document.getElementById("collapsible");
const menuContentButtons = document.getElementById("main-content").getElementsByTagName("button");

function openAndCollapse() {
    var menuContent_ = document.getElementById("menu-content");

    if (menuContent_.clientWidth != 0) {
        menuContent_.style.width = 0;
    }

    else {
        // Getting the maximum width of an element inside the div (in this case, the buttons) for changing the width of the div:
        menuContent_.style.width = menuContent_.scrollWidth + "px";
    };

};

function buttonClick(button_) {
    let index = Array.from(menuContentButtons).indexOf(button_);

    for (let i = 0; i < menuContentButtons.length; i++) {
        if (i != index) {
            menuContentButtons[i].className = "menu-options";
        }

        else {
            button_.className = "active_menu-options";
        };
    };

};

menuButton.addEventListener("click", openAndCollapse);

for (let button of menuContentButtons) {
    button.addEventListener("click", function() {buttonClick(button)});
};
