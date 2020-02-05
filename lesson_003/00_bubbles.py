# -*- coding: utf-8 -*-

import simple_draw as sd

sd.resolution = (1200, 600)

# Нарисовать пузырек - три вложенных окружностей с шагом 5 пикселей
circle_center = sd.get_point(100, 100)
radius = 60
for _ in range(3):
    sd.circle(circle_center, radius, width=2)
    radius += 5


# Написать функцию рисования пузырька, принммающую 3 (или более) параметра: точка рисования, шаг и цвет
def draw_bubble(center, inner_radius=60, step=5, color=(255, 255, 0), line_width=2):
    """Draws a bubble of three circles.

    Parameters
    ----------
    center : simple_draw Point
        Center of bubble

    inner_radius : int, default=60
        Radius of inner circle

    step : int, default=5
        Step of increasing the radius of the circles

    color : tuple(int, int, int), default=(255, 255, 0)
        Color of circles. Accepts tuple(red, green, blue),
        where color value between 0 and 255, including both of them

    line_width : int, default=2
        Circle line width

    """
    for _ in range(3):
        sd.circle(center, inner_radius, color, line_width)
        inner_radius += step


# Нарисовать 10 пузырьков в ряд
# TODO здесь ваш код

# Нарисовать три ряда по 10 пузырьков
# TODO здесь ваш код

# Нарисовать 100 пузырьков в произвольных местах экрана случайными цветами
# TODO здесь ваш код

sd.pause()


