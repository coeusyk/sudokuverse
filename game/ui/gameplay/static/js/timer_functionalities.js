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


function stopTimer(time_) {
    let operation;
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
        } else {
            return;
        }
    }

    else {
        return;
    }

    // Checking the operation to perform:
    if (typeof operation === "string") {
        window.location.href = "/play";
    } else {
        sendData(operation, true);  // From game-over_functionalities.js
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
