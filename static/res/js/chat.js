const ws = new WebSocket(`wss://${window.location.hostname}/projects/apps/xe3/api/ws`);
const room_id = document.getElementById("room-id").innerHTML;

var messageHistory = [];

ws.addEventListener("open", function (event) {
    addMessage("Server", "Connected...", "server");
    updateMessageHistory();
    setConnected(true);
});

ws.addEventListener("message", function (event) {
    if (event.data == "_UPDATE") {
        updateMessageHistory();
    } else if (event.data == "_CLS") {
        clearMessageHistory();
    }
});

ws.addEventListener("close", function (event) {
    addMessage("Server", "Disconnected...", "server");
    setConnected(false);
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
    msgSpan.innerHTML = `<b>${author}</b>: ${message}`;

    msgHistory.appendChild(msgSpan);
    document.getElementById("message-history").scrollTop = document.getElementById("message-history").scrollHeight;
}

function updateMessageHistory() {
    fetch(`/projects/apps/xe3/api/v1/rooms/${room_id}/messages`)
        .then((response) => response.text())
        .then((data) => {
            var json = JSON.parse(data);
            var messages = json.messages;

            for (message of messages) {
                if (!messageHistory.includes(message.id)) {
                    if (message.author == "admin") {
                        addMessage(message.author, message.content, "admin");
                    } else {
                        addMessage(message.author, message.content);
                    }
                    messageHistory.push(message.id);
                    removeTemp();
                }
            }
        });
}

function clearMessageHistory() {
    document.getElementById("message-history").innerHTML = "";
    messageHistory = [];
    addMessage("Server", "Message history was cleared by an administrator.", "server");
}

function submit(event) {
    message = document.getElementById("message-field").value;

    var req = new XMLHttpRequest();
    req.open("POST", `/projects/apps/xe3/api/v1/rooms/${room_id}/messages`, true);
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    req.onload = function () {
        if (req.status == 400) {
            addMessage("Server", "Message failed to send...", "server");
            setConnected(false);
            ws.close();
        }
    };

    var params = "message=" + message;

    if (message == "") {
        return;
    }

    if (message.trim() == "_DC") {
        ws.close();
    } else {
        addTemp(message);
        req.send(params);
        document.getElementById("message-field").value = "";
    }
}

function addTemp(message) {
    addMessage("you", message, "temp");
}

function removeTemp() {
    for (message of document.getElementById("message-history").childNodes) {
        if (message.classList.contains("temp")) {
            document.getElementById("message-history").removeChild(message);
        }
    }
}

function setConnected(connected) {
    document.getElementById("message-field").disabled = !connected;
    document.getElementById("submit").disabled = !connected;
    document.getElementById("message-field").placeholder = connected ? "message" : "message (disconnected)";
    document.getElementById("message-field").value = connected ? document.getElementById("message-field").value : "";
}
