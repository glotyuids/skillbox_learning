# -*- coding: utf-8 -*-

import simple_draw as sd

# Запросить у пользователя желаемую фигуру посредством выбора из существующих
#   вывести список всех фигур с номерами и ждать ввода номера желаемой фигуры.
# и нарисовать эту фигуру в центре экрана

# Код функций из упр lesson_004/02_global_color.py скопировать сюда
# Результат решения см lesson_004/results/exercise_03_shape_select.jpg

COLORS = [
        {'name': 'красный', 'name_root': 'красн', 'code': sd.COLOR_RED},
        {'name': 'оранжевый', 'name_root': 'оранж', 'code': sd.COLOR_ORANGE},
        {'name': 'жёлтый', 'name_root': 'желт', 'code': sd.COLOR_YELLOW},
        {'name': 'зелёный', 'name_root': 'зелен', 'code': sd.COLOR_GREEN},
        {'name': 'голубой', 'name_root': 'голуб', 'code': sd.COLOR_CYAN},
        {'name': 'синий', 'name_root': 'син', 'code': sd.COLOR_BLUE},
        {'name': 'фиолетовый', 'name_root': 'фиол', 'code': sd.COLOR_PURPLE},
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
    for number, color in enumerate(COLORS):
        print(f' {number} - {color["name"]}')
    user_answer = input('Введите номер или назовите цвет радуги, '
                        'которым вы хотите нарисовать фигуры > ')
    user_answer = user_answer.lower().replace('ё', 'е')

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
polygon_function = None
while not polygon_function:
    user_answer = input('Сколько сторон должно быть у фигуры: 3, 4, 5 или 6? > ')

    polygons = ['3', '4', '5', '6', ]
    # TODO Оригинальное решение! Теперь реализуйте для тренировки такую структуру:
    # FIGURES = [
    #     {'name': 'треугольник', 'function': draw_triangle},
    #     ...
    # ]
    #  Не совсем понимаю, зачем именно такую. Фактически достаточно списка.
    #  Я правильно понял, здесь вы предлагаете разобраться, что функции - это тоже объекты с которыми можно работать?
    # TODO Именно, что функции это данные, которые можно хранить, передавать и т.п. Не во всех языках это есть.
    FIGURES = [draw_triangle, draw_square, draw_pentagon, draw_hexagon, ]
    # TODO В таком виде, когда отдельно меню polygons и отдельно список функций, выходит, что при добавлении новой
    #  фигуры это нужно делать согласовано в обоих константах, что не так удобно, когда структура данных одна

    # Получайте выбранную пользователем функцию и вызывайте её с нужными параметрами (можно даже одинаковыми для
    #  всех)
    if user_answer in polygons:
        polygon_function = FIGURES[int(user_answer) - 3]

    else:
        print('\nКажется, вы случайно ввели не тот номер. Попробуйте ещё раз.')

sd.resolution = (600, 600)

polygon_origin = sd.get_point(100, 100)
polygon_function(origin=polygon_origin, angle=20, side_length=100, color=global_color)


sd.pause()
