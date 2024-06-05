let flipButton = document.getElementById("flip");
let headButton = document.getElementById("head");
let tailButton = document.getElementById("tail");
let coin = document.getElementById("coin-img");

var choice = "head"

async function flip() {
    var result = "none";

    let img_tails = "data:image/jpeg;base64,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";
    let img_heads = "data:image/jpeg;base64,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"

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