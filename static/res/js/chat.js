const ws = new WebSocket("ws://localhost:8090");

var messageHistory = [];

ws.addEventListener("open", function (event) {
    addMessage("Server", "Connected...", "server");
    updateMessageHistory();
});

ws.addEventListener("message", function (event) {
    if (event.data == "_update") {
        console.log("received update alert...");
        updateMessageHistory();
    }
});

ws.addEventListener("close", function (event) {
    addMessage("Server", "Disconnected...", "server");
});

document.addEventListener("keydown", function (event) {
    if (!event.shiftKey && event.keyCode == 13) {
        event.preventDefault();
        document.getElementById("submit").click();
    }
});

function addMessage(author, message, special) {
    var msgHistory = document.getElementById("message-history");
    var msgSpan = document.createElement("span");

    msgSpan.classList.add("message");
    if (special) msgSpan.classList.add(special);
    msgSpan.innerHTML = `<b>${author}:</b> ${message}`;

    msgHistory.appendChild(msgSpan);
}

function updateMessageHistory() {
    console.log("updating...");
    fetch("/api/v1/messages")
        .then((response) => response.text())
        .then((data) => {
            var json = JSON.parse(data);
            var messages = json.messages;

            console.log("parsing response...");

            for (message of messages) {
                if (!messageHistory.includes(message.id)) {
                    if (message.author == "admin") {
                        addMessage(message.author, message.content, "admin");
                    } else {
                        addMessage(message.author, message.content);
                    }
                    messageHistory.push(message.id);
                    console.log("adding message...");
                    document.getElementById("message-history").scrollTop = document.getElementById(
                        "message-history"
                    ).scrollHeight;
                }
            }
        });
}

function submit(event) {
    console.log("submitting message...");

    message = document.getElementById("message-field").value;

    var req = new XMLHttpRequest();
    req.open("POST", "/api/v1/messages", true);
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    var params = "message=" + message;

    if (message != "") {
        req.send(params);
        console.log("message sent...");
        document.getElementById("message-field").value = "";
        return true;
    }
}
