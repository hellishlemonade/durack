from random import randint


PLAYERS_COUNT = int(input())


class Table:

    def __init__(self, under_button_player):
        self.card_list = []
        self.under_button_player = under_button_player


class Player:

    def __init__(self, num=0):
        self.num = num
        self.hand = []
        self.name = 'Gamer'

    def take(self, contr_cards):
        for card in contr_cards:
            self.hand.append(card)

    def move(self, cards):
        if len(self.hand) == 0:
            return False
        if len(cards) == 0:
            return self.hand.pop(randint(0, len(self.hand) - 1))
        for card in cards:
            for i, self_card in enumerate(self.hand):
                if card.card_num == self_card.card_num:
                    return self.hand.pop(i)
        return False

    def contr_move(self, contr_card):
        for i, card in enumerate(self.hand):
            if (card.card_num > contr_card.card_num
               and card.card_suit == contr_card.card_suit):
                return self.hand.pop(i)
        return False

    def __str__(self):
        return self.name


class ComputerPlayer(Player):

    def __init__(self, num):
        self.num = num
        self.hand = []
        self.name = f'Computer Player {self.num}'


class Card:

    def __init__(self, card_num, card_suit):
        self.card_num = card_num
        self.card_suit = card_suit
        self.card_name = self.make_name()
        self.is_trump = False

    def make_name(self):
        string = ''
        if self.card_num < 11:
            string = f'{self.card_num}'
        elif self.card_num == 11:
            string = 'Валет'
        elif self.card_num == 12:
            string = 'Дама'
        elif self.card_num == 13:
            string = 'Король'
        else:
            string = 'Туз'
        if self.card_suit == 1:
            string += ' Черви'
        elif self.card_suit == 2:
            string += ' Буби'
        elif self.card_suit == 3:
            string += ' Пики'
        else:
            string += ' Крести'
        return string

    def __str__(self):
        return f'{self.card_name}'


class CardDeck:

    def __init__(self):
        self.card_deck = 52
        self.card_list = []

    def create_deck(self):
        for card_number in range(2, 15):
            for card_suit in range(1, 5):
                self.card_list.append(Card(card_number, card_suit))

    def card_shuffle(self, players_list):
        if self.card_deck == 0:
            return False
        for player in players_list:
            hand = len(player.hand)
            if hand < 6:
                for _ in range(6 - hand):
                    rand_card = self.card_list.pop(randint(0, self.card_deck - 1))
                    player.hand.append(rand_card)
                    self.card_deck -= 1
                    if self.card_deck == 0:
                        return False

    def make_trump(self):
        trump_card = self.card_list[randint(0, self.card_deck - 1)]
        for card in self.card_list:
            if card.card_suit == trump_card.card_suit:
                card.is_trump = True
        return trump_card


def create_players(players_count, players_list):
    players_list.append(Player())
    for num in range(1, players_count):
        players_list.append(ComputerPlayer(num))


players: list = []
create_players(PLAYERS_COUNT, players)
card_deck = CardDeck()
card_deck.create_deck()
card_deck.make_trump()
card_deck.card_shuffle(players)
move = randint(0, PLAYERS_COUNT - 1)
next_move = move + 1
while len(players[0].hand) > 0 and len(players[1].hand) > 0:
    if move == PLAYERS_COUNT - 1:
        next_move = 0
    elif move == PLAYERS_COUNT:
        move = 0
        next_move = 1
    elif move == PLAYERS_COUNT + 1:
        move = 1
        next_move = 2
        if move == PLAYERS_COUNT - 1:
            next_move = 0
    button_player = players[move]
    under_button_player = players[next_move]
    table = Table(under_button_player)

    # Для отладки
    string_button_hand = ''
    for card in button_player.hand:
        string_button_hand += f'{card}. '
    print(f'{button_player}: {string_button_hand}')
    string_under_button_hand = ''
    for card in under_button_player.hand:
        string_under_button_hand += f'{card}. '
    print(f'{under_button_player}: {string_under_button_hand}')

    for _ in range(len(under_button_player.hand)):
        card = button_player.move(table.card_list)
        print(f'\nХод {button_player} - {card}\n')
        if not card:
            print('Бито')
            print(f'Минус {len(table.card_list)} карт(а) в колоде.\n')
            table.card_list.clear()
            break
        table.card_list.append(card)
        contr_card = under_button_player.contr_move(card)
        print(f'Ход {under_button_player} - {contr_card}\n')
        if not contr_card:
            under_button_player.take(table.card_list)
            print(f'Игрок {under_button_player} взял: {len(table.card_list)} карт(у).')
            print(f'Минус {len(table.card_list)} карт(а) в колоде.\n')
            table.card_list.clear()
            move -= 1
            break
        table.card_list.append(contr_card)
        for player in players:
            if player == button_player or player == under_button_player:
                break
            another_card = player.move(table.card_list)
            if not another_card:
                break
            table.card_list.append(another_card)

        # Для отладки
        string_button_hand = ''
        for card in button_player.hand:
            string_button_hand += f'{card}. '
        print(f'{button_player}: {string_button_hand}')
        string_under_button_hand = ''
        for card in under_button_player.hand:
            string_under_button_hand += f'{card}. '
        print(f'{under_button_player}: {string_under_button_hand}')
    card_deck.card_shuffle(players)
    print(f'карт в колоде {len(card_deck.card_list)}')
    move += 1
