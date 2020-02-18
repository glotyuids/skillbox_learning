# -*- coding: utf-8 -*-

import simple_draw as sd

# Запросить у пользователя желаемую фигуру посредством выбора из существующих
#   вывести список всех фигур с номерами и ждать ввода номера желаемой фигуры.
# и нарисовать эту фигуру в центре экрана

# Код функций из упр lesson_004/02_global_color.py скопировать сюда
# Результат решения см lesson_004/results/exercise_03_shape_select.jpg

# TODO продолжаем мучиться с копипастом :D


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


# спрашиваем цвет
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
    for root, color in zip(color_name_roots, colors):
        if root in user_answer:
            global_color = color
            break

    if not global_color:
        print('\nВы ввели некорректный цвет. Напишите на русском языке один из цветов радуги:\n'
              'Подсказка: красный, оранжевый, жёлтый, зелёный, голубой, синий, фиолетовый')

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
