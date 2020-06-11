function init() {
    if (document.getElementById("rooms-list-container")) {
        fetch("/projects/apps/xe3/api/v1/rooms")
            .then((response) => response.text())
            .then((data) => {
                var json = JSON.parse(data);
                var rooms = json.rooms;

                if (rooms.length != 0) {
                    for (room of rooms) {
                        var roomBtn = document.createElement("a");
                        roomBtn.href = "/projects/apps/xe3/rooms/" + room.id;
                        roomBtn.classList.add("wide-block", "txt-centered");
                        roomBtn.innerHTML = room.id;
                        document.getElementById("rooms-list-container").appendChild(roomBtn);
                    }
                }
            });
    }
}

function createRoom() {
    var req = new XMLHttpRequest();
    req.open("POST", `/projects/apps/xe3/api/v1/rooms`, true);
    req.onreadystatechange = function () {
        if (req.status == 400) {
            console.log("could not create room");
        } else if (req.status == 201) {
            window.location.href = `/projects/apps/xe3/rooms/${req.responseText}`;
        }
    };
    req.send();
}

function joinRoom() {
    if (document.getElementById("join-room-id").value != "") {
        window.location.href = `/projects/apps/xe3/rooms/${document.getElementById("join-room-id").value}`;
    } else {
        window.location.href = "/projects/apps/xe3/rooms/public";
    }
}
