from game_classes.black_jack.player import Player


class Dealer(Player):
    def __init__(self):
        super().__init__()
        self.hidden_card = None
