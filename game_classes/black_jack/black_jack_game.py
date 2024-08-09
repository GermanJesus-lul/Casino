from flask import request, session
from game_classes.black_jack.card_deck import CardDeck
from game_classes.black_jack.dealer import Dealer
from game_classes.black_jack.player import Player
from game_classes.black_jack.card import Card
from helper_functions.user_administration import userid_from_token, update_balance
from helper_functions.stats import played_game
from helper_functions.game_utils import get_bet_amount


class BlackJackGame:
    def __init__(self):
        self.deck = CardDeck()
        self.dealer = Dealer()
        self.player = Player()
        self.state = 'initial'

    def start_game(self):
        self.state = 'playing'
        self.dealer.hidden_card = self.deck.draw_card()
        self.dealer.sum += self.dealer.get_value(self.dealer.hidden_card)
        self.dealer.ace_count += self.dealer.check_ace(self.dealer.hidden_card)
        while self.dealer.sum < 17:
            card = self.deck.draw_card()
            self.dealer.add_card(card)
        for i in range(2):
            card = self.deck.draw_card()
            self.player.add_card(card)
        return self.get_game_state()

    def hit(self):
        if self.state != 'playing':
            return self.get_game_state()
        card = self.deck.draw_card()
        self.player.add_card(card)
        if self.player.sum > 21:
            self.state = 'gameOver'
            self.record_game_outcome("Player busts!", -get_bet_amount())
        return self.get_game_state()

    def stay(self):
        if self.state != 'playing':
            return self.get_game_state()
        self.state = 'gameOver'
        self.resolve_game()
        return self.get_game_state()

    def restart(self):
        self.__init__()
        return self.get_game_state()

    def resolve_game(self):
        user_id = userid_from_token(request.cookies.get('token'))
        bet_amount = get_bet_amount()
        if self.player.sum > 21:
            self.record_game_outcome("Player busts!", -bet_amount)
        elif self.dealer.sum > 21:
            self.record_game_outcome("Dealer busts!", bet_amount)
        elif self.player.sum > self.dealer.sum:
            self.record_game_outcome("Player wins!", bet_amount)
        elif self.player.sum < self.dealer.sum:
            self.record_game_outcome("Dealer wins!", -bet_amount)
        else:
            self.record_game_outcome("Tie!", 0)

    def record_game_outcome(self, message, amount):
        user_id = userid_from_token(request.cookies.get('token'))
        update_balance(user_id, amount)
        played_game(user_id, amount, "blackjack", text_field=message)

    def get_game_state(self):
        game_state = {
            "state": self.state,
            "playerSum": self.player.sum,
            "cardsDealer": [card.get_image_filename() for card in self.dealer.cards],
            "cardsPlayer": [card.get_image_filename() for card in self.player.cards],
            "message": self.get_message()
        }
        if self.state == 'gameOver':
            game_state['dealerSum'] = self.dealer.sum
            game_state['hiddenCard'] = self.dealer.hidden_card.get_image_filename()
        else:
            game_state['dealerSum'] = '?'
            game_state['hiddenCard'] = 'back'
        return game_state

    def get_message(self):
        if self.state == 'gameOver':
            if self.player.sum > 21:
                return "Player busts!"
            elif self.dealer.sum > 21:
                return "Dealer busts!"
            elif self.player.sum > self.dealer.sum:
                return "Player wins!"
            elif self.player.sum < self.dealer.sum:
                return "Dealer wins!"
            else:
                return "Tie!"
        return ""

    def to_dict(self):
        return {
            'deck': self.deck.to_dict(),
            'dealer': {
                'sum': self.dealer.sum,
                'ace_count': self.dealer.ace_count,
                'cards': [card.to_dict() for card in self.dealer.cards],
                'hidden_card': self.dealer.hidden_card.to_dict() if self.dealer.hidden_card else None
            },
            'player': {
                'sum': self.player.sum,
                'ace_count': self.player.ace_count,
                'cards': [card.to_dict() for card in self.player.cards]
            },
            'state': self.state
        }

    @classmethod
    def from_dict(cls, data):
        game = cls()
        game.deck = CardDeck.from_dict(data['deck'])
        game.dealer.sum = data['dealer']['sum']
        game.dealer.ace_count = data['dealer']['ace_count']
        game.dealer.cards = [Card.from_dict(card) for card in data['dealer']['cards']]
        game.dealer.hidden_card = Card.from_dict(data['dealer']['hidden_card']) if data['dealer'][
            'hidden_card'] else None
        game.player.sum = data['player']['sum']
        game.player.ace_count = data['player']['ace_count']
        game.player.cards = [Card.from_dict(card) for card in data['player']['cards']]
        game.state = data['state']
        return game
