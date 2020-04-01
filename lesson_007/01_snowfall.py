# -*- coding: utf-8 -*-
import random

import simple_draw as sd


# Шаг 1: Реализовать падение снежинки через класс. Внести в методы:
#  - создание снежинки с нужными параметрами
#  - отработку изменений координат
#  - отрисовку


class Snowflake:
    #  1) Если это константы класса, то они должны быть большими буквами.
    #  2) Знаете отличие атрибутов класса от атрибутов объекта? Таким образом объявляются атрибуты класса (доступ к
    #  которым должен быть через имя класса), но ниже по коду вы к ним обращаетесь как атрибутам объекта (через self).
    #  Предлагаю просто сделать их глобальными константами

    # Да, это должны были быть атрибуты класса. Но поскольку они используются только во время генерации снежинки
    #  и я хотел бы оставить возможность изменять эти параметры,
    #  то добавлю эти переменные как необязательные аргументы __init__

    def __init__(self, min_length=5, max_length=40):
        def remap_range(value, in_min, in_max, out_min, out_max):
            """Функция пропорционально переносит значение (value) из текущего диапазона значений (in_min .. in_max)
                    в новый диапазон (out_min .. out_max), заданный параметрами.
                    Конкретно здесь используется для создания эффекта параллакса

            """
            return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

        self.x = random.randint(-max_length * 2, sd.resolution[0])
        self.y = sd.resolution[1] + max_length
        self.length = random.randint(min_length, max_length)
        self.factor_a = round(random.uniform(0.2, 1), 2)
        self.factor_b = round(random.uniform(0.1, 1), 2)
        self.factor_c = round(random.randint(20, 90), 2)
        self.h_speed = round(remap_range(value=self.length * random.uniform(0.7, 1),
                                         in_min=min_length, in_max=max_length, out_min=0, out_max=15))
        self.v_speed = round(remap_range(value=self.length, in_min=min_length,
                                         in_max=max_length, out_min=2, out_max=30))
        color_byte = round(remap_range(value=self.length, in_min=min_length,
                                       in_max=max_length, out_min=64, out_max=255))
        self.color = (color_byte, color_byte, color_byte)

    def move(self):
        self.h_speed = -self.h_speed if random.randint(0, 100) < 2 else self.h_speed
        self.x += self.h_speed
        self.y -= self.v_speed

    def draw(self, color=None):
        if color is None:
            color = self.color

        point = sd.get_point(self.x, self.y)
        sd.snowflake(
            center=point,
            length=self.length,
            factor_a=self.factor_a,
            factor_b=self.factor_b,
            factor_c=self.factor_c,
            color=color,
        )

    def can_fall(self):
        return (self.y >= -self.length * 2 and
                -self.length * 2 <= self.x <= sd.resolution[0] + self.length * 2)

    def clear_previous_picture(self):
        self.draw(color=sd.background_color)


def get_flakes(count):
    return [Snowflake() for _ in range(count)]


def delete_flakes(flakes_list, numbers_list):
    # C этого модуля избегаем глобальных переменных - передавайте их через параметры функций
    #  Принял. В принципе, изначально и хотел так поступить,
    #  но после снегопада в шестом модуле решил перестраховаться

    # возвращает список упавших функция "get_fallen_flakes", а удаляет delete_fallen_flakes
    #  Глядя на функцию vector из simple_draw, которая и рисовала вектор и возвращала конечную точку я посчитал,
    #  что подобное поведение функции допустимо. Исправляю

    # Не вполне соответствующий пример. Если бы vector кроме рисования ещё в другом месте стирала или писала в
    #  файл, вот тогда - да, плохо :)
    for number in sorted(numbers_list, reverse=True):
        del flakes_list[number]


def get_offscreen_flakes(flakes_list):
    return [number for number, flake in enumerate(flakes_list) if not flake.can_fall()]


# flake = Snowflake()
#
# while True:
#     flake.clear_previous_picture()
#     flake.move()
#     flake.draw()
#     if not flake.can_fall():
#         break
#     sd.sleep(0.1)
#     if sd.user_want_exit():
#         break

# шаг 2: создать снегопад - список объектов Снежинка в отдельном списке, обработку примерно так:
flakes = get_flakes(count=20)  # создать список снежинок
while True:
    sd.start_drawing()
    # TODO Для того, чтобы избавиться от синих артефактов при наложении снежинок, вынес отрисовку синих в отдельный цикл
    for flake in flakes:
        flake.clear_previous_picture()

    for flake in flakes:
        flake.move()
        flake.draw()
    sd.finish_drawing()
    #  С улетевшими за экран снежинками ничего не происходит, а список объектов будет расти и всё будет тормозить.
    #  Поэтому, мне кажется, что тут вместо get_fallen_flakes() подошла бы процедура delete_fallen_flakes(),
    #  которая будет подчищать улетевшие за экран снежинки и возвращать их количество

    # Всё верно, только не "вместо", а в дополнение. Функции должны выполнять строго по одному "делу", одна
    #  считает (точнее отдаёт список упавших), другая удаляет. Так проще понять код, проще комбинировать из таких
    #  "кирпичиков" новый функционал, и проще тестировать.

    #  Готово
    fallen_flakes_numbers = get_offscreen_flakes(flakes)
    if fallen_flakes_numbers:
        delete_flakes(flakes, fallen_flakes_numbers)
        flakes.extend(get_flakes(len(fallen_flakes_numbers)))
        # Тут тоже можно обойтись без функции завязанной на глобальную переменную: добавить снежинок
        #  непосредственно во flakes c помощью get_flakes и extend

        # TODO В принципе да, просто я пытался вписать код в изначально предложенный "скелет" программы. Исправил)

    sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()
