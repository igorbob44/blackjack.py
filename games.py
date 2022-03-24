# Игры
# Демонстрирует создание модуля
class Player(object):
    """ Участник игры. """
    def __init__(self, name, score=0):
        self.name = name
        self.score = score

    def __str__(self):                              # Метод выводит значение класса в виде строки:
        rep = self.name + ":\t" + str(self.score)   # Имя игрока + количество набранных очков на руках
        return rep                                  # возвращение строки


def ask_yes_no(question):                           # функция возвращает ответ "y" или "n" (да или нет)
    """ Задает вопрос с ответом 'да' или 'нет'. """
    response = None
    while response not in ("y", "n"):
        response = input(question).lower()
    return response


def ask_number(question, low, high):
    """ Просит ввести число из заданного диапазона. """
    while True:
        try:
            response = None
            while response not in range(low, high):
                response = int(input(question))
            return response
        except:
            print("Введите цифровое значение, а не строковое из диапазона от 1 до 7.")

if __name__ == "__main__":
    print("Вы запустили этот модуль напрямую, а не импортировали его.")
    input("\n\nНажмите Enter, чтобы выйти.")

