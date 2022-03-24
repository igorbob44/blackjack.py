# Блек-джек
# От 1 до 7 игроков против дилера
import cards
import games


class BlackJackCard(cards.Card):  # класс BJ_Card создан на базе класса Card() модуля cards
    """ Карта для игры в Блек-джек. """
    ACE_VALUE = 1  # Константа, определяющая стоимость туза

    @property  # Свойство, определяющее стоимость карт в списке RANKS
    def value(self):  # класса Card модуля cards
        if self.is_face_up:  # Если карта повёрнута лицевой стороной
            v = BlackJackCard.RANKS.index(self.rank) + 1  # присвоить v список значений карт по возрастанию от 1>
            if v > 10:  # Если переменная больше 10 - вернуть 10
                v = 10
        else:  # В противном случае вернуть ПУСТОЕ значение None
            v = None
        return v


class BlackJackDeck(cards.Deck):
    """ Колода для игры в "Блек-джек". """

    def populate(self):
        for suit in BlackJackCard.SUITS:
            for rank in BlackJackCard.RANKS:
                self.cards.append(BlackJackCard(rank, suit))


class BlackJackHand(cards.Hand):
    """ 'Рука': набор карт "Блек-джрека" у одного игрока. """

    def __init__(self, name):
        super(BlackJackHand, self).__init__()
        self.name = name

    def __str__(self):
        rep = self.name + ":\t" + super(BlackJackHand, self).__str__()
        if self.total:
            rep += "(" + str(self.total) + ")"
        return rep

    @property
    def total(self):
        # если у одной из карт value равно None, то и все свойство равно None
        for card in self.cards:
            if not card.value:
                return None
        # сумируем очки, считая каждый туз за 1 очко
        t = 0
        for card in self.cards:
            t += card.value
        # определяем, есть ли туз на руках у игрока
        contains_ace = False
        for card in self.cards:
            if card.value == BlackJackCard.ACE_VALUE:
                contains_ace = True
        # если на руках есть туз и сумма очков не превышает 11, будем считать туз за 11 очков
        if contains_ace and t <= 11:
            # прибавить нужно лишь 10, потому что единица уже вошла в общую сумму
            t += 10
        return t

    def is_busted(self):
        return self.total > 21


class BlackJackPlayer(BlackJackHand):
    """ Игрок в "Блек-джек". """

    def __init__(self, name, cash=0, player_bet=0, is_bet=False):
        super(BlackJackPlayer, self).__init__(name)
        self.name = name
        self.cash = cash
        self.is_bet = is_bet
        self.player_bet = player_bet

    def __str__(self):
        rep = "\t"+super(BlackJackPlayer, self).__str__()
        rep += "\n"+"\t"+"Всего наличных: "+str(self.cash)
        return rep

    def player_bet_the(self):
        return self.player_bet

    def player_cash(self):
        rep = f"Всего у {self.name} сейчас: " + str(self.cash)
        return rep

    def is_hitting(self):
        self.bet()
        response = games.ask_yes_no(
            "\n" + "*" * 50 + "\n" + self.name + "\t(" + str(self.total) + "), будете брать ещё карты? (Y/N): ")
        return response == "y"

    def bet(self):
        if not self.is_bet:
            while True:
                try:
                    bet_size = int(input(
                        "\n" + "*" * 50 + "\n" + self.name + "\t(" + str(self.total) + ").  Какова ваша ставка? "))
                    self.is_bet = True
                    self.player_bet += bet_size
                    self.cash -= self.player_bet
                    return bet_size
                except:
                    print("Введите, пожалуйста, число, а не текст.")
        else:
            print("Ставка сделана: " + str(self.player_bet))

    def bet_off(self):
        self.is_bet = False
        self.player_bet = 0

    @property
    def player_bet_size(self):
        self.cash -= self.player_bet
        return self.cash

    def no_cash(self):
        if self.cash == 0:
            print(f"Наличные игрока {self.name} закончились: {self.name} выбыл из-за стола.")
            return self.cash == 0

    def bust(self):
        print(self.name, "перебрал.")
        self.lose()

    def lose(self):
        print("="*70)
        print(self.name, "проиграл.")
        print("="*70)

    def win(self):
        print("="*70)
        print(self.name, "выйграл.")
        self.cash += self.player_bet * 2
        print("="*70)

    def push(self):
        print("="*70)
        print(self.name, "сыграл с компьютером вничью.")
        self.cash += self.player_bet
        print("="*70)


class BlackJackDealer(BlackJackHand):
    """ Дилер в игре "Блек-джек". """

    def __init__(self, name, cash, dealer_bet=0, player=None):
        super(BlackJackDealer, self).__init__(name)
        self.name = name
        self.cash = cash
        self.dealer_bet = dealer_bet
        self.player = player

    def __str__(self):
        rep = super(BlackJackDealer, self).__str__()
        rep += "\n" + "Всего наличных: " + str(self.cash)
        return rep

    @property
    def dealer_cash(self):
        return self.cash

    def new_name_player(self, new_name_player):
        self.player = new_name_player
        return self.player

    def rate_processing(self):
        self.cash += self.player.player_bet_the()
        print("Наличные дилера увеличены до: ", self.cash)

    def is_hitting(self):
        return self.total < 17

    def bust(self):
        print("-"*70)
        print(self.name, "перебрал.")
        print("-"*70)

    def bust_1(self):
        print("-"*70)
        print(self.name, "вернул ставку.")
        self.cash -= self.player.player_bet_the()
        print("Наличные дилера уменьшены до: "+str(self.cash))
        print("-"*70)

    def bust_2(self):
        print("-"*70)
        print(self.name, "проиграл игроку.")
        self.cash -= self.player.player_bet_the()*2
        print("Наличные дилера уменьшены до: "+str(self.cash))
        print("-"*70)

    def flip_first_card(self):
        if self.cards:
            first_card = self.cards[0]
            first_card.flip()
        else:
            print("<нет карт>")


class BlackJackGame(object):
    """ Игра в Блек-джек. """

    def __init__(self, names):
        self.add_cash = 1000
        self.remaining_players = []
        self.players = []
        for name in names:
            cash_pl = games.ask_number(f"{name}, cколько денег в вашем распоряжении? (от 1 до 300): ", low=20, high=301)
            player = BlackJackPlayer(name, cash=cash_pl)
            self.players.append(player)
        self.dealer = BlackJackDealer("Dealer", self.add_cash)
        self.deck = BlackJackDeck()
        self.deck.populate()
        self.deck.shuffle()

    @property
    def dropped_out(self):
        remaining_pl = []
        for player in self.players:
            if player.no_cash():
                remaining_pl.append(player)
                self.players.remove(player)
        return remaining_pl

    @property
    def still_playing(self):
        sp = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp

    def __additional_cards(self, player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print("-" * 50)
            print(player)
            print("-" * 50)
            if player.is_busted():
                player.bust()

    def play(self):
        # проверка колоды
        CARDS_IN_HAND = 2
        if len(self.deck.cards) <= 30:
            print("*" * 50)
            print("В колоде осталось " + str(len(self.deck.cards)) + " карт.")
            print("Идёт перетасовка колоды...")
            self.deck.clear()
            self.deck.populate()
            self.deck.shuffle()
            print("Колода перетасована. ")
            print("В колоде теперь " + str(len(self.deck.cards)) + " карт.")
            print("*" * 50)
        # сдача всем по 2 карты
        self.deck.deal(self.players + [self.dealer], CARDS_IN_HAND)  # каждому игроку и дилеру здаются по 2 карты
        self.dealer.flip_first_card()  # первая из карт, сданных дилеру, переворачивается рубашкой вверх
        for player in self.players:  # список игроков и набранных ими значений демонстрируется на экране
            print("-" * 50)
            print(player)
            print("-" * 50)
        print("Тут демонстрируется значение дилера и его банк: ")
        print(self.dealer)  # демонстрирует 1 карту дилера перевёрнутой, а вторую  - нет
        # сдача дополнительных карт игрокам
        for player in self.players:
            self.__additional_cards(player)
            self.dealer.new_name_player(player)
            self.dealer.rate_processing()
        self.dealer.flip_first_card()  # первая карта дилера расркывается
        if not self.still_playing:
            # все игроки перебрали, покажем только "руку" дилера
            print(self.dealer)
            print("Все перебрали. У дилера осталось: " + str(self.dealer.dealer_cash))
        else:
            # сдача дополнительных карт дилеру
            print(self.dealer)
            self.__additional_cards(self.dealer)
            if self.dealer.is_busted():
                # выигрывают все, кто ещё остался в игре
                for player in self.still_playing:
                    self.dealer.new_name_player(player)
                    self.dealer.bust_2()
                    player.win()
                    print(player.player_cash())
                    print("Всего у дилера сейчас: " + str(self.dealer.dealer_cash))
            else:
                # сравниваем суммы очков у дилера и у игроков, оставшихся в игре
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        self.dealer.new_name_player(player)
                        self.dealer.bust_2()
                        player.win()
                        print(player.player_cash())
                        print("Всего у дилера сейчас: " + str(self.dealer.dealer_cash))
                    elif player.total < self.dealer.total:
                        player.lose()
                        print(player.player_cash())
                        print("Деньги остались у дилера: " + str(self.dealer.dealer_cash))
                    else:
                        player.push()
                        print(player.player_cash())
                        self.dealer.new_name_player(player)
                        self.dealer.bust_1()
                        print("У дилера стало: " + str(self.dealer.dealer_cash))
        # вывод списка игроков с дилером и их обновленных значение
        print("="*70)
        print("="*70)
        print("\nВсего у игроков денег на руках сейчас: ")
        for player in self.players:
            print("\n"+str(player.player_cash()), "\n")
        print("="*70)
        print("\nУ дилера сейчас: \n")
        print(self.dealer.dealer_cash)
        print("="*70)
        # удаление всех карт
        for player in self.players:
            player.clear()
            player.bet_off()
        self.dealer.clear()
        # проверка наличностей у игроков: если наличные есть, игроки остаются в игре
        for player in self.dropped_out:
            if player.cash == 0:
                print("До свидания,"+str(player.name)+", в другой раз повезет!")


def main():
    print("\t\tДобро пожаловать за игровой стол Блек-джека!\n")
    LOW_PL = 1
    HIGH_PL = 8
    names = []
    number = games.ask_number("Сколько всего игроков? (1-7): ", LOW_PL, HIGH_PL)
    for i in range(number):
        name = input("Введите имя игрока: ")
        names.append(name)
    game = BlackJackGame(names)
    again = None
    while again != "n":
        game.play()
        # прекращение игры, если за столом не осталось игроков
        if not game.players:
            print("="*70)
            print("="*70)
            print("\tК сожалению, за столом не осталось игроков.")
            print("\tДилер вынужден прекратить игру. До скорой встречи.")
            print("="*70)
            print("="*70)
            break
        again = games.ask_yes_no("\nХотите сыграть ещё раз? ")


main()

input("\n\nНажмите Enter, чтобы выйти.")
