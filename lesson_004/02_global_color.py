# -*- coding: utf-8 -*-
import simple_draw as sd

# Добавить цвет в функции рисования геом. фигур. из упр lesson_004/01_shapes.py
# (код функций скопировать сюда и изменить)
# Запросить у пользователя цвет фигуры посредством выбора из существующих:
#   вывести список всех цветов с номерами и ждать ввода номера желаемого цвета.
# Потом нарисовать все фигуры этим цветом

# Пригодятся функции
# sd.get_point()
# sd.line()
# sd.get_vector()
# и константы COLOR_RED, COLOR_ORANGE, COLOR_YELLOW, COLOR_GREEN, COLOR_CYAN, COLOR_BLUE, COLOR_PURPLE
# Результат решения см lesson_004/results/exercise_02_global_color.jpg

# TODO я так полагаю, здесь нам опять предлагают помучиться с копипастом? :)


def draw_triangle(origin=None, angle=0, side_length=10, color=sd.COLOR_YELLOW):
    if not isinstance(origin, sd.Point):
        print('Incorrect point')
        return
    side_1 = sd.get_vector(start_point=origin, angle=angle, length=side_length)
    side_1.draw(color=color)
    side_2 = sd.get_vector(start_point=side_1.end_point, angle=angle + 120, length=side_length)
    side_2.draw(color=color)
    side_3 = sd.get_vector(start_point=side_2.end_point, angle=angle + 240, length=side_length)
    side_3.draw(color=color)


def draw_square(origin=None, angle=0, side_length=10, color=sd.COLOR_YELLOW):
    if not isinstance(origin, sd.Point):
        print('Incorrect point')
        return
    side_1 = sd.get_vector(start_point=origin, angle=angle, length=side_length)
    side_1.draw(color=color)
    side_2 = sd.get_vector(start_point=side_1.end_point, angle=angle + 90, length=side_length)
    side_2.draw(color=color)
    side_3 = sd.get_vector(start_point=side_2.end_point, angle=angle + 180, length=side_length)
    side_3.draw(color=color)
    side_4 = sd.get_vector(start_point=side_3.end_point, angle=angle + 270, length=side_length)
    side_4.draw(color=color)


def draw_pentagon(origin=None, angle=0, side_length=10, color=sd.COLOR_YELLOW):
    if not isinstance(origin, sd.Point):
        print('Incorrect point')
        return
    side_1 = sd.get_vector(start_point=origin, angle=angle, length=side_length)
    side_1.draw(color=color)
    side_2 = sd.get_vector(start_point=side_1.end_point, angle=angle + 72, length=side_length)
    side_2.draw(color=color)
    side_3 = sd.get_vector(start_point=side_2.end_point, angle=angle + 144, length=side_length)
    side_3.draw(color=color)
    side_4 = sd.get_vector(start_point=side_3.end_point, angle=angle + 216, length=side_length)
    side_4.draw(color=color)
    side_5 = sd.get_vector(start_point=side_4.end_point, angle=angle + 288, length=side_length)
    side_5.draw(color=color)


def draw_hexagon(origin=None, angle=0, side_length=10, color=sd.COLOR_YELLOW):
    if not isinstance(origin, sd.Point):
        print('Incorrect point')
        return
    side_1 = sd.get_vector(start_point=origin, angle=angle, length=side_length)
    side_1.draw(color=color)
    side_2 = sd.get_vector(start_point=side_1.end_point, angle=angle + 60, length=side_length)
    side_2.draw(color=color)
    side_3 = sd.get_vector(start_point=side_2.end_point, angle=angle + 120, length=side_length)
    side_3.draw(color=color)
    side_4 = sd.get_vector(start_point=side_3.end_point, angle=angle + 180, length=side_length)
    side_4.draw(color=color)
    side_5 = sd.get_vector(start_point=side_4.end_point, angle=angle + 240, length=side_length)
    side_5.draw(color=color)
    side_6 = sd.get_vector(start_point=side_5.end_point, angle=angle + 300, length=side_length)
    side_6.draw(color=color)


# с вашего позволения я немного отклонюсь от задания
#     и чтобы было интереснее буду считывать не номер цвета, а его название
global_color = None
while not global_color:
    user_answer = input('Назовите цвет радуги, которым вы хотите нарисовать фигуры? > ')
    user_answer = user_answer.lower()

    # узнаём цвет, который ввёл пользователь
    # принцип: сопоставляем корень слова-названия цвета с константой цвета,
    #   затем ищем корень в строке, которую ввёл пользователь и возвращаем соответствующий цвет
    color_name_roots = ['красн', 'оранж', 'желт', 'жёлт', 'зелен', 'зелён', 'голуб', 'син', 'фиол', ]
    colors = [sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_YELLOW, sd.COLOR_GREEN,
              sd.COLOR_GREEN, sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE, ]
    # TODO Это константы и они должны быть определены в начале модуля. Но ещё лучше, сделайте одну единственную
    #  константу (список словарей) такого вида:
    COLORS = [
        {'name': 'Красный', 'code': sd.COLOR_RED},
        {'name': 'Оранжевый', 'code': sd.COLOR_ORANGE},
        ...
    ]
    # TODO Меню лучше сделайте цифровое (enumerate пригодится), "жестоко" заставлять пользователя писать цвета :)
    for root, color in zip(color_name_roots, colors):
        if root in user_answer:
            global_color = color
            break

    if not global_color:
        print('\nВы ввели некорректный цвет. Напишите на русском языке один из цветов радуги:\n'
              'Подсказка: красный, оранжевый, жёлтый, зелёный, голубой, синий, фиолетовый')

sd.resolution = (600, 600)
triangle_origin = sd.get_point(50, 50)
draw_triangle(origin=triangle_origin, angle=20, side_length=100, color=global_color)

square_origin = sd.get_point(300, 50)
draw_square(origin=square_origin, angle=0, side_length=100, color=global_color)

pentagon_origin = sd.get_point(150, 300)
draw_pentagon(origin=pentagon_origin, angle=45, side_length=100, color=global_color)

hexagon_origin = sd.get_point(450, 300)
draw_hexagon(origin=hexagon_origin, angle=74, side_length=100, color=global_color)

sd.pause()
