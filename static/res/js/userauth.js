window.addEventListener("load", function () {
    init();
});

function init() {
    initElements();

    if (window.location.search.includes("invalid=bad_credentials")) {
        setInvalid("uname", true);
        setInvalid("passwd", true);
    }
}

function initElements() {
    document.getElementById("uname").onkeypress = function (e) {
        setInvalid("uname", false);
        setInvalid("passwd", false);
    };

    document.getElementById("passwd").onkeypress = function (e) {
        setInvalid("uname", false);
        setInvalid("passwd", false);
    };

    document.getElementById("cancel").addEventListener("click", function () {
        window.location.href = "/projects/apps/xe3/";
    });
}

function validate() {
    let valid = true;

    let username = document.getElementById("uname").value;
    let password = document.getElementById("passwd").value;

    if (username.length < 4) {
        setInvalid("uname", true);
        valid = false;
    }

    if (password.length < 4) {
        setInvalid("passwd", true);
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
