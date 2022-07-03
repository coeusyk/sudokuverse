var menuContent = document.getElementById("menu-content");
var newUserContent = document.getElementById("new-user-content");
var optionsSpace = document.getElementById("options-space");

const mediaQuery1 = window.matchMedia('(max-width: 1200px)');
const mediaQuery2 = window.matchMedia('(max-width: 1700px)');


function mQ1Work(e) {
    if (e.matches) {
        menuContent.style.width = "0px";
    } 
    
    else {
        menuContent.style.width = "200px";
    };

};


function mQ2Work(e) {
    if (e.matches) {
        newUserContent.style.position = "relative";
        newUserContent.style.bottom = "0%";
        newUserContent.style.overflow = "visible";
        optionsSpace.style.display = "block";
    }

    else {
        newUserContent.style.position = "fixed";
        newUserContent.style.bottom = "11%";
        newUserContent.style.overflow = "hidden";
        optionsSpace.style.display = "none";
    };

};


mediaQuery1.addListener(mQ1Work);
mediaQuery2.addListener(mQ2Work);

// Initial checks:
mQ1Work(mediaQuery1);
mQ2Work(mediaQuery2);
