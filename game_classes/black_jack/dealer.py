from game_classes.black_jack.player import Player


class Dealer(Player):
    def __init__(self):
        super().__init__()
        # Initialize dealer with a hidden card
        self.hidden_card = None
