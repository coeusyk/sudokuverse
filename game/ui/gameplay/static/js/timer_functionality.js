var timer = document.getElementById("timer");
var pausePlayIcon = document.getElementById("pause-icon");


function updateTime(time_) {
    time_ += 1;

    var minutes = Math.floor((time_ / 60));
    var seconds =  time_ - (60 * minutes);

    if (seconds < 10) {
        timer.innerHTML = `${minutes}:0${seconds}`;
    } 

    else {
        timer.innerHTML = `${minutes}:${seconds}`;
    };

    return time_;

};


function stopTimer() {
    var enabledButtons = document.getElementsByClassName("enabled");

    if (enabledButtons.length == 0) {
        clearInterval(time);
    };

};


function pausePlay() {
    if (pausePlayIcon.src == "http://127.0.0.1:5000/ui/gameplay/images/pause.svg") {
        pausePlayIcon.src = "http://127.0.0.1:5000/ui/gameplay/images/play-fill.svg";
        paused = true;
    }

    else {
        pausePlayIcon.src = "http://127.0.0.1:5000/ui/gameplay/images/pause.svg";
        paused = false;
    };

};


var pausePlayButton = document.getElementById("pause-play");

pausePlayButton.addEventListener('click', pausePlay);


var current_time = 0;
var paused = false;


var time = setInterval(function() {
    if (!paused) {
        current_time = updateTime(current_time);
        stopTimer();
    };

}, 1000);
