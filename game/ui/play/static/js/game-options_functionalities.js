const difficultyLevelCategory = document.getElementById("button-category");
const dLButtons = difficultyLevelCategory.getElementsByTagName("button");
var clickTimes = [0, 0, 0];

var diffInfo = document.getElementById("diff-info");
var playNowButton = document.getElementById("play-now-button");


function diffButtonClick(button_) {
    let index = Array.from(dLButtons).indexOf(button_);

    for (let i = 0; i < dLButtons.length; i++) {
        if (i != index) {
            dLButtons[i].className = "inactive-button";
            clickTimes[i] = 0;
        }

        else {
            if (clickTimes[i] > 0) {
                dLButtons[i].className = "inactive-button";
                clickTimes[i] = 0;

                playNowButton.disabled = true;
                playNowButton.style.backgroundColor = "#777777";
            } 
            
            else {
                dLButtons[i].className = "active-button";
                clickTimes[i]++;

                playNowButton.disabled = false;
                playNowButton.style.backgroundColor = "#E36950";
            };
        };
    };

};


function startGame() {
    if (playNowButton.disabled == false) {
        for (let button of dLButtons) {
            if (button.className == "active-button") {
                diffInfo.value = button.innerHTML;
                break;
            };
        };

        const playNowForm = document.getElementById("play-now-form");
        const formData = new FormData(playNowForm);
        const data = new URLSearchParams(formData);

        fetch(window.location.href, {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            },

            body: data
        })
            .then(response => response.json())
            .then(data => {
                if (data["redirect"] == true) {
                    window.location.href = "/gameplay";
                };
            })
    };

};


// Defaulting the difficulty level to Simple:
dLButtons[0].className = "active-button";
clickTimes[0]++;

playNowButton.disabled = false;
playNowButton.style.backgroundColor = "#E36950";


// Assigning event listeners to the dLButtons ('event delegation'):
difficultyLevelCategory.addEventListener('click', clickEvent => {
    if ((clickEvent.target.className == "inactive-button") | (clickEvent.target.className == "active-button")) {
        diffButtonClick(clickEvent.target);
    };
});

playNowButton.addEventListener('click', startGame);
