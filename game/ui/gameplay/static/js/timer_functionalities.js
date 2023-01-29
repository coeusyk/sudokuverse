var timer = document.getElementById("timer");
var pausePlayIcon = document.getElementById("pause-icon");
var pausePlayButton = document.getElementById("pause-play");

var gridPausedContainer = document.getElementById("grid-container-2");

var quitGameBtn = document.getElementById("quit-game");


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


function stopTimer(time_=null) {
    var enabledButtons = document.getElementsByClassName("enabled");
    const data = {}

    if (enabledButtons.length == 0) {
        clearInterval(time);

        if (document.cookie.includes("__uuid")) {
            data["hints-used"] = usedHints,  
            data["time-taken"] = time_,
            data["game-result"] = 1
        } else {
            window.location.href = "/play"
        };
    }

    else if (time_ == null) {
        clearInterval(time);

        if (document.cookie.includes("__uuid")) {
            data["hints-used"] = null,  
            data["time-taken"] = null,
            data["game-result"] = 0
        } else {
            window.location.href = "/play";
        };
    };

    // Sending the game details to python:
    if ("game-result" in data) {
        fetch("/gameplay", {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },

            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(data => {
                if (data["info-added"] == true) {
                    window.location.href = "/home";
                };
            });
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
quitGameBtn.addEventListener('click', function() { stopTimer() });

// Timer Functionality:
var current_time = 0;
var paused = false;

var time = setInterval(function() {
    if (!paused) {
        current_time = updateTime(current_time);
        stopTimer(current_time);
    };

}, 1000);
