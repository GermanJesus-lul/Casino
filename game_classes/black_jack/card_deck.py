import random
from game_classes.black_jack.card import Card


class CardDeck:
    def __init__(self):
        self.deck = []
        self.build_deck()
        self.shuffle_deck()

    def build_deck(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        self.deck = [Card(suit, value) for suit in suits for value in values]

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def draw_card(self):
        return self.deck.pop()

    def to_dict(self):
        return {
            "deck": [card.to_dict() for card in self.deck]
        }

    @classmethod
    def from_dict(cls, data):
        deck = cls()
        deck.deck = [Card.from_dict(card) for card in data['deck']]
        return deck
