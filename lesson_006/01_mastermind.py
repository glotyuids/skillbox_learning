# -*- coding: utf-8 -*-

# Игра «Быки и коровы»
# https://goo.gl/Go2mb9
#
# Правила:
# Компьютер загадывает четырехзначное число, все цифры которого различны
# (первая цифра числа отлична от нуля). Игроку необходимо разгадать задуманное число.
# Игрок вводит четырехзначное число c неповторяющимися цифрами,
# компьютер сообщают о количестве «быков» и «коров» в названном числе
# «бык» — цифра есть в записи задуманного числа и стоит в той же позиции,
#       что и в задуманном числе
# «корова» — цифра есть в записи задуманного числа, но не стоит в той же позиции,
#       что и в задуманном числе
#
# Например, если задумано число 3275 и названо число 1234,
# получаем в названном числе одного «быка» и одну «корову».
# Очевидно, что число отгадано в том случае, если имеем 4 «быка».
#
# Формат ответа компьютера
# > быки - 1, коровы - 1


# Составить отдельный модуль mastermind_engine, реализующий функциональность игры.
# В этом модуле нужно реализовать функции:
#   загадать_число()
#   проверить_число(NN) - возвращает словарь {'bulls': N, 'cows': N}
# Загаданное число хранить в глобальной переменной.
# Обратите внимание, что строки - это список символов.
#
# В текущем модуле (lesson_006/01_mastermind.py) реализовать логику работы с пользователем:
#   модуль движка загадывает число
#   в цикле, пока число не отгадано
#       у пользователя запрашивается вариант числа
#       модуль движка проверяет число и выдает быков/коров
#       результат быков/коров выводится на консоль
#  когда игрок угадал таки число - показать количество ходов и вопрос "Хотите еще партию?"
#
# При написании кода учитывайте, что движок игры никак не должен взаимодействовать с пользователем.
# Все общение с пользователем делать в текущем модуле. Представьте, что движок игры могут использовать
# разные клиенты - веб, чатбот, приложение, етс - они знают как спрашивать и отвечать пользователю.
# Движок игры реализует только саму функциональность игры.
# Это пример применения SOLID принципа (см https://goo.gl/GFMoaI) в архитектуре программ.
# Точнее, в этом случае важен принцип единственной ответственности - https://goo.gl/rYb3hT

import mastermind_engine as mme


def select_word_form(number, zero_form, one_form, two_form):
    if number % 10 == 1 and number % 100 != 11:
        return one_form

    if number % 10 in [2, 3, 4] and number % 100 not in [12, 13, 14]:
        return two_form

    return zero_form

# TODO Создайте функцию "проверка_ввода" для валидации ответа игрока, где проверяйте:
#  1) ответ состоит из цифр
#  2) цифр 4 шт.
#  3) цифры разные
#  4) число не начинается с нуля


while True:
    mme.generate_number()
    attempts = 1
    while True:
        print(f'\nПопытка номер {attempts}')
        user_input = input('Введите ваш вариант числа или "выход", если хотите завершить игру: ')
        if user_input.lower() == 'выход':
            print('Жаль, что уходите. Возвращайтесь ещё!')
            exit()

        check_result = mme.check_number(user_input)
        if check_result['bulls'] < 4:
            print(f'{check_result["bulls"]} {select_word_form(check_result["bulls"], "быков", "бык", "быка")} '
                  f'и {check_result["cows"]} {select_word_form(check_result["cows"], "коров", "корова", "коровы")}')
            attempts += 1
        else:
            break
    print(f'Ура! Вы угадали число за {attempts} {select_word_form(attempts, "попыток", "попытку", "попытки")}.')
    user_want_to_play = input('Хотите сыграть ещё раз? 1 - да, 0 - нет: ')
    if not int(user_want_to_play):
        print('Спасибо за игру!')
        exit()

