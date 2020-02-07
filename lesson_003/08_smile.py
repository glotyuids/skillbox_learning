# -*- coding: utf-8 -*-

# (определение функций)
from random import randint
import simple_draw

# Написать функцию отрисовки смайлика по заданным координатам
# Форма рожицы-смайлика на ваше усмотрение
# Параметры функции: кордината X, координата Y, цвет.
# Вывести 10 смайликов в произвольных точках экрана.


def draw_smile(x, y, color=simple_draw.COLOR_YELLOW, scale=1):
    draw_head(x, y + 13 * scale, scale, color)
    draw_eyes(x + 4 * scale, y + 22 * scale, scale)
    draw_beard(x, y, scale)
    draw_mouth(x, y + 13 * scale, scale)


def draw_head(x, y, scale=1, color=simple_draw.COLOR_YELLOW):
    for i in range(5):
        left_bottom_x = x + i * scale
        left_bottom_y = y + (5 - i) * scale
        left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

        right_top_x = x + (16 - i) * scale
        right_top_y = y + (13 + i) * scale
        right_top = simple_draw.get_point(right_top_x, right_top_y)

        simple_draw.rectangle(left_bottom, right_top, color, 0)


def draw_mouth(x, y, scale=1):
    # Outline
    left_bottom_x = x + scale
    left_bottom_y = y + 4 * scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = x + 15 * scale
    right_top_y = y + 8 * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    for i in range(1, 5):
        left_bottom_x = x + (1 + i) * scale
        left_bottom_y = y + (4 - i) * scale
        left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

        right_top_x = x + (15 - i) * scale
        right_top_y = y + (5 - i) * scale
        right_top = simple_draw.get_point(right_top_x, right_top_y)

        simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    # Background
    left_bottom_x = x + 2 * scale
    left_bottom_y = y + 4 * scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = x + 14 * scale
    right_top_y = y + 7 * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_WHITE, 0)

    for i in range(1, 4):
        left_bottom_x = x + (i + 2) * scale
        left_bottom_y = y + (4 - i) * scale
        left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

        right_top_x = x + (14 - i) * scale
        right_top_y = y + (5 - i) * scale
        right_top = simple_draw.get_point(right_top_x, right_top_y)

        simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_WHITE, 0)

    # Teeth
    left_bottom_x = x + 5 * scale
    left_bottom_y = y
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = x + 6 * scale
    right_top_y = y + 7 * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    left_bottom_x = x + 10 * scale
    left_bottom_y = y
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = x + 11 * scale
    right_top_y = y + 7 * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)


def draw_eyes(x, y, scale=1):
    # Left eye
    for i in range(2):
        left_bottom_x = x + i * scale
        left_bottom_y = y
        left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

        right_top_x = x + 3 * scale
        right_top_y = y + (3 + i) * scale
        right_top = simple_draw.get_point(right_top_x, right_top_y)

        simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_WHITE, 0)

    # Left pupil
    left_bottom_x = x + scale
    left_bottom_y = y + scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = x + 3 * scale
    right_top_y = y + 3 * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    # Right eye
    for i in range(2):
        left_bottom_x = x + 4 * scale
        left_bottom_y = y
        left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

        right_top_x = x + (6 + i) * scale
        right_top_y = y + (4 - i) * scale
        right_top = simple_draw.get_point(right_top_x, right_top_y)

        simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_WHITE, 0)

    # Right pupil
    left_bottom_x = x + 4 * scale
    left_bottom_y = y + scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = x + 6 * scale
    right_top_y = y + 3 * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    # Left eyebrow
    left_bottom_x = x
    left_bottom_y = y + 4 * scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = x + 3 * scale
    right_top_y = y + 5 * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    # Right eyebrow
    left_bottom_x = x + 5 * scale
    left_bottom_y = y + 5 * scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = x + 7 * scale
    right_top_y = y + 6 * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    left_bottom_x = x + 7 * scale
    left_bottom_y = y + 4 * scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = x + 8 * scale
    right_top_y = y + 5 * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)


def draw_vertical_rectangle(x, y_top, y_bottom, color=simple_draw.COLOR_YELLOW, scale=1):
    left_bottom = simple_draw.get_point(x, y_bottom)
    right_top = simple_draw.get_point(x + scale, y_top)
    simple_draw.rectangle(left_bottom, right_top, color, 0)


def draw_beard(x, y, scale=1):
    beard = [5, 7, 8, 12, 16, 15, 18, 20, 19, 17, 14, 13, 10, 8, 7, 4]
    hair_y_top = y + 20 * scale
    for i, hair in enumerate(beard):
        hair_x = x + i * scale
        hair_y_bottom = hair_y_top - hair * scale
        draw_vertical_rectangle(hair_x, hair_y_top, hair_y_bottom, simple_draw.COLOR_WHITE, scale)


simple_draw.resolution = (1200, 600)

scale = 5
for _ in range(10):
    smile_x = randint(0, simple_draw.resolution[0] - scale * 16)
    smile_y = randint(0, simple_draw.resolution[1] - scale * 29)
    smile_color = simple_draw.random_color()
    draw_smile(smile_x, smile_y, smile_color, scale)


simple_draw.pause()

# зачет! Отличный смайл! Не забудьте запостить его в телеграм-канал с тегом #оцените
