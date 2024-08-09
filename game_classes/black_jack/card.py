class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} of {self.suit}"

    def to_dict(self):
        return {
            "suit": self.suit,
            "value": self.value
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['suit'], data['value'])

    def get_image_filename(self):
        return f"{self.suit}_{self.value}"
