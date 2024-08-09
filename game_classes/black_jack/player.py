class Player:
    def __init__(self):
        # Initialize player with sum of card values, ace count, and list of cards
        self.sum = 0
        self.ace_count = 0
        self.cards = []

    def add_card(self, card):
        # Add a card to the player's hand and update the sum and ace count
        self.sum += self.get_value(card)
        self.ace_count += self.check_ace(card)
        self.sum, self.ace_count = self.reduce_ace(self.sum, self.ace_count)
        self.cards.append(card)

    def get_value(self, card):
        # Get the value of the card
        if card.value == 'ace':
            return 11
        elif card.value in ['jack', 'queen', 'king']:
            return 10
        else:
            return int(card.value)

    def check_ace(self, card):
        # Check if the card is an ace
        return 1 if card.value == 'ace' else 0

    def reduce_ace(self, sum, ace_count):
        # Reduce the value of aces from 11 to 1 if the sum exceeds 21
        while sum > 21 and ace_count > 0:
            sum -= 10
            ace_count -= 1
        return sum, ace_count
