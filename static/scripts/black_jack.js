// Event Listeners
document.getElementById("hit").addEventListener("click", hit);
document.getElementById("stay").addEventListener("click", stay);
document.getElementById("start").addEventListener("click", start);
document.getElementById("restart").addEventListener("click", restart);
document.getElementById("decrementBetBy10").addEventListener("click", () => changeBetAmount(-10));
document.getElementById("decrementBetBy1").addEventListener("click", () => changeBetAmount(-1));
document.getElementById("incrementBetBy1").addEventListener("click", () => changeBetAmount(1));
document.getElementById("incrementBetBy10").addEventListener("click", () => changeBetAmount(10));
document.addEventListener("DOMContentLoaded",  setInitialState);



//Utility Functions


// Change the bet amount by a specified value
function changeBetAmount(amount) {
    const betAmountElement = document.getElementById("betAmount");
    const currentValue = parseInt(betAmountElement.value, 10);
    const newValue = currentValue + amount;
    if (newValue >= betAmountElement.min) {
        betAmountElement.value = newValue;
    }
}


//Validate if the data is a valid game state
function isGameState(data) {
    return (typeof data.message === 'string') && (
        (typeof data.state === 'string' &&
        (typeof data.dealerSum === 'number' || data.dealerSum === '?' || data.dealerSum === null) &&
        (typeof data.playerSum === 'number' || data.playerSum === null) &&
        (Array.isArray(data.cardsDealer) || data.cardsDealer === null) &&
        (Array.isArray(data.cardsPlayer) || data.cardsPlayer === null) &&
        (typeof data.hiddenCard === 'string' || data.hiddenCard === null))
    );
}



// Main Game Functions


// Start a new game with the specified bet amount
async function start() {
    try {
        const betAmountElement = document.getElementById("betAmount");
        const betAmount = parseInt(betAmountElement.value, 10);

        // Validate bet amount
        if (isNaN(betAmount) || betAmount < 1) {
            throw new Error("Invalid bet amount");
        }

        // Send request to start a new game
        const response = await fetch('/black_jack/start', {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({"bet":  betAmount })
        });

        // Parse the response
        const gameState = await response.json();

        // Handle the different response statuses
        if (response.status === 400) {
            document.getElementById("result").textContent = gameState.message;
        } else if  (!response.ok) {
            throw new Error(`Network response was not ok`);
        } else if (isGameState(gameState)){
            updateGameState(gameState);
        } else {
            throw new Error('Invalid game state data')
        }
    } catch (error) {
        console.error('Error during start:', error);
        if (error.message === "Invalid bet amount") {
            document.getElementById("result").textContent = "Bet amount must be greater than 0.";
        } else {
            document.getElementById("result").textContent = "An error occurred while starting.";
        }
    }
}


// Player hits and draws a card
async function hit() {
    try {
        // Send request to hit
        const response = await fetch('/black_jack/hit', {method: "POST"});

        // Check if response is ok
        if (!response.ok) {
            throw new Error(`Network response was not ok`);
        }

        // Parse the response
        const gameState = await response.json();

        // Validate and update game state
        if (isGameState(gameState)) {
            updateGameState(gameState);
            updateUserdata();
        } else {
            throw new Error('Invalid game state data')
        }
    } catch (error) {
        console.error('Error during hit:', error);
        document.getElementById("result").textContent = "An error occurred while hitting.";
    }
}


// Player stays and the game is resolved
async function stay() {
    try {
        // Send request to stay
        const response = await fetch('/black_jack/stay', {method: "POST"});

        // Check if response is ok
        if (!response.ok) {
            throw new Error(`Network response was not ok`);
        }

        // Parse the response
        const gameState = await response.json();

        // Validate and update game state
        if (isGameState(gameState)) {
            updateGameState(gameState);
            updateUserdata();
        } else {
            throw new Error('Invalid game state data')
        }
    } catch (error) {
        console.error('Error during stay:', error);
        document.getElementById("result").textContent = "An error occurred while staying.";
    }
}

// Restart the game
async function restart() {
    try {
        // Send request to restart
        const response = await fetch('/black_jack/restart', {method: "POST"});

        // Check if response is ok
        if (!response.ok) {
            throw new Error(`Network response was not ok`);
        }

        // Parse the response
        const gameState = await response.json();

        // Validate and update game state
        if (isGameState(gameState)) {
            updateGameState(gameState);
        } else {
            throw new Error('Invalid game state data')
        }
    } catch (error) {
        console.error('Error during restart:', error);
        document.getElementById("result").textContent = "An error occurred while restarting.";
    }
}



// Helper Functions


// Update the game state on the UI
function updateGameState(gameState) {
    // Update dealer and player sums
    document.getElementById("sumDealer").textContent = gameState.dealerSum;
    document.getElementById("sumPlayer").textContent = gameState.playerSum;

    // Update dealer's cards
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

    // Update player's cards
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

    // Update result message
    if (gameState.state === 'initial') {
        document.getElementById("result").textContent = "Welcome to Black Jack! The goal is to get as close to 21 without going over. Good luck!";
    }
    else {
        document.getElementById("result").textContent = gameState.message;
    }

    // Update button states
    updateButtonStates(gameState);
}


// Update the states of the buttons based on the game state
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
    const betAmountElement = document.getElementById("betAmount");

    // Disable all buttons initially
    for (const key in buttons) {
        buttons[key].disabled = true;
        buttons[key].style.backgroundColor = '#D3D3D3';
        buttons[key].style.cursor = "default";
    }

    // Enable buttons based on game state
    if (gameState.state === 'initial') {
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

        betAmountElement.disabled = false;
    } else if (gameState.state === 'playing') {
        buttons.hit.disabled = false;
        buttons.hit.style.backgroundColor = '#8FB8DE';
        buttons.hit.style.cursor = 'pointer';

        buttons.stay.disabled = false;
        buttons.stay.style.backgroundColor = '#8FB8DE';
        buttons.stay.style.cursor = 'pointer';

        betAmountElement.disabled = true;
    } else if (gameState.state === 'gameOver') {
        buttons.restart.disabled = false;
        buttons.restart.style.backgroundColor = '#8FB8DE';
        buttons.restart.style.cursor = 'pointer';

        betAmountElement.disabled = true;
    }
}


// Set the initial state of the game
function setInitialState() {
    // Set initial state for dealer and player
    document.getElementById("sumDealer").textContent = "?";
    document.getElementById("sumPlayer").textContent = "0";

    // Clear any previous result
    document.getElementById("result").textContent = "";

    // Display Black Jack explanation
    document.getElementById("result").textContent = "Welcome to Black Jack! The goal is to get as close to 21 without going over. Good luck!";

    // Disable buttons on page load
    const buttons = {
        hit: document.getElementById("hit"),
        stay: document.getElementById("stay"),
        restart: document.getElementById("restart"),
        start: document.getElementById("start"),
        decrementBetBy10: document.getElementById("decrementBetBy10"),
        decrementBetBy1: document.getElementById("decrementBetBy1"),
        incrementBetBy1: document.getElementById("incrementBetBy1"),
        incrementBetBy10: document.getElementById("incrementBetBy10")
    };

    for (const key in buttons) {
        buttons[key].disabled = true;
        buttons[key].style.backgroundColor = '#D3D3D3';
        buttons[key].style.cursor = "default";
    }

    // Enable only the start button and bet buttons
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
}

