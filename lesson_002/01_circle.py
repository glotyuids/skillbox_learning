#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть значение радиуса круга
radius = 42

# Выведите на консоль значение прощади этого круга с точностю до 4-х знаков после запятой
# подсказки:
#       формулу можно подсмотреть в интернете,
#       пи возьмите равным 3.1415926
#       точность указывается в функции round()
circle_area = 3.1415926 * radius ** 2
circle_area = round(circle_area, 4)
print(circle_area)


# Далее, пусть есть координаты точки
point_1 = (23, 34)
# где 23 - координата х, 34 - координата у

# Если точка point лежит внутри того самого круга [центр в начале координат (0, 0), radius = 42],
# то выведите на консоль True, Или False, если точка лежит вовне круга.
# подсказки:
#       нужно определить расстояние от этой точки до начала координат (0, 0)
#       формула так же есть в интернете
#       квадратный корень - это возведение в степень 0.5
#       операции сравнения дают булевы константы True и False


def calculate_distance(cite1, cite2):
    distance = ((cite1[0] - cite2[0]) ** 2 + (cite1[1] - cite2[1]) ** 2) ** 0.5
    return distance


origin = (0, 0)
origin_point1 = calculate_distance(origin, point_1)
print(True if origin_point1 <= radius else False)   # не знал, что так можно делать. спасибо

# Аналогично для другой точки
point_2 = (30, 30)
# Если точка point_2 лежит внутри круга (radius = 42), то выведите на консоль True,
# Или False, если точка лежит вовне круга.
origin_point2 = calculate_distance(origin, point_2)
print(True if origin_point2 <= radius else False)

# Пример вывода на консоль:
#
# 77777.7777
# False
# False


