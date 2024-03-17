const difficultyLevels = document.getElementById("diff-grid");

var returnBtn = document.getElementById("return-btn");


// Getting the next operation or data:
function nextOperation(success=false, time_=null) {
    const difficulty = difficultyChosen.innerText.toUpperCase();
    const data = {};

    if (!success) {
        if ((document.cookie.includes("__uuid")) && (!document.cookie.includes("logged-out"))) {
            data["hints-used"] = null;
            data["time-taken"] = null;
            data["game-result"] = 0;
            data["difficulty"] = difficulty;

            console.log(data);
        } else {
            return "redirect";
        }
    }

    else {
        if ((document.cookie.includes("__uuid")) && (!document.cookie.includes("logged-out"))) {
            data["hints-used"] = usedHints;
            data["time-taken"] = time_;
            data["game-result"] = 1;
            data["difficulty"] = difficulty;
        } else {
            return "redirect";
        }
    }

    return data;
}


// Sending game details to Python:
async function sendData(gameData, redirect=false) {
    const sdRequest = await fetch("/gameplay",
        {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },

            body: JSON.stringify(gameData)
        }
    );

    if (redirect) {
        const sdResponse = await sdRequest.json();
        if (sdResponse["info-added"] === true) {
            window.location.href = "/home";
        }
    }
}


function newGame(diffBtn) {
    const diffInfo = document.getElementById("diff-info");
    diffInfo.value = diffBtn.innerText.toUpperCase();

    const newGameForm = document.getElementById("new-game-form");
    const formData = new FormData(newGameForm);
    const data = new URLSearchParams(formData);

    async function reloadGame() {
        const rgRequest = await fetch(
            "/gameplay", {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },

                body: data
            }
        );

        if (rgRequest.status === 205) {
            document.location.reload();
        }
    }

    if ((document.cookie.includes("__uuid")) && (!document.cookie.includes("logged-out"))) {
        let gameStats = nextOperation(success=false, time_=null);
        sendData(gameStats);
    }

    reloadGame();

}


// Assigning event listeners to the diff-btns ('event delegation'):
difficultyLevels.addEventListener('click', clickEvent => {
    if (clickEvent.target.className === "diff-btns") {
        newGame(clickEvent.target);
    }
})

returnBtn.addEventListener('click', function() {
    stopTimer(null);  // From timer_functionalities.js
})
