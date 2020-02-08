# -*- coding: utf-8 -*-

# (цикл for)
import simple_draw

# Нарисовать стену из кирпичей. Размер кирпича - 100х50
# Использовать вложенные циклы for
BRICK_WIDTH = 100
BRICK_HEIGHT = 50
simple_draw.resolution = (1262, 615)

# Для создная гибкого кода важно как можно меньше использовать харкод - числа, строки, а вмест них использовать
#  константы и/или программые способы их получения:
#  1) введите константы размеров кирпича
#  2) там где нужны размеры окна вывода используйте sd.resolution


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
    simple_draw.rectangle(left_bottom, right_top, color=simple_draw.COLOR_DARK_RED, width=0)
    simple_draw.rectangle(left_bottom, right_top, color=simple_draw.COLOR_BLACK, width=1)


def draw_brick_line(x, y, line_width, brick_width=100, brick_height=50):
    """Draws line of bricks

    Parameters
    ----------


    x, y : int
        Bottom left point of first brick

    line_width : int
        Width of bricks line in pixels

    brick_width : int, default=100
        Width of brick

    brick_height : int, default=50
        Height of brick

    """
    #  Здесь к конечной точке (второй аргумент range) добавил ширину кирпича, чтобы был заполнен весь экран.
    #  Если этого не сделать, то в смещённых по x строках не будет хватать одного кирпича. Можете проверить
    # Согласен, у вас немного другая отрисовка кирпича, а когда их рисуют просто контуром, то эта "нехватка" не заметна
    for x in range(x, x + line_width + brick_width, brick_width):
        draw_brick(x, y, brick_width, brick_height)


for y in range(0, simple_draw.resolution[1], BRICK_HEIGHT):
    x = 0 if y % (BRICK_HEIGHT * 2) else -BRICK_WIDTH // 2
    # Убрал сравнение с нулём, это избыточно, на практике так не делают
    draw_brick_line(x, y, simple_draw.resolution[0], BRICK_WIDTH, BRICK_HEIGHT)

simple_draw.pause()

# зачет!
