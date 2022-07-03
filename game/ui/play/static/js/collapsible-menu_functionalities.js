const menuButton = document.getElementById("collapsible");
const menuContentButtons = document.getElementById("main-content").getElementsByTagName("button");

const playButton = menuContentButtons[0];
playButton.className = "active_menu-options";


function openAndCollapse() {
    var menuContent_ = document.getElementById("menu-content")
    var newUserContent = document.getElementById("new-user-content");

    if (menuContent_.clientWidth != 0 && newUserContent.clientWidth != 0) {
        menuContent_.style.width = "0px";
        newUserContent.style.width = "0px";
    }

    else {
        menuContent_.style.width = "200px";
        newUserContent.style.width = "200px";
    };

};


function buttonClick() {
    let index = Array.from(menuContentButtons).indexOf(this);

    for (let i = 0; i < menuContentButtons.length; i++) {
        if (i != index) {
            menuContentButtons[i].className = "menu-options";
        }

        else {
            menuContentButtons[i].className = "active_menu-options";
        };
    };

};


menuButton.addEventListener('click', openAndCollapse);

for (let button of menuContentButtons) {
    button.addEventListener('click', buttonClick);
};
