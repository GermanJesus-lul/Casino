class Player:
    def __init__(self):
        self.sum = 0
        self.ace_count = 0
        self.cards = []

    def add_card(self, card):
        self.sum += self.get_value(card)
        self.ace_count += self.check_ace(card)
        self.sum, self.ace_count = self.reduce_ace(self.sum, self.ace_count)
        self.cards.append(card)

    def get_value(self, card):
        if card.value == 'ace':
            return 11
        elif card.value in ['jack', 'queen', 'king']:
            return 10
        else:
            return int(card.value)

    def check_ace(self, card):
        return 1 if card.value == 'ace' else 0

    def reduce_ace(self, sum, ace_count):
        while sum > 21 and ace_count > 0:
            sum -= 10
            ace_count -= 1
        return sum, ace_count
