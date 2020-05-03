# -*- coding: utf-8 -*-

# День сурка
#
# Напишите функцию one_day() которая возвращает количество кармы от 1 до 7
# и может выкидывать исключения:
# + IamGodError
# + DrunkError
# + CarCrashError
# + GluttonyError
# + DepressionError
# + SuicideError
# Одно из этих исключений выбрасывается с вероятностью 1 к 13 каждый день
#
# Функцию оберните в бесконечный цикл, выход из которого возможен только при накоплении
# кармы до уровня ENLIGHTENMENT_CARMA_LEVEL. Исключения обработать и записать в лог.
# При создании собственных исключений максимально использовать функциональность
# базовых встроенных исключений.
import random

ENLIGHTENMENT_KARMA_LEVEL = 777


def strike(string):
    return '\u0336'.join(string) + '\u0336'


def italic(string):
    return '\x1B[3m' + string + '\x1B[23m'


def bold(string):
    return '\033[1m' + string + '\033[0m'


class PhilError(Exception):     # просто для того, чтобы не перехватывать потом каждое исключение отдельно
    pass


class IamGodError(PhilError):
    def __str__(self):
        return 'Я бог. Не этот, конечно, но какой-то другой точно'


class DrunkError(PhilError):
    def __str__(self):
        return f'{strike("Джим Бим, лёд, вода.")} Сладкий вермут со льдом и соломинкой, пожалуйста'


class CarCrashError(PhilError):
    def __str__(self):
        return f'Фил разбился в атокатастрофе. {strike("Птичку")} Сурка жалко('


class GluttonyError(PhilError):
    def __str__(self):
        return 'Фил объелся сладостями'


class DepressionError(PhilError):
    def __str__(self):
        return 'Фил Фил обратился к психиатру. "Зайдите завтра"'


class SuicideError(PhilError):
    def __str__(self):
        return f'Фил {strike("выпрыгнул")} выпал {italic("(роскомнадзор бдит)")} из окна'


def one_day():
    # список исключений можно было бы вынести в константы в начало модуля,
    # но тогда интерпретатор будет ругаться на то, что классы ещё не объявлены
    errors = [IamGodError, DrunkError, CarCrashError, GluttonyError, DepressionError, SuicideError]
    dice = random.randint(1, 13)
    if dice == 13:
        raise random.choice(errors)
    return random.randint(1, 7)


current_karma = 0
day = 0
print(bold('ДЕНЬ'), bold('ОШИБКА'.center(15)), bold('СООБЩЕНИЕ'.center(55)), sep='  ')
while current_karma < ENLIGHTENMENT_KARMA_LEVEL:
    day += 1
    try:
        current_karma += one_day()
    except PhilError as exc:
        print(f'{day:4d}  {exc.__class__.__name__:<15}  {exc}')

print(f'\nФил исправился за 1 день и {day} повторов :)')

# https://goo.gl/JnsDqu
