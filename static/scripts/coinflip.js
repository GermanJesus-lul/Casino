flipButton = document.getElementById("flip");

async function flip() {
    const response = await fetch("/coinflip/flip");
    document.getElementById("result").innerText = await response.text();
}

flipButton.addEventListener('click', flip);