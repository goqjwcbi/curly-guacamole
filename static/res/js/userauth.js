/* 
 * User authentication cli-side script for chat webapp project
 * Version: 1.0
 * Last Revision: 2020-05-31 by JacobDixon0
 * Authors: dev@jacobdixon.us (Jacob Dixon)
 */

window.addEventListener("load", function() {
    init();
})

function init() {
    initElements();

    if (window.location.search.includes("invalid=uname_taken")) {
        setInvalid("username", true);
    } else if (window.location.search.includes("invalid=bad_credentials")) {
        setInvalid("username", true);
        setInvalid("password", true);
    }
}

function initElements() {
    document.getElementById("username").onkeypress = function(e) {
        setInvalid("username", false);
        setInvalid("password", false);
    }

    document.getElementById("password").onkeypress = function(e) {
        setInvalid("username", false);
        setInvalid("password", false);
    }

    document.getElementById("rt-btn").addEventListener("click", function() {
        window.location.href = "/";
    });
}

function validate(){
    let valid = true;

    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    if (username.length < 4){
        setInvalid("username", true);
        valid = false;
    }
    
    if (password.length < 4){
        setInvalid("password", true);
        valid = false;
    }

    return valid;
}

function setInvalid(id, isValid) {
    if (isValid) {
        document.getElementById(id).classList.add("invalid");
        document.getElementById("invalid-" + id).hidden = false;
    } else {
        document.getElementById(id).classList.remove("invalid");
        document.getElementById("invalid-" + id).hidden = true;
    }
}
