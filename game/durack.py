from random import randint


PLAYERS_COUNT = int(input())


class Table:

    def __init__(self):
        self.cards_list = []


class Player:

    def __init__(self, num=0):
        self.num = num
        self.hand = []

    def can_make_move(self, contr_card=None):
        if contr_card is None:
            return True
        card_number, card_suit = contr_card
        for self_card_number, self_card_suit in self.hand:
            if self_card_number > card_number and self_card_suit == card_suit:
                return True
        return False

    def take(self, contr_card):
        self.hand.append(contr_card)

    def move(self, contr_card=None):
        if contr_card is None:
            card_index = int(input())
            return self.hand.pop(card_index)
        card_number, card_suit = contr_card
        for i, card in enumerate(self.hand):
            self_card_number, self_card_suit = card
            if self_card_number > card_number and self_card_suit == card_suit:
                print(i)
                card_index = int(input())
                self.hand.pop(card_index)
                break
        return False


class ComputerPlayer(Player):

    def __init__(self, num):
        self.num = num
        self.hand = []

    def move(self, contr_card=None):
        if contr_card is None:
            return self.hand.pop(randint(0, len(self.hand)-1))
        card_number, card_suit = contr_card
        for i, card in enumerate(self.hand):
            self_card_number, self_card_suit = card
            if self_card_number > card_number and self_card_suit == card_suit:
                self.hand.pop(i)
                break
        return False


class CardDeck:

    def __init__(self):
        self.card_deck = 52
        self.card_list = []

    def create_deck(self):
        for card_number in range(2, 15):
            for card_suit in range(1, 5):
                self.card_list.append((card_number, card_suit))

    def card_shuffle(self, player):
        for _ in range(6):
            rand_card = self.card_list.pop(randint(0, self.card_deck - 1))
            player.hand.append(rand_card)
            self.card_deck -= 1


card_deck = CardDeck()
players_list = []
players_list.append(Player())
for player_num in range(1, PLAYERS_COUNT):
    players_list.append(ComputerPlayer(player_num))
card_deck.create_deck()
for player in players_list:
    card_deck.card_shuffle(player)
    print(player.hand)
start = randint(0, PLAYERS_COUNT - 1)
while True:
    next = start + 1
    if start >= PLAYERS_COUNT - 1:
        next = 0
    start_player = players_list[start]
    next_player = players_list[next]
    start_card = start_player.move()
    if next_player.move(start_card) is False:
        next_player.take(start_card)
    print(start_player.hand)
    print(next_player.hand)
    if start >= PLAYERS_COUNT - 1:
        start = 0
        continue
    start += 1
