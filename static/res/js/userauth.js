/* 
 * User authentication cli-side script for chat webapp project
 * Version: 1.0
 * Last Revision: 2020-05-31 by JacobDixon0
 * Authors: dev@jacobdixon.us (Jacob Dixon)
 */

window.addEventListener("load", function(){
    init();
})

function init(){
    initElements();
}

function initElements(){

    var returnButtons = document.getElementsByClassName("rt-btn");

    for (let i = 0; i < returnButtons.length; i++) {
        let bt = returnButtons[i]
        let sendTo = "/";

        if (bt.getAttribute("data-sendto") != null) {
            sendTo = bt.getAttribute("data-sendto");
        }

        bt.addEventListener("click", function() {
            window.location.href = sendTo;
        });
    }
}
