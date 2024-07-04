/*document.getElementById("hit").addEventListener("click", hitFunction);
document.getElementById("stay").addEventListener("click", stayFunction);*/

var dealerSum = 0;
var yourSum = 0;

var dealerAceCount = 0;
var yourAceCount = 0;

var hidden;
var deck;

var canHit = true;

window.onload = function() {
    fetch("/blackjack/deal", {method: "POST"})
        .then(response => response.json())
        .then(data => {
            document.getElementById("sumDealer").innerText = data.dealer_sum;
            document.getElementById("sumPlayer").innerText = data.player_sum;

            hidden = data.hidden_card;
            dealerSum = data.dealer_sum;
            yourSum = data.player_sum;

            dealerAceCount = data.dealer_ace_count;
            yourAceCount = data.player_ace_count;

            data.player_cards.forEach(card => {
                let cardImg = document.createElement("img");
                cardImg.src = `/static/images/card_deck_black_jack/${card}.svg`;
                document.getElementById("playerCards").append(cardImg);

            });

            let dealerCardImg = document.createElement("img");
            dealerCardImg.src = `/static/images/card_deck_black_jack/${data.dealer_cards[0]}.svg`;
            document.getElementById("cardsDealer").append(dealerCardImg);
        });

    document.getElementById("hit").addEventListener("click", hit);
    document.getElementById("stay").addEventListener("click", stay);
};

function hit() {
    if (!canHit) {
        return;
    }
    fetch('/black_jack/hit', {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            let cardImg = document.createElement('img');
            cardImg.src = `/static/images/cards/${data.card}.svg`;
            document.getElementById('cardsPlayer').append(cardImg);

            yourSum += data.value;
            yourAceCount += data.ace;
            yourSum = reduceAce(yourSum, yourAceCount);

            document.getElementById('sumPlayer').innerText = yourSum;

            if (yourSum > 21) {
                canHit = false;
                document.getElementById('results').innerText = "You lose!";
            }
        });

}

function stay() {
        canHit = false;
    fetch('/black_jack/stay', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            dealer_sum: dealerSum,
            dealer_ace_count: dealerAceCount,
            dealer_cards: [document.getElementById('cardsDealer').firstChild.src.split('/').pop().split('.')[0]]
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('hiddenCard').src = `/static/images/cards/${hidden}.svg`;

        data.dealer_cards.forEach((card, index) => {
            if (index > 0) {
                let cardImg = document.createElement('img');
                cardImg.src = `/static/images/cards/${card}.svg`;
                document.getElementById('cardsDealer').append(cardImg);
            }
        });

        dealerSum = data.dealer_sum;
        document.getElementById('sumDealer').innerText = dealerSum;

        let message = "";
        if (yourSum > 21) {
            message = "You lose!";
        } else if (dealerSum > 21) {
            message = "You win!";
        } else if (yourSum > dealerSum) {
            message = "You win!";
        } else if (yourSum < dealerSum) {
            message = "You lose!";
        } else {
            message = "It's a tie!";
        }
        document.getElementById('results').innerText = message;
    });
}

function reduceAce(playerSum, playerAceCount) {
    while (playerSum > 21 && playerAceCount > 0) {
        playerSum -= 10;
        playerAceCount--;
    }
    return playerSum;
}
/*
async function hitFunction() {}
async function stayFunction() {}*/
