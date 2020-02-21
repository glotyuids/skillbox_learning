# -*- coding: utf-8 -*-
from pprint import pprint

import simple_draw as sd
import random


# На основе кода из практической части реализовать снегопад:
# - создать списки данных для отрисовки N снежинок
# - нарисовать падение этих N снежинок
# - создать список рандомных длинн лучей снежинок (от 10 до 100) и пусть все снежинки будут разные

N = 20

# Пригодятся функции
# sd.get_point()
# sd.snowflake()
# sd.sleep()
# sd.random_number()
# sd.user_want_exit()


def remap_range(value, in_min, in_max, out_min, out_max):
    """Функция пропорционально переносит значение (value) из текущего диапазона значений (fromLow .. fromHigh)
            в новый диапазон (toLow .. toHigh), заданный параметрами.

    """
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def generate_snowflake():
    sf_length = random.randint(MIN_LENGTH, MAX_LENGTH)
    return {
            'x': random.randint(0, sd.resolution[0]),
            'y': sd.resolution[1] + MAX_LENGTH,
            'length': sf_length,
            'factor_a': round(random.uniform(0.2, 1), 2),
            'factor_b': round(random.uniform(0.1, 1), 2),
            'factor_c': round(random.randint(20, 90), 2),
            'h_speed': random.randint(0, 30),
            'v_speed': round(remap_range(value=sf_length, in_min=MIN_LENGTH, in_max=MAX_LENGTH, out_min=2, out_max=60))
        }


MAX_LENGTH = 100
MIN_LENGTH = 10

# генерим первоначальный список снежинок
blizzard = []
for _ in range(N):
    blizzard.append(generate_snowflake())
# pprint(blizzard)

# sd.resolution = (600, 1200)
# while True:
#     sd.clear_screen()
#
#     for snowflake in blizzard:
#         point = sd.get_point(snowflake['x'], snowflake['y'])
#         sd.snowflake(
#             center=point,
#             length=snowflake['length'],
#             factor_a=snowflake['factor_a'],
#             factor_b=snowflake['factor_b'],
#             factor_c=snowflake['factor_c'],
#         )
#         snowflake['y'] -= snowflake['v_speed']
#         if snowflake['y'] < snowflake['length']:
#             blizzard
#         x = x + 30
#
#
#     sd.sleep(0.1)
#     if sd.user_want_exit():
#         break
#
# sd.pause()

# подсказка! для ускорения отрисовки можно
#  - убрать clear_screen()
#  - в начале рисования всех снежинок вызвать sd.start_drawing()
#  - на старом месте снежинки отрисовать её же, но цветом sd.background_color
#  - сдвинуть снежинку
#  - отрисовать её цветом sd.COLOR_WHITE на новом месте
#  - после отрисовки всех снежинок, перед sleep(), вызвать sd.finish_drawing()


# 4) Усложненное задание (делать по желанию)
# - сделать рандомные отклонения вправо/влево при каждом шаге
# - сделать сугоб внизу экрана - если снежинка долетает до низа, оставлять её там,
#   и добавлять новую снежинку
# Результат решения см https://youtu.be/XBx0JtxHiLg


