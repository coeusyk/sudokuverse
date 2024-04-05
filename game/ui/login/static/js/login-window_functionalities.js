const phashInput = document.getElementsByClassName("login-inputs")[1];
const welcomeOrErrorBox = document.getElementsByClassName("welcome-or-error-box")[0];
const loginButton = document.getElementById("login-button");


function transitionErrorBox() {
    let executeTimes = 0;
    const errorTransition = setInterval(function () {
        if (executeTimes % 2 !== 0) {
            welcomeOrErrorBox.style.transform = "translateX(4px)";
        } else {
            welcomeOrErrorBox.style.transform = "translateX(-4px)";
        }

        executeTimes++;

        if (executeTimes === 5) {
            welcomeOrErrorBox.style.transform = "translateX(0px)";
            clearInterval(errorTransition);
        }

    }, 50);
}


async function loginFunctionality() {
    const formLogin = document.getElementById("login-form");

    const formData = new FormData(formLogin);
    const data = new URLSearchParams(formData);

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: data
        });

        const result = await response.json();

        if (result['success'] === false) {
            phashInput.value = "";

            // Changing the welcome box to error box:
            welcomeOrErrorBox.classList.add("error");

            const msg = welcomeOrErrorBox.querySelector("span");
            msg.innerText = "Invalid Email or Password";

            transitionErrorBox();
        } else {
            window.location.href = "/home";  // Redirecting to the home window
        }
    } catch (error) {
        console.error('Error:', error);
    }
}


loginButton.addEventListener('click', loginFunctionality);
