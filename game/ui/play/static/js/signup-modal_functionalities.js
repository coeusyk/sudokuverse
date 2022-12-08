const signUpButton = document.getElementById("signup-button");
const formSignUp = document.getElementById("signup-form");

var dobHead = document.getElementById("dob-head");
var [unameNE, emailNE, phashNE] = document.getElementsByClassName("not-entered");

var phashInput = document.getElementById("phash-input");
var phashViewButton = document.getElementById("phash-view-toggle");

var showPhashIcon = document.getElementById("show-phash-icon");
var hidePhashIcon = document.getElementById("hide-phash-icon");

const unameErrorMap = {
    "not-entered": "Enter a username",
    "invalid-length": "Sorry, your username must be between 5 and 25 characters <br>long",
    "taken": "Sorry, this username is already taken"
};

const emailErrorMap = {
    "not-entered": "Enter an email",
    "invalid-length": "Sorry, your email must contain atmost 256 characters",
    "invalid-format": "Sorry, your email is invalid",
    "taken": "Sorry, this email is in use"
};

var invalidChar = "";
const phashErrorMap = {
    "not-entered": "Enter a password",
    "invalid-length": "Sorry, your password must contain atleast 6 characters",
    "invalid-format-1": `Sorry, your password cannot contain \'${invalidChar}\'`,
    "invalid-format-2": "Sorry, your password contains disallowed special characters"
};


function changeMargin() {
    // To-do
};


function showBasicPhashReq() {
    phashNE.color = "#777777";

    if (phashInput.value.length < 6) {
        phashNE.color = "#777777";
        phashNE.innerHTML = "Password must contain atleast 6 characters";
    } else {
        phashNE.innerHTML = "";
        phashNE.color = "rgb(255, 0, 0)";
    };

};


function signUpFunctionality() {
    const formData = new FormData(formSignUp);
    const data = new URLSearchParams(formData);

    // Sending form data to python:
    fetch("/play/guest", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        },

        body: data
    })
    .then(function showErrors() {
        // Setting the error messages:
        if (typeof unameValidity === "string") {
            unameNE.innerHTML = unameErrorMap[unameValidity];  // For username
        };

        if (typeof emailValidity === "string") {
            emailNE.innerHTML = emailErrorMap[emailValidity];  // For email
        };
        
        // For phash:
        if (Array.isArray(phashValidity)) {
            invalidChar = phashValidity[1];
            phashNE.innerHTML = phashErrorMap[phashValidity[0]]
        }

        else if (typeof phashValidity === "string") {
            phashNE.innerHTML = phashErrorMap[phashValidity];
        };
    });

};


function togglePhashView() {
    if (showPhashIcon.style.display != "none") {
        showPhashIcon.style.display = "none";
        hidePhashIcon.style.display = "block";

        phashInput.type = "text";
    } 
    
    else if (hidePhashIcon.style.display != "none") {
        hidePhashIcon.style.display = "none";
        showPhashIcon.style.display = "block";

        phashInput.type = "password";
    } 

    else {  // Mostly unreachable
        hidePhashIcon.style.display = "none";
        showPhashIcon.style.display = "block";

        phashInput.type = "password";
    };

};


// Event listeners:
signUpButton.addEventListener('click', signUpFunctionality);
phashInput.addEventListener('focus', function() {
    showBasicPhashReq();  // Initial check
    phashInput.addEventListener('keyup', showBasicPhashReq);
});

phashViewButton.addEventListener('click', togglePhashView);
