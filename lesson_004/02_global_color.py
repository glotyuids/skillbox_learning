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

COLORS = [
        {'name': 'красный', 'name_root': 'красн', 'code': sd.COLOR_RED},
        {'name': 'оранжевый', 'name_root': 'оранж', 'code': sd.COLOR_ORANGE},
        {'name': 'жёлтый', 'name_root': 'желт', 'code': sd.COLOR_YELLOW},
        {'name': 'зелёный', 'name_root': 'зелен', 'code': sd.COLOR_GREEN},
        {'name': 'голубой', 'name_root': 'голуб', 'code': sd.COLOR_CYAN},
        {'name': 'синий', 'name_root': 'син', 'code': sd.COLOR_BLUE},
        {'name': 'фиолетовый', 'name_root': 'фиол', 'code': sd.COLOR_PURPLE},
]
# Задумка была как раз в том, чтобы использовать эту структуру данных и для вывода меню и для получения кода цвета.
#  Напишите цвета полностью и выводите меню используя enumerate
# TODO Всё же для имени цвета выделю отдельный ключ. Причины - в тудушке ниже


def draw_polygon(origin=None, angle=0, side_length=10, sides_number=4, color=sd.COLOR_YELLOW):
    if not isinstance(origin, sd.Point):
        print('Incorrect point')
        return
    angle_step = round(360 / sides_number)
    next_start_point = origin

    for next_angle in range(angle, 360 + angle - angle_step, angle_step):
        next_start_point = sd.vector(start=next_start_point, angle=next_angle, length=side_length, color=color)

    sd.line(next_start_point, origin, color=color)


def draw_triangle(origin=None, angle=0, side_length=10, color=sd.COLOR_YELLOW):
    draw_polygon(origin=origin, angle=angle, side_length=side_length, sides_number=3, color=color)


def draw_square(origin=None, angle=0, side_length=10, color=sd.COLOR_YELLOW):
    draw_polygon(origin=origin, angle=angle, side_length=side_length, sides_number=4, color=color)


def draw_pentagon(origin=None, angle=0, side_length=10, color=sd.COLOR_YELLOW):
    draw_polygon(origin=origin, angle=angle, side_length=side_length, sides_number=5, color=color)


def draw_hexagon(origin=None, angle=0, side_length=10, color=sd.COLOR_YELLOW):
    draw_polygon(origin=origin, angle=angle, side_length=side_length, sides_number=6, color=color)


global_color = None
while not global_color:
    for number, color in enumerate(COLORS):
        print(f' {number} - {color["name"]}')
    # Константа данных о цветах для того и введена, чтобы если понадобится добавить цвет, это можно было сделать в
    #  одном месте. А сейчас у вас меню независимое от самих цветов, это не удобно и избыточно.
    # TODO Теперь понял. Логично, так обслуживание кода будет проще

    user_answer = input('Введите номер или назовите цвет радуги, '
                        'которым вы хотите нарисовать фигуры > ')
    user_answer = user_answer.lower().replace('ё', 'е')

    # Это константы и они должны быть определены в начале модуля. Но ещё лучше, сделайте одну единственную
    #  константу (список словарей)
    # Сделано) Кстати, константы лучше выносить вверх,
    #  или же оставлять недалеко от того места, где они используются?
    # Константы должны быть сразу после импортов сторонних модулей. Там их легче найти при надобности

    # Меню лучше сделайте цифровое (enumerate пригодится), "жестоко" заставлять пользователя писать цвета :)
    # Реализовал оба варианта :)

    # если пользователь ввёл число, то просто дёргаем цвет по номеру из COLORS
    if user_answer.isnumeric():
        user_answer = int(user_answer)
        if 0 <= user_answer <= len(COLORS):
            global_color = COLORS[user_answer]['code']

    else:
        # перебирая цвета ищем корень в строке, которую ввёл пользователь и возвращаем соответствующий цвет
        for color in COLORS:
            # Если вас так это вдохновило, то можно переделать на оборот: искать вхождение ответа
            #  пользователя в значения по ключу name. Не помешает преобразование к нижнему регистру ответа пользователя
            # TODO преобразование к нижнему регистру делаётся сразу после считывания.
            #  Я проверяю вхождение ответа в занчения по корню слова,
            #  поскольку на входе могут быть строки вроде "зелёненький".
            if color['name_root'] in user_answer:
                global_color = color['code']
                break

    if not global_color:
        print('\nВы ввели некорректный цвет. Напишите на русском языке один из цветов радуги, либо введите его номер.\n'
              'Подсказка:')


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
