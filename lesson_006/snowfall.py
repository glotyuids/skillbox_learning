# -*- coding: utf-8 -*-
import random
from pprint import pprint

import simple_draw as sd

SNOWFLAKE_MAX_LENGTH = 40
SNOWFLAKE_MIN_LENGTH = 5

_blizzard = []


def remap_range(value, in_min, in_max, out_min, out_max):
    """Функция пропорционально переносит значение (value) из текущего диапазона значений (in_min .. in_max)
            в новый диапазон (out_min .. out_max), заданный параметрами.
            Конкретно здесь используется для создания эффекта параллакса

    """
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def generate_snowflakes(count=1):
    """Функция генерирует и добавляет в _blizzard заданное число новых рандомизованных снежинок.

    Parameters
    ----------
    count : int, default=1
        количество снежинок, которое требуется сгенерировать

    Returns
    -------
    """
    global _blizzard
    for _ in range(count):
        sf_length = random.randint(SNOWFLAKE_MIN_LENGTH, SNOWFLAKE_MAX_LENGTH)
        h_speed = round(remap_range(value=sf_length * random.uniform(0.7, 1),
                                    in_min=SNOWFLAKE_MIN_LENGTH, in_max=SNOWFLAKE_MAX_LENGTH, out_min=0, out_max=15))
        _blizzard.append({
            'x': random.randint(-sf_length * 2, sd.resolution[0]),
            'y': sd.resolution[1] + SNOWFLAKE_MAX_LENGTH,
            'length': sf_length,
            'factor_a': round(random.uniform(0.2, 1), 2),
            'factor_b': round(random.uniform(0.1, 1), 2),
            'factor_c': round(random.randint(20, 90), 2),
            'h_speed': h_speed,
            'v_speed': round(remap_range(value=sf_length, in_min=SNOWFLAKE_MIN_LENGTH,
                                         in_max=SNOWFLAKE_MAX_LENGTH, out_min=2, out_max=30)),
        })


def draw_snowflakes(color=sd.COLOR_WHITE):
    """Функция отрисовывает снежинки

    Parameters
    ----------
    color: tuple(int, int, int), default=(255, 255, 0)
        Цвет снежинок. Это кортеж (red, green, blue),
        где для каждый из трёх элементов цвета принимает значения от 0 до 255 включительно

    Returns
    -------
    """
    # мне кажется, что для большей гибкости кода и лучших результатов (уменьшения мерцания)
    # sd.start_drawing и sd.finish_drawing лучше вынести в основной модуль,
    # но поскольку в задании чётко указано обращаться ТОЛЬКО к функциям из этого модуля,
    # то я перенёс работу с фреймбуфером (кажется так это называется) в эту функцию
    global _blizzard
    sd.start_drawing()
    for snowflake in _blizzard:
        point = sd.get_point(snowflake['x'], snowflake['y'])
        sd.snowflake(
            center=point,
            length=snowflake['length'],
            factor_a=snowflake['factor_a'],
            factor_b=snowflake['factor_b'],
            factor_c=snowflake['factor_c'],
            color=color,
        )
    sd.finish_drawing()


def move_snowflakes():
    """Функция изменяет координаты снежинок в соответствии с параметрами

    """
    global _blizzard
    for snowflake in _blizzard:
        snowflake['h_speed'] = -snowflake['h_speed'] if random.randint(0, 100) < 2 else snowflake['h_speed']
        snowflake['x'] += snowflake['h_speed']
        snowflake['y'] -= snowflake['v_speed']


def get_offscreen_snowflakes():
    """Функция возвращает номера снежинок, вышедших за пределы экрана

    Returns
    -------
    Список номеров снежинок, вышедших за пределы экрана
    """
    global _blizzard
    # условие получается уж больно монструозным, поскольку я удаляю ещё и снежинки, вышедшие за вертикальные края экрана
    # двойная длина в условие добавлена для того, чтобы наверняка избавиться от белых артефактов с краёв экрана,
    # но при этом не зацепить снежинки, только что сгенерированные за краем экрана
    return [number for number, snowflake in enumerate(_blizzard)
            if ((snowflake['y'] < -snowflake['length'] * 2) or
                (snowflake['x'] < -snowflake['length'] * 2) or
                (snowflake['x'] > sd.resolution[0] + snowflake['length'] * 2))]


def delete_offscreen_snowflakes(snowflakes_numbers):
    """Функция удаляет из _blizzard снежинки с номерами, переданными в списке snowflakes_numbers

    Parameters
    ----------
    snowflakes_numbers: list of int
        список номеров снежинок для удаления

    """
    global _blizzard
    # сортируем номера по убыванию потому что при удалении элемента меняется индексация элементов правее него
    for number in sorted(snowflakes_numbers, reverse=True):
        del _blizzard[number]


# ------------------- тестовая демка для демонстрации концепта, описанного в модуле snowfall_module --------------------
def _get_snowdrift_snowflakes():
    """Функция возвращает номера снежинок, добавляемых в сугроб

    Returns
    -------
    Список номеров снежинок, добавляемых в сугроб
    """
    global _blizzard
    return [number for number, snowflake in enumerate(_blizzard) if (snowflake['y'] < snowflake['length'])]


def _draw_custom_snowflakes(snowflakes_numbers, color=sd.COLOR_WHITE):
    """Функция отрисовывает снежинки с заданными номерами

    Parameters
    ----------
    snowflakes_numbers: list of int
        Номера снежинок, которые необходимо нарисовать

    color: tuple(int, int, int), default=(255, 255, 0)
        Цвет снежинок. Это кортеж (red, green, blue),
        где для каждый из трёх элементов цвета принимает значения от 0 до 255 включительно

    Returns
    -------
    """
    global _blizzard
    snowflakes = [_blizzard[number] for number in snowflakes_numbers]
    for snowflake in snowflakes:
        point = sd.get_point(snowflake['x'], snowflake['y'])
        sd.snowflake(
            center=point,
            length=snowflake['length'],
            factor_a=snowflake['factor_a'],
            factor_b=snowflake['factor_b'],
            factor_c=snowflake['factor_c'],
            color=color,
        )


if __name__ == "__main__":
    fps = 24
    # на 24 фпс подлагивает, видимо, медленно работает sd.take_background.
    # Тут уже нужно копать в сторону сохранения фона не на диске, а в оперативной памяти
    generate_snowflakes(20)
    sd.take_background()
    while True:
        sd.start_drawing()

        snowdrift_snowflakes = _get_snowdrift_snowflakes()
        if snowdrift_snowflakes:
            sd.draw_background()
            _draw_custom_snowflakes(snowdrift_snowflakes)
            sd.take_background()
            delete_offscreen_snowflakes(snowdrift_snowflakes)
            generate_snowflakes(len(snowdrift_snowflakes))
        else:
            sd.draw_background()

        _draw_custom_snowflakes(range(len(_blizzard)))
        sd.finish_drawing()

        # draw_snowflakes(sd.COLOR_WHITE)

        move_snowflakes()
        sd.sleep(1 / fps)
        if sd.user_want_exit():
            break

    sd.pause()
