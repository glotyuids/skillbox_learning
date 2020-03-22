# -*- coding: utf-8 -*-
import random

_target_number = ''


def generate_number():
    global _target_number
    _target_number = str(random.randint(1, 9))
    _target_number += ''.join(random.sample(set('0123456789') - set(_target_number), 3))
    # Не обеспечивается правило "первой цифрой не может быть ноль"
    # TODO Поправил


def input_is_valid(number_str):
    return (
        number_str.isnumeric() and
        len(number_str) == 4 and
        len(set(number_str)) == 4 and
        number_str[0] != '0'
    )


def check_number(user_number):
    global _target_number
    bulls, cows = 0, 0
    for user_char, target_char in zip(user_number, _target_number):
        if user_char == target_char:
            bulls += 1
        if user_char in _target_number:
            cows += 1
    cows = cows - bulls
    return {'bulls': bulls, 'cows': cows}  # РЕР8 в конце файла должна быть ровно одна пустая строка
