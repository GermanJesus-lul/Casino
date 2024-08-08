// Referenz zur grid-container-Div erhalten
const gridContainer = document.getElementById('grid-container');
const betButton  = document.getElementById('betButton');
const cashOutButton = document.getElementById('cashOutButton');
const betValue = document.getElementById('betValue');
const mineCount = document.getElementById('mineCount');

betButton.addEventListener('click', placeBet)
cashOutButton.addEventListener('click', cashOut)


async function placeBet() {
    fetch('/minesweeper/newGame', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            "count": parseInt(mineCount.value),
            "bet": parseInt(betValue.value)
        })
    })
    .then(async function (response) {
        let result = await response.text();
        if (result === "minesweeper created") {
            // disable bet-area and show the cash-out-area
            alert("Created Game");
            document.getElementById('cashOutValue').innerText = betValue.value;
        }
        else alert(result);
    })
    .then(async function (response) {
        updateUserdata();
    })
}

async function cashOut() {
    fetch('/minesweeper/cashOut', {
        method: 'POST'})
    .then(async function (response) {
        let result = await response.text();
        alert(result);
    })
    .then(async function (response) {
        updateUserdata();
        document.getElementById('cashOutValue').innerText = '0';
    })
}

async function buttonClicked(number) {
    console.log(`clicked ${number}`);
    /*
    fetch('minesweeper/try', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            "pos": number
        })
    }).then(response => response.json())
        .then(async function (response) {
            response[0]
        })
    })
     */
}

// Buttons dynamisch erzeugen und Event Listener hinzufügen
for (let i = 0; i < 25; i++) {
    const button = document.createElement('button');
    button.textContent = i.toString();
    button.addEventListener('click', () => buttonClicked(i));

    const gridItem = document.createElement('div');
    gridItem.classList.add('grid-item');
    gridItem.appendChild(button);

    gridContainer.appendChild(gridItem);
}