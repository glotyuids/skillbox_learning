# -*- coding: utf-8 -*-
import random

_target_number = ''


def generate_number():
    global _target_number
    _target_number = ''.join(random.sample(set('0123456789'), 4))


def check_number(user_number):
    global _target_number
    bulls, cows = 0, 0
    for user_char, target_char in zip(user_number, _target_number):
        if user_char == target_char:
            bulls += 1
        if user_char in _target_number:
            cows += 1
    cows = cows - bulls
    return {'bulls': bulls, 'cows': cows}