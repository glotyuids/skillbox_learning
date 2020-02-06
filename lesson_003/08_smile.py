# -*- coding: utf-8 -*-

# (определение функций)
import simple_draw

# Написать функцию отрисовки смайлика по заданным координатам
# Форма рожицы-смайлика на ваше усмотрение
# Параметры функции: кордината X, координата Y, цвет.
# Вывести 10 смайликов в произвольных точках экрана.


def draw_smile(x, y, color=simple_draw.COLOR_YELLOW):
    scale = 10
    draw_head(x, y + 13, scale, color)
    draw_eyes(x + 4, y + 22, scale)
    draw_beard(x, y, scale)
    draw_mouth(x + 1, y + 13, scale)


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


def draw_eyes(x, y, scale=1):
    # Left eye
    for i in range(2):
        left_bottom_x = (x + i) * scale
        left_bottom_y = y * scale
        left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

        right_top_x = (x + 3) * scale
        right_top_y = (y + 3 + i) * scale
        right_top = simple_draw.get_point(right_top_x, right_top_y)

        simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_WHITE, 0)

    # Left pupil
    left_bottom_x = (x + 1) * scale
    left_bottom_y = (y + 1) * scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = (x + 3) * scale
    right_top_y = (y + 3) * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    # Right eye
    for i in range(2):
        left_bottom_x = (x + 4) * scale
        left_bottom_y = y * scale
        left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

        right_top_x = (x + 6 + i) * scale
        right_top_y = (y + 4 - i) * scale
        right_top = simple_draw.get_point(right_top_x, right_top_y)

        simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_WHITE, 0)

    # Right pupil
    left_bottom_x = (x + 4) * scale
    left_bottom_y = (y + 1) * scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = (x + 6) * scale
    right_top_y = (y + 3) * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    # Left eyebrow
    left_bottom_x = x * scale
    left_bottom_y = (y + 4) * scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = (x + 3) * scale
    right_top_y = (y + 5) * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    # Right eyebrow
    left_bottom_x = (x + 5) * scale
    left_bottom_y = (y + 5) * scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = (x + 7) * scale
    right_top_y = (y + 6) * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    left_bottom_x = (x + 7) * scale
    left_bottom_y = (y + 4) * scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = (x + 8) * scale
    right_top_y = (y + 5) * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)


def draw_vertical_rectangle (x, y_top, y_bottom, color=simple_draw.COLOR_YELLOW, scale=1):
    left_bottom = simple_draw.get_point(x * scale, y_bottom * scale)
    right_top = simple_draw.get_point((x + 1) * scale, y_top * scale)
    simple_draw.rectangle(left_bottom, right_top, color, 0)


def draw_beard(x, y, scale=1):
    beard = [5, 7, 8, 12, 16, 15, 18, 20, 19, 17, 14, 13, 10, 8, 7, 4]
    hair_y_top = y + 20
    for i, hair in enumerate(beard):
        hair_x = x + i
        hair_y_bottom = hair_y_top - hair
        draw_vertical_rectangle(hair_x, hair_y_top, hair_y_bottom, simple_draw.COLOR_WHITE, scale)


simple_draw.resolution = (1200, 600)

draw_smile(10, 10)

simple_draw.pause()
