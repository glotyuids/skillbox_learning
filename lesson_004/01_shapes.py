# -*- coding: utf-8 -*-

import simple_draw as sd

# Часть 1.
# Написать функции рисования равносторонних геометрических фигур:
# - треугольника
# - квадрата
# - пятиугольника
# - шестиугольника
# Все функции должны принимать 3 параметра:
# - точка начала рисования
# - угол наклона
# - длина стороны
#
# Использование копи-пасты - обязательно! Даже тем кто уже знает про её пагубность. Для тренировки.
# Как работает копипаста:
#   - одну функцию написали,
#   - копипастим её, меняем название, чуть подправляем код,
#   - копипастим её, меняем название, чуть подправляем код,
#   - и так далее.
# В итоге должен получиться ПОЧТИ одинаковый код в каждой функции

# Пригодятся функции
# sd.get_point()
# sd.get_vector()
# sd.line()
# Результат решения см lesson_004/results/exercise_01_shapes.jpg


def draw_triangle(origin=None, angle=0, side_length=10):
    if not isinstance(origin, sd.Point):
        print('Incorrect point')
        return
    side_1 = sd.get_vector(start_point=origin, angle=angle, length=side_length)
    side_1.draw()
    side_2 = sd.get_vector(start_point=side_1.end_point, angle=angle + 120, length=side_length)
    side_2.draw()
    side_3 = sd.get_vector(start_point=side_2.end_point, angle=angle + 240, length=side_length)
    side_3.draw()


def draw_square(origin=None, angle=0, side_length=10):
    if not isinstance(origin, sd.Point):
        print('Incorrect point')
        return
    side_1 = sd.get_vector(start_point=origin, angle=angle, length=side_length)
    side_1.draw()
    side_2 = sd.get_vector(start_point=side_1.end_point, angle=angle + 90, length=side_length)
    side_2.draw()
    side_3 = sd.get_vector(start_point=side_2.end_point, angle=angle + 180, length=side_length)
    side_3.draw()
    side_4 = sd.get_vector(start_point=side_3.end_point, angle=angle + 270, length=side_length)
    side_4.draw()


def draw_pentagon(origin=None, angle=0, side_length=10):
    if not isinstance(origin, sd.Point):
        print('Incorrect point')
        return
    side_1 = sd.get_vector(start_point=origin, angle=angle, length=side_length)
    side_1.draw()
    side_2 = sd.get_vector(start_point=side_1.end_point, angle=angle + 72, length=side_length)
    side_2.draw()
    side_3 = sd.get_vector(start_point=side_2.end_point, angle=angle + 144, length=side_length)
    side_3.draw()
    side_4 = sd.get_vector(start_point=side_3.end_point, angle=angle + 216, length=side_length)
    side_4.draw()
    side_5 = sd.get_vector(start_point=side_4.end_point, angle=angle + 288, length=side_length)
    side_5.draw()


sd.resolution = (1200, 600)
common_origin = sd.get_point(100, 100)

draw_triangle(common_origin, 0, 200)
draw_square(common_origin, 0, 200)
draw_pentagon(common_origin, 0, 200)

# Часть 1-бис.
# Попробуйте прикинуть обьем работы, если нужно будет внести изменения в этот код.
# Скажем, связывать точки не линиями, а дугами. Или двойными линиями. Или рисовать круги в угловых точках. Или...
# А если таких функций не 4, а 44? Код писать не нужно, просто представь объем работы... и запомни это.

# Часть 2 (делается после зачета первой части)
#
# Надо сформировать функцию, параметризированную в местах где была "небольшая правка".
# Это называется "Выделить общую часть алгоритма в отдельную функцию"
# Потом надо изменить функции рисования конкретных фигур - вызывать общую функцию вместо "почти" одинакового кода.
#
# В итоге должно получиться:
#   - одна общая функция со множеством параметров,
#   - все функции отрисовки треугольника/квадрата/етс берут 3 параметра и внутри себя ВЫЗЫВАЮТ общую функцию.
#
# Не забудте в этой общей функции придумать, как устранить разрыв
#   в начальной/конечной точках рисуемой фигуры (если он есть)

# Часть 2-бис.
# А теперь - сколько надо работы что бы внести изменения в код? Выгода на лицо :)
# Поэтому среди программистов есть принцип D.R.Y. https://clck.ru/GEsA9
# Будьте ленивыми, не используйте копи-пасту!


sd.pause()