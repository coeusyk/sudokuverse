var timer = document.getElementById("timer");
var pausePlayIcon = document.getElementById("pause-icon");
var pausePlayButton = document.getElementById("pause-play");

var gridPausedContainer = document.getElementById("grid-container-2");

var quitGameBtn = document.getElementById("quit-game");

var difficultyChosen = document.getElementById("difficulty-chosen");


function updateTime(time_) {
    time_ += 1;

    var minutes = Math.floor((time_ / 60));
    var seconds =  time_ - (60 * minutes);

    if (seconds < 10) {
        timer.innerHTML = `${minutes}:0${seconds}`;
    } else {
        timer.innerHTML = `${minutes}:${seconds}`;
    };

    return time_;

};


function stopTimer(time_) {
    var enabledButtons = document.getElementsByClassName("enabled");

    if (time_ == null) {
        var operation = nextOperation(success=false);  // From game-over_functionalities.js
    }

    else if (enabledButtons.length == 0) {
        // Checking if all entered values are valid:
        let gameCompleted = true;
        for (let div of GridElements) {
            if (div.style.color == "rgb(255, 0, 0)") {
                gameCompleted = false;
                break;
            };
        };

        if (gameCompleted) {
            var operation = nextOperation(success=true, time_=time_);
        } else {
            return;
        };
    }

    else {
        return;
    };

    // Checking the operation to perform:
    if (typeof operation === "string") {
        window.location.href = "/play";
    } else {
        sendData(operation, redirect=true);  // From game-over_functionalities.js
    };

};


function pausePlay() {
    var gameOptions = document.getElementById("play-options");

    if (pausePlayIcon.src == "http://127.0.0.1:5000/ui/gameplay/images/pause.svg") {
        pausePlayIcon.src = "http://127.0.0.1:5000/ui/gameplay/images/play-fill.svg";
        paused = true;

        gridContainer.style.display = "none";
        gridPausedContainer.style.display = "grid";
        gameOptions.style.pointerEvents = "none";
    }

    else {
        pausePlayIcon.src = "http://127.0.0.1:5000/ui/gameplay/images/pause.svg";
        paused = false;

        gridContainer.style.display = "grid";
        gridPausedContainer.style.display = "none";
        gameOptions.style.pointerEvents = "auto";
    };

};


pausePlayButton.addEventListener('click', pausePlay);
quitGameBtn.addEventListener('click', function() { stopTimer(null) });

// Timer Functionality:
var current_time = 0;
var paused = false;

var time = setInterval(function() {
    if (!paused) {
        current_time = updateTime(current_time);
        stopTimer(current_time);
    };

}, 1000);
