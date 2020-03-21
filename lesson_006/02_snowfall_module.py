# -*- coding: utf-8 -*-

import simple_draw as sd
import snowfall

# На основе кода из lesson_004/05_snowfall.py
# сделать модуль snowfall.py в котором реализовать следующие функции
#  создать_снежинки(N) - создает N снежинок
#  нарисовать_снежинки_цветом(color) - отрисовывает все снежинки цветом color
#  сдвинуть_снежинки() - сдвигает снежинки на один шаг
#  номера_достигших_низа_экрана() - выдает список номеров снежинок, которые вышли за границу экрана
#  удалить_снежинки(номера) - удаляет снежинки с номерами из списка
#
# В текущем модуле реализовать главный цикл падения снежинок,
# обращаясь ТОЛЬКО к функциям модуля snowfall

N = 20
COLOR = sd.COLOR_WHITE

# создать_снежинки(N)
snowfall.generate_snowflakes(N)
while True:
    #  нарисовать_снежинки_цветом(color=sd.background_color)

    # TODO кстати, сугроб в четвёртом уроке без синих артефактов (от снежинок цвета фона) можно получить,
    #  если перед удалением упавших снежинок делать sd.draw_background, выводить только удаляемые снежинки
    #  и делать sd.take_background. Продемонстрировал концепт в самом модуле snowfall.
    #  Здесь же для ускорения работы можно обойтись однократным sd.take_background перед циклом
    #  и sd.draw_background в начале каждой итерации вместо рисования снежинок цветом фона
    snowfall.draw_snowflakes(sd.background_color)
    #  сдвинуть_снежинки()
    snowfall.move_snowflakes()
    #  нарисовать_снежинки_цветом(color)
    snowfall.draw_snowflakes(COLOR)
    #  если есть номера_достигших_низа_экрана() то
    offscreen_snowflakes = snowfall.get_offscreen_snowflakes()
    if offscreen_snowflakes:
        # удалить_снежинки(номера)
        snowfall.delete_offscreen_snowflakes(offscreen_snowflakes)
        # создать_снежинки(count)
        snowfall.generate_snowflakes(len(offscreen_snowflakes))
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()
