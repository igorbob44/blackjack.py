# Демонстрирует решение задачи из книги Майкла Доусона "Программируем на python" (издание 3)
# Задача из главы 9. Объектно-ориентированное программирование. Игра "Блек-джек"
# Страница 276, задача 2

# Условие:
# Написать однокарточную версию "Война", стуктура раунда в которой такова:
# все игроки тянут по одной карте, а выигрывает тот,
# у кого номинал карты оказывается наибольшим
import cards
import games


class War_card(cards.Card):
    """Карта для игры 'Война'"""

    ACE_VALUE = 1  # Константа, определяющая стоимость туза

    @property  # Свойство, определяющее стоимость карт в списке RANKS
    def value(self):  # класса Card модуля cards
        if self.is_face_up:  # Если карта повёрнута лицевой стороной
            v = War_card.RANKS.index(self.rank) + 1  # присвоить v список значений карт по возрастанию от 1>
        else:  # В противном случае вернуть ПУСТОЕ значение None
            v = None
        return v


class War_deck(cards.Deck):
    """Колода для игры в 'Война'"""

    def populate(self):
        for suit in War_card.SUITS:
            for rank in War_card.RANKS:
                self.cards.append(War_card(rank, suit))


class War_hand(cards.Hand):
    """Рука игрока в игру 'Война'"""

    def __init__(self, name):
        super(War_hand, self).__init__()
        self.name = name

    def __str__(self):
        rep = self.name + ":\t" + super(War_hand, self).__str__()
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
            if card.value == War_card.ACE_VALUE:
                contains_ace = True
        # если на руках есть туз и сумма очков не превышает 11, будем считать туз за 11 очков
        if contains_ace and t <= 15:
            # прибавить нужно лишь 10, потому что единица уже вошла в общую сумму
            t += 14
        return t


class War_player(War_hand):
    """ Игрок в игре "Война". """

    def lose(self):
        print("=" * 70)
        print(self.name, "проиграл.")
        print("=" * 70)

    def win(self):
        print("=" * 70)
        print("." * 70)
        print(self.name, "|"*20+"ВЫИГРАЛ!"+"|"*20)
        print("." * 70)
        print("=" * 70)


class War_dealer(War_hand):
    """ Дилер в игре "Блек-джек". """

    def flip_first_card(self):
        if self.cards:
            first_card = self.cards[0]
            first_card.flip()
        else:
            print("<нет карт>")


class War_game(object):
    """ Игра в Блек-джек. """

    def __init__(self, names):
        self.players = []
        # self.dealer = War_dealer("Dealer")
        for name in names:
            player = War_player(name)
            self.players.append(player)
        self.deck = War_deck()
        self.deck.populate()
        self.deck.shuffle()

    def __additional_cards(self, player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print("-" * 50)
            print(player)
            print("-" * 50)

    def play(self):
        # проверка колоды
        CARDS_IN_HAND = 1
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
        # сдача всем по 1 карте
        self.deck.deal(self.players, CARDS_IN_HAND)
        for player in self.players:  # список игроков и набранных ими значений демонстрируется на экране
            print("-" * 50)
            print(player)
            print("-" * 50)
        # сравниваем суммы очков у дилера и у игроков, оставшихся в игре
        vin = 0
        ravno = 0
        not_bad = 0
        for player in self.players:
            for caunt in self.players:
                if player.total < caunt.total:
                    vin += 1
                elif player.total == caunt.total:
                    ravno += 1
                else:
                    not_bad += 1
            if vin == 0 and ravno == 0:
                player.win()
                vin = 0
                ravno = 0
            elif vin == 0 and ravno >= 0:
                player.win()
                vin = 0
                ravno = 0
            elif vin > 0 and ravno >= 0:
                player.lose()
                vin = 0
                ravno = 0
            elif vin > 0 and ravno == 0:
                player.lose()
                vin = 0
                ravno = 0
            else:
                vin = 0
                ravno = 0
                print("не определено")
        # удаление всех карт
        for player in self.players:
            player.clear()
        # self.dealer.clear()


def main():
    print("\t\tДобро пожаловать за игровой стол игры \"Война\"!\n")
    LOW_PL = 1
    HIGH_PL = 8
    names = []
    number = games.ask_number("Сколько всего игроков? (1-7): ", LOW_PL, HIGH_PL)
    for i in range(number):
        name = input("Введите имя игрока: ")
        names.append(name)
    game = War_game(names)
    again = None
    while again != "n":
        game.play()
        # if not game.players:  # прекращение игры, если за столом не осталось игроков
        #     print("=" * 70)
        #     print("=" * 70)
        #     print("\tК сожалению, за столом не осталось игроков.")
        #     print("\tДилер вынужден прекратить игру. До скорой встречи.")
        #     print("=" * 70)
        #     print("=" * 70)
        #     break
        again = games.ask_yes_no("\nХотите сыграть ещё раз? ")


main()

input("\n\nНажмите Enter, чтобы выйти.")
