// Referenz zur grid-container-Div erhalten
const gridContainer = document.getElementById('grid-container');
const betButton  = document.getElementById('betButton');
const cashOutButton = document.getElementById('cashOutButton');
const betValue = document.getElementById('betValue');
const mineCount = document.getElementById('mineCount');

betButton.addEventListener('click', placeBet);
cashOutButton.addEventListener('click', cashOut);
cashOutButton.disabled = true;

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
            updateUserdata();
            addButtonGrid();
            betButton.disabled = true;
            cashOutButton.disabled = false;
        }
        else {
            alert(result);
        }
    })
}

async function cashOut() {
    fetch('/minesweeper/cashOut', {
        method: 'POST'})
    .then(async function (response) {
        let result = await response.text();
        if (result === "Cashed out 0.00") {
            alert("You Lost");
        }
        else alert(result);
    })
    .then(async function (response) {
        updateUserdata();
        document.getElementById('cashOutValue').innerText = '0';
        removeButtons();
        betButton.disabled = false;
        cashOutButton.disabled = true;
    })
}

async function buttonClicked(number, buttonRef) {
    console.log(`clicked ${number}`);
    fetch('/minesweeper/try', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            "pos": number
        })
    })
    .then(async function (response) {
        let result = await response.json();
        let multiplier = result[0];
        let cashoutVal = result[1];
        if (multiplier === 0) {
            await cashOut();
        }
        else {
            buttonRef.textContent = multiplier;
        document.getElementById('cashOutValue').innerText = cashoutVal.toString();
        alert("Multiplier: " + multiplier.toString() + " Cashout: " + cashoutVal.toString());
        }
    })
    .then(async function (response) {
        buttonRef.disabled = true;
    })
}

function addButtonGrid() {
    // Buttons dynamisch erzeugen und Event Listener hinzufügen
    for (let i = 0; i < 25; i++) {
    const button = document.createElement('button');
    button.textContent = '?';
    button.addEventListener('click', () => buttonClicked(i, button));

    const gridItem = document.createElement('div');
    gridItem.classList.add('grid-item');
    gridItem.appendChild(button);

    gridContainer.appendChild(gridItem);
    }
}

function removeButtons() {
    while (gridContainer.firstChild) {
        gridContainer.removeChild(gridContainer.firstChild);
    }
}