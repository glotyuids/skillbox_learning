# -*- coding: utf-8 -*-

import simple_draw as sd
import random


# На основе кода из практической части реализовать снегопад:
# - создать списки данных для отрисовки N снежинок
# - нарисовать падение этих N снежинок
# - создать список рандомных длинн лучей снежинок (от 10 до 100) и пусть все снежинки будут разные

N = 20
MAX_LENGTH = 40
MIN_LENGTH = 5

# Пригодятся функции
# sd.get_point()
# sd.snowflake()
# sd.sleep()
# sd.random_number()
# sd.user_want_exit()


def remap_range(value, in_min, in_max, out_min, out_max):
    """Функция пропорционально переносит значение (value) из текущего диапазона значений (in_min .. in_max)
            в новый диапазон (out_min .. out_max), заданный параметрами.
            Конкретно здесь используется для создания эффекта параллакса

    """
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
# Вах! Тут челюсть моя немного отпала! :) Это очень оригинально и интересно!!
#  Эта функция есть в стандартной библиотеке arduino. Очень удобная штука, которой в питоне мне очень не хватало)


def generate_snowflake():
    sf_length = random.randint(MIN_LENGTH, MAX_LENGTH)
    h_speed = round(remap_range(value=sf_length * random.uniform(0.7, 1),
                                in_min=MIN_LENGTH, in_max=MAX_LENGTH, out_min=0, out_max=15))
    color_byte = round(remap_range(value=sf_length, in_min=MIN_LENGTH, in_max=MAX_LENGTH, out_min=64, out_max=255))
    return {
            'x': random.randint(-MAX_LENGTH * 2, sd.resolution[0]),
            'y': sd.resolution[1] + MAX_LENGTH,
            'length': sf_length,
            'factor_a': round(random.uniform(0.2, 1), 2),
            'factor_b': round(random.uniform(0.1, 1), 2),
            'factor_c': round(random.randint(20, 90), 2),
            'h_speed': h_speed,
            'v_speed': round(remap_range(value=sf_length, in_min=MIN_LENGTH, in_max=MAX_LENGTH, out_min=2, out_max=30)),
            'color': (color_byte, color_byte, color_byte)
        }


# генерим первоначальный список снежинок
blizzard = []
for _ in range(N):
    blizzard.append(generate_snowflake())

sd.resolution = (1200, 600)
while True:
    sd.start_drawing()

    # проверяем положение снежинки. Если приземлилась, то удаляем её из списка и генерируем новую
    for i, snowflake in enumerate(blizzard):
        if snowflake['y'] < snowflake['length']:
            del blizzard[i]
            blizzard.append(generate_snowflake())
            continue

        # рисуем снежинку фоновым цветом, чтобы закрыть нарисованную в предыдущем шаге
        point = sd.get_point(snowflake['x'], snowflake['y'])
        sd.snowflake(
            center=point,
            length=snowflake['length'],
            factor_a=snowflake['factor_a'],
            factor_b=snowflake['factor_b'],
            factor_c=snowflake['factor_c'],
            color=sd.background_color
        )

        snowflake['h_speed'] = -snowflake['h_speed'] if random.randint(0, 100) < 2 else snowflake['h_speed']
        snowflake['x'] += snowflake['h_speed']
        snowflake['y'] -= snowflake['v_speed']
        point = sd.get_point(snowflake['x'], snowflake['y'])
        sd.snowflake(
            center=point,
            length=snowflake['length'],
            factor_a=snowflake['factor_a'],
            factor_b=snowflake['factor_b'],
            factor_c=snowflake['factor_c'],
            color=snowflake['color'],
        )

    sd.finish_drawing()
    sd.sleep(0.042)
    if sd.user_want_exit():
        break

sd.pause()

# подсказка! для ускорения отрисовки можно
#  - убрать clear_screen()
#  - в начале рисования всех снежинок вызвать sd.start_drawing()
#  - на старом месте снежинки отрисовать её же, но цветом sd.background_color
#  - сдвинуть снежинку
#  - отрисовать её цветом sd.COLOR_WHITE на новом месте
#  - после отрисовки всех снежинок, перед sleep(), вызвать sd.finish_drawing()


# 4) Усложненное задание (делать по желанию)
# - сделать рандомные отклонения вправо/влево при каждом шаге
# - сделать сугоб внизу экрана - если снежинка долетает до низа, оставлять её там,
#   и добавлять новую снежинку
# Результат решения см https://youtu.be/XBx0JtxHiLg

# зачет!
