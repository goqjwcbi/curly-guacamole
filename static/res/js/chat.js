const ws = new WebSocket("ws://localhost:8090");

var messageHistory = [];

ws.addEventListener("open", function (event) {
    addMessage("Server", "Connected...", true);
    updateMessageHistory();
});

ws.addEventListener("message", function (event) {
    if (event.data == "_update") {
        updateMessageHistory();
    }
});

ws.addEventListener("close", function (event) {
    addMessage("Server", "Disconnected...", true);
});

document.addEventListener("keydown", function (event) {
    if (!event.shiftKey && event.keyCode == 13) {
        event.preventDefault();
        document.getElementById("submit").click();
    }
});

function addMessage(author, message, isServer) {
    var msgHistory = document.getElementById("message-history");
    var msgSpan = document.createElement("span");

    msgSpan.classList.add("message");
    if (isServer) msgSpan.classList.add("server");
    msgSpan.innerHTML = `<b>${author}:</b> ${message}`;

    msgHistory.appendChild(msgSpan);
}

function updateMessageHistory() {
    fetch("/api/v1/messages")
        .then((response) => response.text())
        .then((data) => {
            var json = JSON.parse(data);
            var messages = json.messages;

            for (message of messages) {
                if (!messageHistory.includes(message.id)) {
                    addMessage(message.author, message.content, false);
                    messageHistory.push(message.id);
                }
            }
        });

    document.getElementById("message-history").scrollTop = document.getElementById("message-history").scrollHeight;
}

function submit(event) {
    message = document.getElementById("message-field").value;

    var req = new XMLHttpRequest();
    req.open("POST", "/api/v1/messages", true);
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    var params = "message=" + message;

    if (message != "") {
        req.send(params);
        document.getElementById("message-field").value = "";
        return true;
    }
}
