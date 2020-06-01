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
    document.getElementById("rt-btn").addEventListener("click", function() {
        window.location.href = "/";
    });
}
