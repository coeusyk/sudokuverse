const [menuSignUpButton, menuLoginButton] = document.getElementById("new-user-content").getElementsByTagName("button");
const [signUpModal, loginModal] = document.getElementsByClassName("modals");
const closeLogin = document.getElementsByClassName("close-button")[0];

const signUp = [menuSignUpButton], login = [menuLoginButton, closeLogin];
const buttons = [signUp, login];


function toggleModal(category_) {
    if (category_ === login) {
        if (signUpModal.className == "active-modal") {
            signUpModal.classList.toggle("active-modal");
        };

        loginModal.classList.toggle("active-modal");
    }

    else {
        if (loginModal.className == "active-modal") {
            loginModal.classlist.toggle("active-modal");
        };
        
        signUpModal.classList.toggle("active-modal");
    };

};


function windowOnClick(event) {
    if (event.target === loginModal) {
        toggleModal(login);
    }

    else if (event.target === signUpModal) {
        toggleModal(signUp);
    };

};


for (let category of buttons) {
    for (let element of category) {
        element.addEventListener("click", function() {toggleModal(category)});
    };
};

window.addEventListener("click", windowOnClick);
