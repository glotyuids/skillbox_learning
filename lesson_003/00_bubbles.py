# -*- coding: utf-8 -*-

from random import randint
import simple_draw as sd

sd.resolution = (1200, 600)

# Нарисовать пузырек - три вложенных окружностей с шагом 5 пикселей
circle_center = sd.get_point(100, 100)
radius = 60
for _ in range(3):
    sd.circle(circle_center, radius, width=2)
    radius += 5

sd.sleep(1)
sd.clear_screen()


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
    # Вроде бы оверкилл, но я должен был попробовать запилить такой докстринг
    for _ in range(3):
        sd.circle(center, inner_radius, color, line_width)
        inner_radius += step


# Нарисовать 10 пузырьков в ряд
x = 100
for _ in range(10):
    circle_center = sd.get_point(x, 500)
    draw_bubble(circle_center)
    x += 100

sd.sleep(1)
sd.clear_screen()


# Нарисовать три ряда по 10 пузырьков
y = 300
for _ in range(3):
    x = 300
    for _ in range(10):
        circle_center = sd.get_point(x, y)
        draw_bubble(circle_center, 20, line_width=1, step=3)
        x += 50
    y += 50

sd.sleep(1)
sd.clear_screen()

# Нарисовать 100 пузырьков в произвольных местах экрана случайными цветами
"""
хотел здесь после пятисекундной паузы почистить экран, но кажется, что констукция
sd.start_drawing() 
...
sd.finish_drawing()
sd.sleep(5)
sd.start_drawing() 
...
sd.finish_drawing()
работает некорректно. Вместо того, чтобы вывести буфер и приостановить вывод на 5 секунд, 
окно просто на эти 5 секунд подвисает без какого-либо вывода
"""
# Именно так и должна работать sd.sleep(5)!  А пара функций start/finish_drawing ускоряет вывод графики, но ни на
#  очистку, ни на паузу никак не влияет. Паузы и очистку вставил сам при проверке.
# TODO Это я всё понял. Значит всё таки косяк из-за работы под макосью

for _ in range(100):
    bubble_center = sd.random_point()
    color = sd.random_color()
    bubble_radius = randint(10, 100)
    draw_bubble(bubble_center, bubble_radius, line_width=1, step=3, color=color)

sd.pause()

# зачет! На вопрос ответил выше

