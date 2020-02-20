# -*- coding: utf-8 -*-

import simple_draw as sd

# Запросить у пользователя желаемую фигуру посредством выбора из существующих
#   вывести список всех фигур с номерами и ждать ввода номера желаемой фигуры.
# и нарисовать эту фигуру в центре экрана

# Код функций из упр lesson_004/02_global_color.py скопировать сюда
# Результат решения см lesson_004/results/exercise_03_shape_select.jpg

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


# спрашиваем цвет
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

# спрашиваем количество сторон
polygon_sides_number = None
while not polygon_sides_number:
    user_answer = input('Сколько сторон должно быть у фигуры: 3, 4, 5 или 6? > ')

    polygons = ['3', '4', '5', '6', ]
    # TODO Оригинальное решение! Теперь реализуйте для тренировки такую структуру:
    FIGURES = [
        {'name': 'треугольник', 'function': draw_triangle},
        ...
    ]
    # TODO Получайте выбранную пользователем функцию и вызывайте её с нужными параметрами (можно даже одинаковыми для
    #  всех)
    if user_answer in polygons:
        polygon_sides_number = int(user_answer)
    else:
        print('\nКажется, вы случайно ввели не тот номер. Попробуйте ещё раз.')

sd.resolution = (600, 600)

if polygon_sides_number == 3:
    triangle_origin = sd.get_point(50, 50)
    draw_triangle(origin=triangle_origin, angle=20, side_length=100, color=global_color)
elif polygon_sides_number == 4:
    square_origin = sd.get_point(300, 50)
    draw_square(origin=square_origin, angle=0, side_length=100, color=global_color)
elif polygon_sides_number == 5:
    pentagon_origin = sd.get_point(150, 300)
    draw_pentagon(origin=pentagon_origin, angle=45, side_length=100, color=global_color)
elif polygon_sides_number == 6:
    hexagon_origin = sd.get_point(450, 300)
    draw_hexagon(origin=hexagon_origin, angle=74, side_length=100, color=global_color)

sd.pause()
