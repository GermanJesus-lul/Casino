import random
from game_classes.black_jack.card import Card


class CardDeck:
    def __init__(self):
        # Initialize the deck and build and shuffle it
        self.deck = []
        self.build_deck()
        self.shuffle_deck()

    def build_deck(self):
        # Build a standard deck of 52 cards
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        self.deck = [Card(suit, value) for suit in suits for value in values]

    def shuffle_deck(self):
        # Shuffle the deck
        random.shuffle(self.deck)

    def draw_card(self):
        # Draw a card from the deck
        return self.deck.pop()

    def to_dict(self):
        # Convert the deck to a dictionary
        return {
            "deck": [card.to_dict() for card in self.deck]
        }

    @classmethod
    def from_dict(cls, data):
        # Create a CardDeck instance from a dictionary
        deck = cls()
        deck.deck = [Card.from_dict(card) for card in data['deck']]
        return deck
