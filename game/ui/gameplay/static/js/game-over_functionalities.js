const difficultyLevels = document.getElementById("diff-grid");

const returnBtn = document.getElementById("return-btn");


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
async function sendData(gameData, showCompletion=false, timeTaken=null) {
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

    const sdResponse = await sdRequest.json();

    if (showCompletion && sdResponse["info-added"] === true) {
        // Show completion modal
        const difficulty = difficultyChosen.innerText;
        const bestTime = sdResponse["best-time"] || null;
        showCompletionModal(difficulty, timeTaken, bestTime);
    } else if (sdResponse["info-added"] === true) {
        // Just redirect for quit/game over
        deleteDiffCookie();
        window.location.href = "/home";
    }
}

function deleteDiffCookie() {
    if (document.cookie.split(';').some((item) => item.trim().startsWith('__diff='))) {
        document.cookie = "__diff=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/";
    }
}

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds - (60 * minutes);
    return secs < 10 ? `${minutes}:0${secs}` : `${minutes}:${secs}`;
}

function showCompletionModal(difficulty, timeTaken, bestTime) {
    const completionBg = document.querySelector('.completion-bg');
    const completionDifficulty = document.getElementById('completion-difficulty');
    const completionTime = document.getElementById('completion-time');
    const completionBestTime = document.getElementById('completion-best-time');
    const bestTimeRow = document.getElementById('best-time-row');
    
    // Set difficulty and time
    completionDifficulty.textContent = difficulty;
    completionTime.textContent = formatTime(timeTaken);
    
    // Show best time if available (for logged-in users)
    if (bestTime) {
        completionBestTime.textContent = bestTime;
        bestTimeRow.style.display = 'grid';
    } else {
        bestTimeRow.style.display = 'none';
    }
    
    // Show the modal
    completionBg.classList.add('completion-shown');
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
        let gameStats = nextOperation(false, null);
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

// Completion modal handlers
const completionDiffGrid = document.getElementById('completion-diff-grid');
const completionReturnBtn = document.getElementById('completion-return-btn');

function completionNewGame(diffBtn) {
    const diffInfo = document.getElementById('diff-info');
    diffInfo.value = diffBtn.innerText.toUpperCase();

    const newGameForm = document.getElementById('new-game-form');
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

    reloadGame();
}

function completionReturn() {
    deleteDiffCookie();
    
    if ((document.cookie.includes("__uuid")) && (!document.cookie.includes("logged-out"))) {
        window.location.href = "/home";
    } else {
        window.location.href = "/play";
    }
}

completionDiffGrid.addEventListener('click', clickEvent => {
    if (clickEvent.target.classList.contains('completion-diff-btns')) {
        completionNewGame(clickEvent.target);
    }
})

completionReturnBtn.addEventListener('click', completionReturn)
