document.getElementById("hit").addEventListener("click", hit);
document.getElementById("stay").addEventListener("click", stay);
document.getElementById("start").addEventListener("click", start);
document.getElementById("restart").addEventListener("click", restart)
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
    document.getElementById("sumDealer").textContent = gameState.dealerSum;
    document.getElementById("sumPlayer").textContent = gameState.playerSum;
    // Update the cards displayed for the dealer, clear existing cards first (except the hidden card)
    const dealerCardsContainer = document.getElementById("cardsDealer");
    while (dealerCardsContainer.children.length > 0) { // Keep the hidden card
        dealerCardsContainer.removeChild(dealerCardsContainer.lastChild);
    }
    if (gameState.hiddenCard !== null){
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
}
