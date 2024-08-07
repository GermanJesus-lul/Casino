document.getElementById("hit").addEventListener("click", hit);
document.getElementById("stay").addEventListener("click", stay);
document.getElementById("start").addEventListener("click", start);
document.getElementById("restart").addEventListener("click", restart);
document.getElementById("decrementBetBy10").addEventListener("click", () => changeBetAmount(-10));
document.getElementById("decrementBetBy1").addEventListener("click", () => changeBetAmount(-1));
document.getElementById("incrementBetBy1").addEventListener("click", () => changeBetAmount(1));
document.getElementById("incrementBetBy10").addEventListener("click", () => changeBetAmount(10));

function changeBetAmount(amount) {
    const betAmountElement = document.getElementById("betAmount");
    const currentValue = parseInt(betAmountElement.value, 10);
    const newValue = currentValue + amount;
    if (newValue >= betAmountElement.min) {
        betAmountElement.value = newValue;
    }
}

async function hit() {
    // Send a GET request to the /hit route
    const response = await fetch('/black_jack/hit', { method: "GET" });
    // Parse the JSON response
    const gameState = await response.json();
    // Update the HTML elements with the new game state
    updateGameState(gameState);
}

async function stay() {
    // Send a GET request to the /stay route
    const response = await fetch('/black_jack/stay', { method: "GET" });
    // Parse the JSON response
    const gameState = await response.json();
    // Update the HTML elements with the new game state
    updateGameState(gameState);
}

async function restart() {
    const response = await fetch('/black_jack/restart', { method: "GET" });
    const gameState = await response.json();
    updateGameState(gameState);
}


async function start() {
    // Send a GET request to the /start route
    const response = await fetch('/black_jack/start', { method: "GET" });
    // Parse the JSON response
    const gameState = await response.json();
    // Update the HTML elements with the new game state
    updateGameState(gameState);
}

function updateGameState(gameState) {
    // Update dealer and player sums
    console.log("gameState", gameState)
    document.getElementById("sumDealer").textContent = gameState.dealerSum;
    document.getElementById("sumPlayer").textContent = gameState.playerSum;
    // Update the cards displayed for the dealer, clear existing cards first (except the hidden card)
    const dealerCardsContainer = document.getElementById("cardsDealer");
    while (dealerCardsContainer.children.length > 0) { // Keep the hidden card
        dealerCardsContainer.removeChild(dealerCardsContainer.lastChild);
    }
    if (gameState.state === 'gameOver'){
        const hiddenCardImg = document.createElement("img");
        hiddenCardImg.src = `/static/images/card_deck_black_jack/${gameState.hiddenCard}.svg`;
        hiddenCardImg.alt = gameState.hiddenCard;
        dealerCardsContainer.appendChild(hiddenCardImg);
    }
    else {
        const hiddenCardImg = document.createElement("img");
        hiddenCardImg.src = `/static/images/card_deck_black_jack/back.svg`;
        hiddenCardImg.alt = "back";
        dealerCardsContainer.appendChild(hiddenCardImg);

    }
    gameState.cardsDealer.forEach(card => {
        const img = document.createElement("img");
        img.src = `/static/images/card_deck_black_jack/${card}.svg`;
        img.alt = card;
        dealerCardsContainer.appendChild(img);
    });

    // Update the cards displayed for the player, clear existing cards first
    const playerCardsContainer = document.getElementById("cardsPlayer");
    while (playerCardsContainer.firstChild) {
        playerCardsContainer.removeChild(playerCardsContainer.firstChild);
    }
    gameState.cardsPlayer.forEach(card => {
        const img = document.createElement("img");
        img.src = `/static/images/card_deck_black_jack/${card}.svg`;
        img.alt = card;
        playerCardsContainer.appendChild(img);
    });

    // Clear any previous result
    document.getElementById("result").textContent = gameState.message;
    updateButtonStates(gameState);
}

function updateButtonStates(gameState) {
    const buttons = {
        hit: document.getElementById("hit"),
        stay: document.getElementById("stay"),
        start: document.getElementById("start"),
        restart: document.getElementById("restart"),
        decrementBetBy10: document.getElementById("decrementBetBy10"),
        decrementBetBy1: document.getElementById("decrementBetBy1"),
        incrementBetBy1: document.getElementById("incrementBetBy1"),
        incrementBetBy10: document.getElementById("incrementBetBy10")
    };
    for (const key in buttons) {
        buttons[key].disabled = true;
        buttons[key].style.backgroundColor = "grey";
        buttons[key].style.cursor = "default";
    }
        if (gameState.state === 'initial' || gameState.state === 'betting') {
        buttons.start.disabled = false;
        buttons.start.style.backgroundColor = '#8FB8DE';
        buttons.start.style.cursor = 'pointer';

        buttons.decrementBetBy10.disabled = false;
        buttons.decrementBetBy10.style.backgroundColor = '#8FB8DE';
        buttons.decrementBetBy10.style.cursor = 'pointer';

        buttons.decrementBetBy1.disabled = false;
        buttons.decrementBetBy1.style.backgroundColor = '#8FB8DE';
        buttons.decrementBetBy1.style.cursor = 'pointer';

        buttons.incrementBetBy1.disabled = false;
        buttons.incrementBetBy1.style.backgroundColor = '#8FB8DE';
        buttons.incrementBetBy1.style.cursor = 'pointer';

        buttons.incrementBetBy10.disabled = false;
        buttons.incrementBetBy10.style.backgroundColor = '#8FB8DE';
        buttons.incrementBetBy10.style.cursor = 'pointer';
    } else if (gameState.state === 'playing') {
        buttons.hit.disabled = false;
        buttons.hit.style.backgroundColor = '#8FB8DE';
        buttons.hit.style.cursor = 'pointer';

        buttons.stay.disabled = false;
        buttons.stay.style.backgroundColor = '#8FB8DE';
        buttons.stay.style.cursor = 'pointer';
    } else if (gameState.state === 'gameOver') {
        buttons.restart.disabled = false;
        buttons.restart.style.backgroundColor = '#8FB8DE';
        buttons.restart.style.cursor = 'pointer';
    }
}
