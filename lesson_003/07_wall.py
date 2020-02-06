# -*- coding: utf-8 -*-

# (цикл for)
import simple_draw

# Нарисовать стену из кирпичей. Размер кирпича - 100х50
# Использовать вложенные циклы for

simple_draw.resolution = (1200, 600)


def draw_brick(x, y, width=100, height=50):
    """Draws a brick

    Parameters
    ----------
    x, y : int
        Bottom left point of brick

    width : int, default=100
        Width of brick

    height : int, default=50
        Height of brick

    """
    left_bottom = simple_draw.get_point(x, y)
    right_top = simple_draw.get_point(x + width, y + height)
    simple_draw.rectangle(left_bottom, right_top, width=1)


def draw_brick_line (x, y, count):
    """Draws line of bricks

    Parameters
    ----------
    x, y : int
        Bottom left point of first brick

    count : int
        Count of bricks in line

    """
    next_x = x
    for _ in range(count):
        draw_brick(next_x, y)
        next_x += 100


wall_width = simple_draw.resolution[0] // 100 + 1   # +1 для того, чтобы при смещении на полкирпича всё было корректно
wall_height = simple_draw.resolution[1] // 50 + 1   # +1 на случай, если размер окна не кратен размеру кирпича

for i in range(wall_height):
    line_y = i * 50
    if i % 2 == 0:
       line_x = 0
    else:
        line_x = -50
    draw_brick_line(line_x, line_y, wall_width)

simple_draw.pause()
