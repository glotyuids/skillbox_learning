# -*- coding: utf-8 -*-

import simple_draw as sd
import random

SNOWFLAKE_MAX_LENGTH = 40
SNOWFLAKE_MIN_LENGTH = 5

HOUSE_SMOKE_SCALE = 1.5


def remap_range(value, in_min, in_max, out_min, out_max):
    """Функция пропорционально переносит значение (value) из текущего диапазона значений (in_min .. in_max)
            в новый диапазон (out_min .. out_max), заданный параметрами.
            Конкретно здесь используется для создания эффекта параллакса

    """
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def generate_snowflake():
    """Функция генерирует новую рандомизованную снежинку.

    Returns
    -------
    Словарь с параметрами снежинки (см. описание snowflake в модуле simple_draw) и её скоростью
    """
    sf_length = random.randint(SNOWFLAKE_MIN_LENGTH, SNOWFLAKE_MAX_LENGTH)
    h_speed = round(remap_range(value=sf_length * random.uniform(0.7, 1),
                                in_min=SNOWFLAKE_MIN_LENGTH, in_max=SNOWFLAKE_MAX_LENGTH, out_min=0, out_max=15))
    color_byte = round(remap_range(value=sf_length, in_min=SNOWFLAKE_MIN_LENGTH,
                                   in_max=SNOWFLAKE_MAX_LENGTH, out_min=64, out_max=255))
    return {
        'x': random.randint(-SNOWFLAKE_MAX_LENGTH * 2, sd.resolution[0]),
        'y': sd.resolution[1] + SNOWFLAKE_MAX_LENGTH,
        'length': sf_length,
        'factor_a': round(random.uniform(0.2, 1), 2),
        'factor_b': round(random.uniform(0.1, 1), 2),
        'factor_c': round(random.randint(20, 90), 2),
        'h_speed': h_speed,
        'v_speed': round(remap_range(value=sf_length, in_min=SNOWFLAKE_MIN_LENGTH,
                                     in_max=SNOWFLAKE_MAX_LENGTH, out_min=2, out_max=30)),
        'color': (color_byte, color_byte, color_byte)
    }


def init_smoke(smoke_origin):
    # немного смещаем вверх точку генерации дыма, чтобы было красивее
    smoke_origin = (smoke_origin[0], smoke_origin[1] + 30)
    return [generate_cloud(*smoke_origin, scale=HOUSE_SMOKE_SCALE), ]


def generate_cloud(x, y, scale=1):
    """Функция генерирует рандомизованное облако из трёх кругов.

    Parameters
    ----------
    x, y: int
        координаты облака
    scale: float, default=1
        масштаб облака

    Returns
    -------
    Словарь с параметрами облака (см. описание draw_cloud) и его скоростью
    """
    color_bytes = [127, 192, 255]
    random.shuffle(color_bytes)
    sizes = [
        round(15 * scale),
        round(10 * scale),
        round(8 * scale)
    ]
    return {
        'x': x,
        'y': y,
        'radii': sizes,
        'factor_a': random.randint(-sizes[0] // 2, sizes[0] // 2),
        'factor_b': random.randint(-sizes[1] // 2, sizes[1] // 2),
        'factor_c': random.randint(-sizes[2] // 2, sizes[2] // 2),
        'factor_d': random.randint(-max(sizes) // 2, max(sizes) // 2),
        'color_bytes': color_bytes,
        'h_speed': random.randint(-1, 1),
        'v_speed': random.randint(4, 10)
    }


def draw_cloud(x, y, radii=[15, 10, 8], factor_a=5, factor_b=5, factor_c=5, factor_d=5, color_bytes=[127, 192, 255]):
    """Функция рисует облако в районе точки x, y с радиусами элементов radii
            серым цветом с яркостями color_bytes (255 - белый, 0 - чёрный)

    Parameters
    ----------
    x, y: int
        точка рисования облака
    radii: list[int, int, int ], default=[15, 10, 8]
        радиусы кругов облака
    factor_a: int, default=5
        смещение первого круга по горизонтали
    factor_b: int, default=5
        смещение второго круга по горизонтали
    factor_c: int, default=5
        смещение третьего круга по горизонтали
    factor_d: int, default=5
        расстояние между кругами по вертикали
    color_bytes: list[int, int, int ], default=[127, 192, 255]
        яркости первого, второго и третьего кругов соответственно

    """
    circle_y = y
    for radius, factor, color_byte in zip(radii, [factor_a, factor_b, factor_c], color_bytes):
        origin = sd.get_point(x + factor, circle_y)
        sd.circle(
            center_position=origin,
            radius=radius,
            color=(color_byte, color_byte, color_byte),
            width=0
        )
        circle_y += factor_d


def blizzard_init():
    blizzard = []
    for _ in range(20):
        blizzard.append(generate_snowflake())
    return blizzard


def draw_smoke(smoke):
    """Отрисовка дыма и изменение координат облачков в соответствии с параметрами

    Parameters
    ----------
    smoke: list
        Список облачков-словарей с параметрами этих облачков. См. докстринг к draw_cloud()

    Returns
    -------
    Список облачков с новыми параметрами
    """
    for cloud in smoke:
        draw_cloud(
            x=cloud['x'],
            y=cloud['y'],
            radii=cloud['radii'], color_bytes=cloud['color_bytes'],
            factor_a=cloud['factor_a'], factor_b=cloud['factor_b'],
            factor_c=cloud['factor_c'], factor_d=cloud['factor_d'],
        )
        cloud['h_speed'] = -cloud['h_speed'] if random.randint(0, 100) < 2 else cloud['h_speed']
        cloud['x'] += int(cloud['h_speed'])
        cloud['y'] += int(cloud['v_speed'])

    return smoke


def draw_smoke_step(smoke, smoke_origin, submarine, step):
    smoke = draw_smoke(smoke)

    for i, cloud in enumerate(smoke):
        if cloud['y'] > sd.resolution[1] + max(cloud['radii']) * 2:
            del smoke[i]

    if (step + 2) % 4 == 0:
        smoke.append(generate_cloud(*smoke_origin, scale=HOUSE_SMOKE_SCALE))
        smoke.append(generate_cloud(submarine['x'] + submarine['width'] // 2, submarine['y'] + submarine['height']))

    return smoke


def draw_blizzard(blizzard):
    """Функция отрисовывает снежинки и изменяет их координаты в соответствии с параметрами

    Parameters
    ----------
    blizzard: list
        список снежинок (см. generate_snowflake)

    Returns
    -------
    Возвращает изменённый список снежинок
    """
    for snowflake in blizzard:
        point = sd.get_point(snowflake['x'], snowflake['y'])
        sd.snowflake(
            center=point,
            length=snowflake['length'],
            factor_a=snowflake['factor_a'],
            factor_b=snowflake['factor_b'],
            factor_c=snowflake['factor_c'],
            color=snowflake['color'],
        )
        snowflake['h_speed'] = -snowflake['h_speed'] if random.randint(0, 100) < 2 else snowflake['h_speed']
        snowflake['x'] += snowflake['h_speed']
        snowflake['y'] -= snowflake['v_speed']

    return blizzard


def draw_blizzard_step(blizzard):
    blizzard = draw_blizzard(blizzard)

    for i, snowflake in enumerate(blizzard):
        if snowflake['y'] < 0 - snowflake['length']:
            del blizzard[i]
            blizzard.append(generate_snowflake())
    return blizzard


# тестовая демка
if __name__ == "__main__":
    # генерим первоначальный список снежинок
    blizzard = []
    for _ in range(20):
        blizzard.append(generate_snowflake())

    sd.resolution = (1200, 600)
    smoke = [generate_cloud(100, 100)]
    adding_step = 1
    sd.take_background()
    while True:
        sd.start_drawing()
        sd.draw_background()
        # метель
        blizzard = draw_blizzard(blizzard)

        # проверяем положение снежинки. Если приземлилась, то удаляем её из списка и генерируем новую
        for i, snowflake in enumerate(blizzard):
            if snowflake['y'] < 0 - snowflake['length']:
                del blizzard[i]
                blizzard.append(generate_snowflake())

        # дым
        smoke = draw_smoke(smoke)

        for i, cloud in enumerate(smoke):
            if cloud['y'] > sd.resolution[1] + max(cloud['radii']) * 2:
                del smoke[i]

        if adding_step % 4 == 0:
            smoke.append(generate_cloud(100, 100))
        adding_step += 1

        sd.finish_drawing()
        sd.sleep(0.042)
        if sd.user_want_exit():
            break

    sd.pause()
