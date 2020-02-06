# -*- coding: utf-8 -*-

# (определение функций)
import simple_draw

# Написать функцию отрисовки смайлика по заданным координатам
# Форма рожицы-смайлика на ваше усмотрение
# Параметры функции: кордината X, координата Y, цвет.
# Вывести 10 смайликов в произвольных точках экрана.


def draw_smile(x, y, color=simple_draw.COLOR_YELLOW):
    pass
#   TODO Здесь собираем морду
    scale = 10
    draw_head(x, y + 13, scale, color)
    draw_mouth(x + 1, y + 12, scale)


def draw_head(x, y, scale=1, color=simple_draw.COLOR_YELLOW):
    for i in range(5):
        left_bottom_x = (x + i) * scale
        left_bottom_y = (y + 5 - i) * scale
        left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

        right_top_x = (x + 16 - i) * scale
        right_top_y = (y + 13 + i) * scale
        right_top = simple_draw.get_point(right_top_x, right_top_y)

        simple_draw.rectangle(left_bottom, right_top, color, 0)


def draw_mouth(x, y, scale=1):
#   TODO Здесь рисуем рот
    # Outline
    left_bottom_x = x * scale
    left_bottom_y = (y + 4) * scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = (x + 14) * scale
    right_top_y = (y + 8) * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    for i in range(1, 5):
        left_bottom_x = (x + i) * scale
        left_bottom_y = (y + 4 - i) * scale
        left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

        right_top_x = (x + 14 - i) * scale
        right_top_y = (y + 5 - i) * scale
        right_top = simple_draw.get_point(right_top_x, right_top_y)

        simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    # Background
    left_bottom_x = (x + 1) * scale
    left_bottom_y = (y + 4) * scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = (x + 13) * scale
    right_top_y = (y + 7) * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_WHITE, 0)

    for i in range(1, 4):
        left_bottom_x = (x + i + 1) * scale
        left_bottom_y = (y + 4 - i) * scale
        left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

        right_top_x = (x + 13 - i) * scale
        right_top_y = (y + 5 - i) * scale
        right_top = simple_draw.get_point(right_top_x, right_top_y)

        simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_WHITE, 0)

    # Teeth
    left_bottom_x = (x + 4) * scale
    left_bottom_y = y * scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = (x + 5) * scale
    right_top_y = (y + 7) * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    left_bottom_x = (x + 9) * scale
    left_bottom_y = y * scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = (x + 10) * scale
    right_top_y = (y + 7) * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)


def draw_eyes(x, y):
    pass
#   TODO Здесь рисуем глаза


def draw_beard(x, y):
    pass
#   TODO Здесь рисуем бороду

simple_draw.resolution = (1200, 600)

draw_smile(10, 10)



simple_draw.pause()
