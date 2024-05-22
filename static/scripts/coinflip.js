let flipButton = document.getElementById("flip");
let headButton = document.getElementById("head");
let tailButton = document.getElementById("tail");

var choice = "head"

async function flip() {
    fetch("/coinflip/flip", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            "bet": document.getElementById("bet").value,
            "choice": choice
        })
    })
    .then(async function (response) {
        document.getElementById("result").innerText = await response.text();
    })
}

headButton.addEventListener("click", function () {
    choice = "head"
})
tailButton.addEventListener("click", function () {
    choice = "tail"
})
flipButton.addEventListener('click', flip);