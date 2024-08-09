class Card:
    def __init__(self, suit, value):
        # Initialize card with suit and value
        self.suit = suit
        self.value = value

    def __str__(self):
        # Return a string representation of the card
        return f"{self.value} of {self.suit}"

    def to_dict(self):
        # Convert the card to a dictionary
        return {
            "suit": self.suit,
            "value": self.value
        }

    @classmethod
    def from_dict(cls, data):
        # Create a Card instance from a dictionary
        return cls(data['suit'], data['value'])

    def get_image_filename(self):
        # Get the image filename for the card
        return f"{self.suit}_{self.value}"
