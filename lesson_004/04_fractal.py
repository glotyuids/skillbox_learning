# -*- coding: utf-8 -*-

import simple_draw as sd
import random

# 1) Написать функцию draw_branches, которая должна рисовать две ветви дерева из начальной точки
# Функция должна принимать параметры:
# - точка начала рисования,
# - угол рисования,
# - длина ветвей,
# Отклонение ветвей от угла рисования принять 30 градусов,

# 2) Сделать draw_branches рекурсивной
# - добавить проверку на длину ветвей, если длина меньше 10 - не рисовать
# - вызывать саму себя 2 раза из точек-концов нарисованных ветвей,
#   с параметром "угол рисования" равным углу только что нарисованной ветви,
#   и параметром "длинна ветвей" в 0.75 меньшей чем длина только что нарисованной ветви

# 3) Запустить вашу рекурсивную функцию, используя следующие параметры:
# root_point = sd.get_point(300, 30)
# draw_branches(start_point=root_point, angle=90, length=100)

# Пригодятся функции
# sd.get_point()
# sd.get_vector()
# Возможный результат решения см lesson_004/results/exercise_04_fractal_01.jpg

# можно поиграть -шрифтами- цветами и углами отклонения


def draw_branches(start_point, angle, length, color=sd.COLOR_BLUE):
    if length < random.randint(5, 10):
        return
    angle_shift = random.uniform(0.6, 1.4)
    branch1 = sd.get_vector(start_point=start_point, angle=angle + 30 * angle_shift, length=length)
    branch1.draw(color)
    angle_shift = random.uniform(0.6, 1.4)
    branch2 = sd.get_vector(start_point=start_point, angle=angle - 30 * angle_shift, length=length)
    branch2.draw(color)

    next_color = []
    for byte in color:
        byte += random.randint(0, 25)
        next_color.append(255 if byte > 255 else byte)
    next_color = tuple(next_color)

    next_length = length * .75 * random.uniform(0.8, 1.2)
    draw_branches(start_point=branch1.end_point, angle=branch1.angle, length=next_length, color=next_color)
    next_length = length * .75 * random.uniform(0.8, 1.2)
    draw_branches(start_point=branch2.end_point, angle=branch2.angle, length=next_length, color=next_color)


root_point = sd.get_point(300, 30)
draw_branches(start_point=root_point, angle=90, length=100)
# 4) Усложненное задание (делать по желанию)
# - сделать рандомное отклонение угла ветвей в пределах 40% от 30-ти градусов
# - сделать рандомное отклонение длины ветвей в пределах 20% от коэффициента 0.75
# Возможный результат решения см lesson_004/results/exercise_04_fractal_02.jpg

# Пригодятся функции
# sd.random_number()

sd.pause()

# зачет! Красивое дерево!
