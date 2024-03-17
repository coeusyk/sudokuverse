const signUpButton = document.getElementsByClassName("signup-button")[0];

const [unameError, dobError, emailError, phashError] = document.getElementsByClassName("input-errors");
const [unameInput, dobInput, emailInput, phashInput] = document.getElementsByClassName("signup-inputs");

const [dobSpace, emailSpace, phashSpace] = document.getElementsByClassName("input-space");
const signUpBtnSpace = document.getElementById("button-space");

const phashViewButton = document.getElementById("phash-view-toggle");

const showPhashIcon = document.getElementById("show-phash-icon");
const hidePhashIcon = document.getElementById("hide-phash-icon");

const unameErrorMap = {
    "not-entered": "Enter a username",
    "invalid-length": "Your username must be between 5 and 25 characters long",
    "invalid-format": "Only letters (a-z or A-Z) and numbers (0-9) are allowed",
    "taken": "This username is already taken"
};

const dobErrorMap = {
    "underage": "Unfortunately, you're too young",
    "overage": "Are you a superhuman? I have so many questions!",
    "invalid-age": "Did you come from the future? I have so many questions!",
    "invalid-format": "Are you sure that it is correct?"
}

const emailErrorMap = {
    "not-entered": "Enter an email",
    "invalid-length": "Your email must contain atmost 256 characters",
    "invalid-format": "Your email is invalid",
    "taken": "This email is in use"
};

let invalidChar = "";
const phashErrorMap = {
    "not-entered": "Enter a password",
    "invalid-length": "Your password must contain atleast 6 characters",
    "invalid-format-1": `Your password cannot contain \'${invalidChar}\'`,
    "invalid-format-2": "Your password contains disallowed special characters"
};

let phashErrorPrev = false;


function changeMargin() {
    // For the space between dob and the uname error:
    if (unameError.innerText === "") {
        dobSpace.style.height = "48px";
    } else if (!(unameError.innerHTML.includes("<br>"))) {
        dobSpace.style.height = "34px";
    } else {
        dobSpace.style.height = "20px";
    }

    // For the space between email and dob error:
    if (dobError.innerText === "") {
        emailSpace.style.height = "48px";
    } else if (!(dobError.innerHTML.includes("<br>"))) {
        emailSpace.style.height = "34px"
    } else {
        emailSpace.style.height = "20px";
    }

    // For the space between phash and email error:
    if (emailError.innerText === "") {
        phashSpace.style.height = "48px";
    } else {
        phashSpace.style.height = "34px";
    }

    // For the space between signup button and phash error:
    if (phashError.innerText === "") {
        signUpBtnSpace.style.height = "34px";
    } else {
        signUpBtnSpace.style.height = "20px";
    }
}


function changeInputBorder() {
    // For the username input:
    if (unameError.innerText !== "") {
        unameInput.style.borderColor = "rgb(255, 0, 0)";  // Red in rgb format
    } else {
        unameInput.style.borderColor = "rgb(43, 43, 43)";  // #2B2B2B in rgb format
    }

    // For the dob input:
    if (dobError.innerText !== "") {
        dobInput.style.borderColor = "rgb(255, 0, 0)";
    } else {
        dobInput.style.borderColor = "rgb(43, 43, 43)";
    }

    // For the email input:
    if (emailError.innerText !== "") {
        emailInput.style.borderColor = "rgb(255, 0, 0)";
    } else {
        emailInput.style.borderColor = "rgb(43, 43, 43)";
    }

    // For the phash input:
    if (phashError.innerText !== "") {
        phashInput.style.borderColor = "rgb(255, 0, 0)";
    } else {
        phashInput.style.borderColor = "rgb(43, 43, 43)";
    }
}


function showBasicPhashReq() {
    if (phashErrorPrev === false) {
        if (phashInput.value.length < 6) {
            phashError.style.color = "#777777";
            phashError.innerText = "Password must contain atleast 6 characters";
        } else {
            phashError.innerText = "";
            phashError.style.color = "rgb(255, 0, 0)";
        }
    }

    changeMargin();
}


function enableSignUpBtn() {
    if ((unameInput.value !== "") && (emailInput.value !== "") && (phashInput.value !== "")) {
        signUpButton.disabled = false;
        signUpButton.classList.remove("disabled");
    } else {
        signUpButton.disabled = true;
        signUpButton.classList.add("disabled");
    }
}


function signUpFunctionality() {
    const formSignUp = document.getElementById("signup-form");

    const formData = new FormData(formSignUp);
    const data = new URLSearchParams(formData);

    // Sending form data to python:
    fetch("/signup", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        },

        body: data
    })
        .then(request => request.json())
        .then(data => {
            if (data["success"] === false) {
                // Accessing the data sent:
                if ("username" in data) {
                    unameError.innerText = unameErrorMap[data["username"]];
                }
                
                if ("dob" in data) {
                    dobError.innerText = dobErrorMap[data["dob"]];
                }
                
                if ("email" in data) {
                    emailError.innerText = emailErrorMap[data["email"]];
                }
                
                if ("phash" in data) {
                    phashErrorPrev = true;
                    if (Array.isArray(data["phash"])) {
                        invalidChar = data["phash"][1];
                        phashError.innerText = phashErrorMap[data["phash"][0]];
                    } else {
                        phashError.innerText = phashErrorMap[data["phash"]];
                    }
                }

                changeMargin();
                changeInputBorder();
            }
            
            else {
                window.location.href = "/home";  // Redirecting the user to the home window
            }
        });
}


function togglePhashView() {
    if (showPhashIcon.style.display !== "none") {
        showPhashIcon.style.display = "none";
        hidePhashIcon.style.display = "block";

        phashInput.type = "text";
    }
    
    else if (hidePhashIcon.style.display !== "none") {
        hidePhashIcon.style.display = "none";
        showPhashIcon.style.display = "block";

        phashInput.type = "password";
    } 

    else {  // Mostly unreachable
        hidePhashIcon.style.display = "none";
        showPhashIcon.style.display = "block";

        phashInput.type = "password";
    }
}


// Event listeners:
signUpButton.addEventListener('click', function() { 
    signUpFunctionality();
});

phashInput.addEventListener('focus', function() {
    showBasicPhashReq();  // Initial check
    phashInput.addEventListener('keyup', showBasicPhashReq);
});

phashViewButton.addEventListener('click', togglePhashView);

window.addEventListener('keyup', enableSignUpBtn);
window.addEventListener('click', enableSignUpBtn);

// Initial checks:
changeMargin();
enableSignUpBtn();
