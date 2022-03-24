# Модуль cards
# Набор базовых классов для карточной игры
class Card(object):
    """ Одна игральная карта. """
    RANKS = ["Туз", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Валет", "Дама", "Король"]
    SUITS = ["♥", "♠", "♦", "♣"]

    def __init__(self, rank, suit, face_up=True):
        self.rank = rank
        self.suit = suit
        self.is_face_up = face_up

    def __str__(self):                      # демонстрирует значение карты или показывает перевёрнутую карту
        if self.is_face_up:
            rep = self.rank + self.suit
        else:
            rep = "XX"
        return rep

    def flip(self):                         # переводит face_up на False (переключатель - поворачивает карту)
        self.is_face_up = not self.is_face_up


class Hand(object):
    """ 'Рука': набор карт на руках у одного игрока. """

    def __init__(self):
        self.cards = []

    def __str__(self):
        if self.cards:                      # Если в списке self.cards есть карты, то:
            rep = ""                        # создаём переменную (rep) и присваиваем ей пустое значение типа str
            for card in self.cards:         # Цикл переберет все карты в списке и выведет их на экран через пробел,
                rep += str(card) + "\t"     # вернув строку в переменной rep в виде списка карт, которые есть на руке
        else:                               # В противном случае:
            rep = "<пусто>"                 # переменной rep будет присвоена пустая строка "пусто" (пустая рука)
        return rep

    def clear(self):
        self.cards = []

    def add(self, card):                    # Метод, который добавляет карты в список self.cards (т. е. в руку)
        self.cards.append(card)

    def give(self, card, other_hand):       # Метод, который передаёт карту(card) из руки в другую руку(other_hand)
        self.cards.remove(card)
        if self.cards:
            other_hand.add(card)            # other_hand будет являтся экземпляром класса Hand() с теми же методами
        else:
            print("<пусто>")


class Deck(Hand):                           # Новый класс создан на базе класса Hand,
    """ Колода игральных карт. """          # поэтому в нём будет рботать метод self.add() класса Hand()

    def populate(self):                     # Метод, который формирует из констант RANKS и SUITS колоду из 52 карт
        for suit in Card.SUITS:                       # Цикл перебирает масти в списке SUITS, совмещая их с индексами
            for rank in Card.RANKS:                   # цикла, который перебирает карты значений в списке RANKS
                self.add(Card(rank, suit))            # и всё это добавляет в новый список (колоду) self.cards

    def shuffle(self):                      # Метод, позволяющий перемешать карты в колоде
        import random                       # Импорт модуля random
        random.shuffle(self.cards)          # Исопльзование специального метода модуля random - random.shuffle()

    def deal(self, hands, per_hand=1):      # Метод, заменяющий дилера(аргументы: количество игроков+количество раздач)
        for rounds in range(per_hand):               # цикл каждый раунд (rounds) раздаёт количество карт (per_hand)
            for hand in hands:                       # цикл игроку на руки (hand) из списка игроков (hands) выдаёт карту
                if self.cards:                       # Если колода (self.cards) наполнена картами:
                    top_card = self.cards[0]         # первую карту колоды(top_card) по первому индексу(self.cards)
                    self.give(top_card, hand)        # - выдать на руки
                else:                                                   # В противном случае, когда список (колода)
                    print("Не могу больше сдавать: карты кончились!")   # пуст - выдаёт предупреждение


if __name__ == "__main__":
    print("Это модуль, содержащий классы для карточных игр.")
    input("\n\nНажмите Enter, чтобы выйти.")
