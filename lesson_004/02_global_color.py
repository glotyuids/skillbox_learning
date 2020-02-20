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
        {'name_root': 'красн', 'code': sd.COLOR_RED},
        {'name_root': 'оранж', 'code': sd.COLOR_ORANGE},
        {'name_root': 'желт', 'code': sd.COLOR_YELLOW},
        {'name_root': 'зелен', 'code': sd.COLOR_GREEN},
        {'name_root': 'голуб', 'code': sd.COLOR_CYAN},
        {'name_root': 'син', 'code': sd.COLOR_BLUE},
        {'name_root': 'фиол', 'code': sd.COLOR_PURPLE},
        {'name_root': 'жёлт', 'code': sd.COLOR_YELLOW},
        {'name_root': 'зелён', 'code': sd.COLOR_GREEN},
]


def draw_polygon(origin=None, angle=0, side_length=10, sides_number=4, color=sd.COLOR_YELLOW):
    if not isinstance(origin, sd.Point):
        print('Incorrect point')
        return
    angle_step = 360 / sides_number
    next_start_point = origin
    next_angle = angle
    for _ in range(sides_number - 1):
        side = sd.get_vector(start_point=next_start_point, angle=next_angle, length=side_length)
        side.draw(color=color)
        next_start_point = side.end_point
        next_angle += angle_step
    sd.line(next_start_point, origin, color)       # небольшой хак для того, чтобы контур фигуры был замкнутым


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
    print(' 0 - красный, \n'
          ' 1 - оранжевый, \n'
          ' 2 - жёлтый, \n'
          ' 3 - зелёный, \n'
          ' 4 - голубой, \n'
          ' 5 - синий, \n'
          ' 6 - фиолетовый')
    user_answer = input('Введите номер или назовите цвет радуги, '
                        'которым вы хотите нарисовать фигуры > ')
    user_answer = user_answer.lower()

    # Это константы и они должны быть определены в начале модуля. Но ещё лучше, сделайте одну единственную
    #  константу (список словарей)
    # TODO Сделано) Кстати, константы лучше выносить вверх,
    #  или же оставлять недалеко от того места, где они используются?

    # Меню лучше сделайте цифровое (enumerate пригодится), "жестоко" заставлять пользователя писать цвета :)
    # TODO Реализовал оба варианта :)

    # если пользователь ввёл число, то просто дёргаем цвет по номеру из COLORS
    if user_answer.isnumeric():
        user_answer = int(user_answer)
        if 0 <= user_answer <= 6:
            global_color = COLORS[user_answer]['code']

    else:
        # перебирая цвета ищем корень в строке, которую ввёл пользователь и возвращаем соответствующий цвет
        for color in COLORS:
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
