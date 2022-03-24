def ask_number(question, low, high):
    """ Просит ввести число из заданного диапазона. """
    response = None
    while response not in range(low, high):
        try:
            response = int(input(question))
        except:
            print(f"Введите, пожалуйста число из диапазона {low, high}.")
    return response


question = ask_number("Выбери вариант Y/N: ", low = 1, high = 5)
print(question)
