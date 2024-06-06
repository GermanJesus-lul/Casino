let flipButton = document.getElementById("flip");
let headButton = document.getElementById("head");
let tailButton = document.getElementById("tail");
let coin = document.getElementById("coin-img");

var choice = "head"

async function flip() {
    var result = "none";

    let img_tails = "/static/images/tail.svg"
    let img_heads = "/static/images/head.svg"

    fetch("/coinflip/flip", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            "bet": document.getElementById("bet").value,
            "choice": choice
        })
    })
    .then(async function (response) {
        result = await response.text();
        if (result === "won") {
            if (choice === "head") {
                coin.src = img_heads;
            } else {
                coin.src = img_tails;
            }
        } else if (result === "lost") {
            if (choice === "head") {
                coin.src = img_tails;
            } else {
                coin.src = img_heads;
            }
        }
    })
    .then(async function (response) {
        updateUserdata()
    })
}

headButton.addEventListener("click", function () {
    choice = "head"
})
tailButton.addEventListener("click", function () {
    choice = "tail"
})
flipButton.addEventListener('click', flip);