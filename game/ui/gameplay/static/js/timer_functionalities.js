const timer = document.getElementById("timer");
const pausePlayIcon = document.getElementById("pause-icon");
const pausePlayButton = document.getElementById("pause-play");

const gridPausedContainer = document.getElementById("grid-container-2");

const quitGameBtn = document.getElementById("quit-game");

const difficultyChosen = document.getElementById("difficulty-chosen");


function updateTime(time_) {
    time_ += 1;

    const minutes = Math.floor((time_ / 60));
    const seconds = time_ - (60 * minutes);

    if (seconds < 10) {
        timer.innerText = `${minutes}:0${seconds}`;
    } else {
        timer.innerText = `${minutes}:${seconds}`;
    }

    return time_;
}


async function stopTimer(time_) {
    let operation;
    let isCompletion = false;
    const enabledButtons = document.getElementsByClassName("enabled");

    if (time_ == null) {
        operation = nextOperation(false);  // From game-over_functionalities.js
    }

    else if (enabledButtons.length === 0) {
        // Checking if all entered values are valid:
        let gameCompleted = true;
        for (let div of GridElements) {
            if (div.style.color === "rgb(255, 0, 0)") {
                gameCompleted = false;
                break;
            }
        }

        if (gameCompleted) {
            operation = nextOperation(true, time_);
            isCompletion = true;
        } else {
            return;
        }
    }

    else {
        return;
    }

    // Checking the operation to perform:
    if (typeof operation === "string") {
        if (isCompletion) {
            // Guest user completed the game: show completion modal (no stats post)
            clearInterval(time);
            showCompletionModal(difficultyChosen.innerText, time_, null); // From game-over_functionalities.js
        } else {
            // Guest user quit - clear game state and session before redirecting
            if (typeof clearGameState !== 'undefined') {
                clearGameState();
            }
            // Clear server-side session puzzle (await to ensure it completes)
            try {
                await fetch('/gameplay/clear-session', {method: 'POST'});
            } catch (error) {
                console.error('Failed to clear session:', error);
            }
            window.location.href = "/play";
        }
    } else {
        if (isCompletion) {
            // Logged-in user: post stats and show completion modal with best time
            clearInterval(time);
            sendData(operation, true, time_);  // From game-over_functionalities.js
        } else {
            // Logged-in user quit - clear state before posting
            if (typeof clearGameState !== 'undefined') {
                clearGameState();
            }
            sendData(operation, false, null);  // From game-over_functionalities.js
        }
    }
}


let paused;

function pausePlay() {
    const gameOptions = document.getElementById("play-options");

    if (pausePlayIcon.src.includes("/ui/gameplay/images/pause.svg")) {
        pausePlayIcon.src = "/ui/gameplay/images/play-fill.svg";
        paused = true;

        gridContainer.style.display = "none";
        gridPausedContainer.style.display = "grid";
        gameOptions.style.pointerEvents = "none";
    }

    else {
        pausePlayIcon.src = "/ui/gameplay/images/pause.svg";
        paused = false;

        gridContainer.style.display = "grid";
        gridPausedContainer.style.display = "none";
        gameOptions.style.pointerEvents = "auto";
    }
}


pausePlayButton.addEventListener('click', pausePlay);
quitGameBtn.addEventListener('click', function() { stopTimer(null) });

// Timer Functionality:
let current_time = 0;
paused = false;

const time = setInterval(function () {
    if (!paused) {
        current_time = updateTime(current_time);
        stopTimer(current_time);
    }
}, 1000);
