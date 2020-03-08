# -*- coding: utf-8 -*-

# (цикл for)
import simple_draw
import random
import pygame


BRICK_WIDTH = 100
BRICK_HEIGHT = 50
rainbow_colors = [simple_draw.COLOR_RED, simple_draw.COLOR_ORANGE, simple_draw.COLOR_YELLOW, simple_draw.COLOR_GREEN,
                  simple_draw.COLOR_CYAN, simple_draw.COLOR_BLUE, simple_draw.COLOR_PURPLE]


def draw_brick(x, y, width=100, height=50, border_width=1,
               color=simple_draw.COLOR_DARK_RED, border_color=simple_draw.COLOR_BLACK):
    """Draws a brick

    Parameters
    ----------
    x, y : int
        Bottom left point of brick

    width : int, default=100
        Width of brick

    height : int, default=50
        Height of brick

    border_width : int, default=1
        Width of brick border

    color, border_color : tuple(int, int, int), default=(255, 255, 0)
        Color of brick and color of brick border respectively. Accepts tuple(red, green, blue),
        where color value between 0 and 255, including both of them

    """
    left_bottom = simple_draw.get_point(x, y)
    right_top = simple_draw.get_point(x + width, y + height)
    simple_draw.rectangle(left_bottom, right_top, color=color, width=0)
    simple_draw.rectangle(left_bottom, right_top, color=border_color, width=border_width)


def draw_brick_line(x, y, line_width, brick_width=100, brick_height=50):
    """Draws line of bricks

    Parameters
    ----------


    x, y : int
        Bottom left point of first brick

    line_width : int
        Width of bricks line in pixels

    brick_width : int, default=100
        Width of brick

    brick_height : int, default=50
        Height of brick

    """
    last_x = x
    for x in range(x, x + line_width, brick_width):
        draw_brick(x, y, brick_width, brick_height)
        last_x = x
    return last_x


def draw_wall(x, y, wall_width=100, wall_height=100, brick_width=100, brick_height=50):
    """Отрисовка стены с заданными параметрами

    Parameters
    ----------
    x, y: int
        Координаты левого нижнего угла стены

    wall_width, wall_height: int, default=100
        Ширина и высота стены. Обратите внимание, что стена будет выше и шире указанных параметров,
        поскольку должна быть кратной размерам кирпичей

    brick_width, brick_height: int, default=100, 50
        Ширина и высота кирпича соответственно

    Returns
    -------
    Возвращает вертикальную координату последнего (верхнего) ряда кирпичей
    """
    last_brick_y = y
    for number, brick_line_y in enumerate(range(y, y + wall_height, brick_height)):
        last_brick_y = brick_line_y
        last_brick_x = draw_brick_line(x=x if number % 2 else x + brick_width // 2,
                                       y=brick_line_y,
                                       line_width=wall_width if number % 2 else wall_width - brick_width,
                                       brick_width=brick_width,
                                       brick_height=brick_height)

        # здесь дорисовываем по полкирпича в начале и конце смещённой строки
        if not (number % 2):
            draw_brick(x=x, y=brick_line_y, height=brick_height, width=brick_width // 2)
            draw_brick(
                x=last_brick_x + brick_width,
                y=brick_line_y,
                height=brick_height,
                width=brick_width // 2
            )
    return last_brick_y


def _draw_roof(center_x, y, width, height, color=simple_draw.COLOR_YELLOW):
    """Отрисовка треугольной крыши дома

    Parameters
    ----------
    center_x, y: int
        Центральная нижняя точка крыши (середина основания треугольника)

    width: int
        Ширина крыши

    height: int
        Высота крыши

    color: tuple(int, int, int), default=(255, 255, 0)
        Цвет крыши. Это кортеж (red, green, blue),
        где для каждый из трёх элементов цвета принимает значения от 0 до 255 включительно

    """
    points = [
        simple_draw.get_point(center_x - width // 2, y),
        simple_draw.get_point(center_x + width // 2, y),
        simple_draw.get_point(center_x, y + height),
    ]
    simple_draw.polygon(points, color=color, width=0)


def draw_house(x=100, y=0, wall_width=500, wall_height=400,
               roof_width=600, roof_height=200, brick_width=80, brick_height=40):
    """Рисует кирпичный дом с окном и дымоходом

    Parameters
    ----------
    x, y: int, default=100, 0
        Координаты левого нижнего угла стены. Обратите внимание, что левый скат крыши может заходить левее

    wall_width, wall_height: int, default=500, 400
        Ширина и высота стены. Обратите внимание, что стена будет выше и шире указанных параметров,
        поскольку должна быть кратной размерам кирпичей

    roof_width, roof_height: int, default=600, 200
        Ширина и высота крыши

    brick_width, brick_height: int, default=80, 40
        Ширина и высота кирпича

    Returns
    -------
    Возвращает кортеж из двух координат середины верхней части дымохода
    """

    last_brick_y = draw_wall(
        x, y,
        wall_width=wall_width, wall_height=wall_height,
        brick_width=brick_width, brick_height=brick_height
    )
    # рисуем окно по центру стены
    window_width = 3 * brick_width
    window_height = 6 * brick_height
    draw_brick(
        x=x + (wall_width // brick_width + 1) * brick_width // 2 - window_width // 2,
        y= (last_brick_y - y + brick_height) // 2 - window_height // 2,
        width=window_width,
        height=window_height,
        color=simple_draw.COLOR_BLUE,
        border_color=simple_draw.COLOR_BLACK,
        border_width=4
    )
    #  рисуем дымоход
    draw_brick(
        x=x + wall_width - brick_width,
        y=last_brick_y + brick_height,
        width=brick_width,
        height=brick_height * 4,
        color=simple_draw.COLOR_DARK_RED,
        border_color=simple_draw.COLOR_BLACK,
        border_width=4
    )
    #  рисуем треугольник крыши
    _draw_roof(
        center_x=x + (wall_width // brick_width + 1) * brick_width // 2,
        y=last_brick_y + brick_height,
        width=roof_width, height=roof_height
    )
    chimney_top = (
        x + wall_width - brick_width + brick_width // 2,
        y + wall_height + brick_height * 4
    )
    return chimney_top


def _draw_branches(start_point, angle, length, color=simple_draw.COLOR_BLUE):
    """Рекурсивно рисует бинарное дерево с рандомизованными отклонениями

    Parameters
    ----------
    start_point: simple_draw.Point
        Точка, из которой начинается построение дерева

    angle: int
        Угол поворота дерева

    length: int
        Начальная длина ветвей

    color: tuple(int, int, int), default=(0, 0, 255)
        Начальный цвет ветвей. Это кортеж (red, green, blue),
        где для каждый из трёх элементов цвета принимает значения от 0 до 255 включительно

    """
    if length < random.randint(5, 10):
        return
    angle_shift = random.uniform(0.6, 1.4)
    branch1 = simple_draw.get_vector(start_point=start_point, angle=angle + 30 * angle_shift, length=length)
    branch1.draw(color)
    angle_shift = random.uniform(0.6, 1.4)
    branch2 = simple_draw.get_vector(start_point=start_point, angle=angle - 30 * angle_shift, length=length)
    branch2.draw(color)

    next_color = []
    for byte in color:
        byte += random.randint(0, 25)
        next_color.append(255 if byte > 255 else byte)
    next_color = tuple(next_color)

    next_length = length * .75 * random.uniform(0.8, 1.2)
    _draw_branches(start_point=branch1.end_point, angle=branch1.angle, length=next_length, color=next_color)
    next_length = length * .75 * random.uniform(0.8, 1.2)
    _draw_branches(start_point=branch2.end_point, angle=branch2.angle, length=next_length, color=next_color)


def draw_tree(x=0, trunk_length=100, init_branch_length=100, color=simple_draw.COLOR_BLUE):
    """Рекурсивно риует дерево: ствол и рандомизованные ветви

    Parameters
    ----------

    x: int, default=0
        Горизонтальная координата, из которой будет расти дерево.
        вертикальная не нужна, ибо она очевидно равна нулю.

    trunk_length: int, default=100
        Длина ствола

    init_branch_length: int, default=100
        Начальная длина веток

    color: tuple(int, int, int), default=(0, 0, 255)
        Цвет ствола и начальный цвет веток. Это кортеж (red, green, blue),
        где для каждый из трёх элементов цвета принимает значения от 0 до 255 включительно
    """
    pass
    root_point = simple_draw.get_point(x, 0)
    init_branches_point = simple_draw.vector(
        start=root_point, angle=90, width=2,
        length=trunk_length, color=color
    )
    _draw_branches(start_point=init_branches_point, angle=90, length=init_branch_length, color=color)


def draw_smile(x, y, color=simple_draw.COLOR_YELLOW, scale=1):
    """Рисует смайл хоттабыча в соответствии с параметрами

    Parameters
    ----------
    x, y: int
        Координаты правого нижнего угла смайла

    color: tuple(int, int, int), default=(255, 255, 0)
        Цвет смайла. Это кортеж (red, green, blue),
        где для каждый из трёх элементов цвета принимает значения от 0 до 255 включительно

    scale: int, default=1
        Масштаб (размер пикселя) смайла

    """
    _draw_head(x, y + 13 * scale, scale, color)
    _draw_eyes(x + 4 * scale, y + 22 * scale, scale)
    _draw_beard(x, y, scale)
    _draw_mouth(x, y + 13 * scale, scale)


def _draw_head(x, y, scale=1, color=simple_draw.COLOR_YELLOW):
    """Рисует голову смайла

    Parameters
    ----------
    x, y: int
        Координаты правого нижнего угла головы

    scale: int, default=1
        Масштаб (размер пикселя) смайла

    color: tuple(int, int, int), default=(255, 255, 0)
        Цвет смайла. Это кортеж (red, green, blue),
        где для каждый из трёх элементов цвета принимает значения от 0 до 255 включительно

    """
    for i in range(5):
        left_bottom_x = x + i * scale
        left_bottom_y = y + (5 - i) * scale
        left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

        right_top_x = x + (16 - i) * scale
        right_top_y = y + (13 + i) * scale
        right_top = simple_draw.get_point(right_top_x, right_top_y)

        simple_draw.rectangle(left_bottom, right_top, color, 0)


def _draw_mouth(x, y, scale=1):
    """Рисует рот смайла

    Parameters
    ----------
    x, y: int
        Координаты правого нижнего угла рта

    scale: int, default=1
        Масштаб (размер пикселя) смайла

    """
    # Outline
    left_bottom_x = x + scale
    left_bottom_y = y + 4 * scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = x + 15 * scale
    right_top_y = y + 8 * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    for i in range(1, 5):
        left_bottom_x = x + (1 + i) * scale
        left_bottom_y = y + (4 - i) * scale
        left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

        right_top_x = x + (15 - i) * scale
        right_top_y = y + (5 - i) * scale
        right_top = simple_draw.get_point(right_top_x, right_top_y)

        simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    # Background
    left_bottom_x = x + 2 * scale
    left_bottom_y = y + 4 * scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = x + 14 * scale
    right_top_y = y + 7 * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_WHITE, 0)

    for i in range(1, 4):
        left_bottom_x = x + (i + 2) * scale
        left_bottom_y = y + (4 - i) * scale
        left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

        right_top_x = x + (14 - i) * scale
        right_top_y = y + (5 - i) * scale
        right_top = simple_draw.get_point(right_top_x, right_top_y)

        simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_WHITE, 0)

    # Teeth
    left_bottom_x = x + 5 * scale
    left_bottom_y = y
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = x + 6 * scale
    right_top_y = y + 7 * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    left_bottom_x = x + 10 * scale
    left_bottom_y = y
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = x + 11 * scale
    right_top_y = y + 7 * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)


def _draw_eyes(x, y, scale=1):
    """Рисует глаза смайла

        Parameters
        ----------
        x, y: int
            Координаты правого нижнего угла левого глаза

        scale: int, default=1
            Масштаб (размер пикселя) смайла

        """
    # Left eye
    for i in range(2):
        left_bottom_x = x + i * scale
        left_bottom_y = y
        left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

        right_top_x = x + 3 * scale
        right_top_y = y + (3 + i) * scale
        right_top = simple_draw.get_point(right_top_x, right_top_y)

        simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_WHITE, 0)

    # Left pupil
    left_bottom_x = x + scale
    left_bottom_y = y + scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = x + 3 * scale
    right_top_y = y + 3 * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    # Right eye
    for i in range(2):
        left_bottom_x = x + 4 * scale
        left_bottom_y = y
        left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

        right_top_x = x + (6 + i) * scale
        right_top_y = y + (4 - i) * scale
        right_top = simple_draw.get_point(right_top_x, right_top_y)

        simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_WHITE, 0)

    # Right pupil
    left_bottom_x = x + 4 * scale
    left_bottom_y = y + scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = x + 6 * scale
    right_top_y = y + 3 * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    # Left eyebrow
    left_bottom_x = x
    left_bottom_y = y + 4 * scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = x + 3 * scale
    right_top_y = y + 5 * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    # Right eyebrow
    left_bottom_x = x + 5 * scale
    left_bottom_y = y + 5 * scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = x + 7 * scale
    right_top_y = y + 6 * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)

    left_bottom_x = x + 7 * scale
    left_bottom_y = y + 4 * scale
    left_bottom = simple_draw.get_point(left_bottom_x, left_bottom_y)

    right_top_x = x + 8 * scale
    right_top_y = y + 5 * scale
    right_top = simple_draw.get_point(right_top_x, right_top_y)

    simple_draw.rectangle(left_bottom, right_top, simple_draw.COLOR_BLACK, 0)


def _draw_vertical_rectangle(x, y_top, y_bottom, color=simple_draw.COLOR_YELLOW, scale=1):
    """Рисует вертикальный прямоугольник в соответствии с параметрами

    Parameters
    ----------
    x: int
        Горизонтальная координата правого нижнего угла прямоугольника

    y_top, y_bottom: int
        Вертикальные координаты верха и низа прямоугольника

    color: tuple(int, int, int), default=(255, 255, 0)
        Цвет смайла. Это кортеж (red, green, blue),
        где для каждый из трёх элементов цвета принимает значения от 0 до 255 включительно

    scale: int, default=1
        Масштаб (размер пикселя) смайла

    """
    left_bottom = simple_draw.get_point(x, y_bottom)
    right_top = simple_draw.get_point(x + scale, y_top)
    simple_draw.rectangle(left_bottom, right_top, color, 0)


def _draw_beard(x, y, scale=1):
    """Рисует бороду смайла

        Parameters
        ----------
        x, y: int
            Координаты правого нижнего угла бороды

        scale: int, default=1
            Масштаб (размер пикселя) смайла

        """
    beard = [5, 7, 8, 12, 16, 15, 18, 20, 19, 17, 14, 13, 10, 8, 7, 4]
    hair_y_top = y + 20 * scale
    for i, hair in enumerate(beard):
        hair_x = x + i * scale
        hair_y_bottom = hair_y_top - hair * scale
        _draw_vertical_rectangle(hair_x, hair_y_top, hair_y_bottom, simple_draw.COLOR_WHITE, scale)


def shift_list(input_list, steps):
    """Циклически смещает список на указанное количество элементов

    Parameters
    ----------
    input_list: list
        Целевой список

    steps: int
        Количество шагов, на которое смещается список

    Returns
    -------
    Смещённый список
    """
    return input_list[steps:] + input_list[:steps]


def draw_rainbow(colors, center_x=0, center_y=-700):
    """Рисует радугу

    Parameters
    ----------
    colors: list
        Список цветов

    center_x, center_y: int, default=0, -700
        Координаты исходной точки, из которой рисуются окружности, образующие радугу

    """
    circles_center = simple_draw.get_point(center_x, center_y)
    radius = 1200
    line_width = 40
    for color in colors:
        simple_draw.circle(circles_center, radius, color, width=line_width)
        radius += line_width


def draw_sun(center_x=0, center_y=0, angle=0, ray_length=100, core_radius=50, ray_gap=10, ray_count=8, ray_width=3):
    """Рисует солнце в соответствии с параметрами

    Parameters
    ----------
    center_x, center_y: int, default=0, 0
        Координаты центра солнца

    angle: int, default=0
        Угол поворота лучей солнца

    ray_length: int, default=100
        Длина лучей

    core_radius: int, default=50
        Радиус внутренней части

    ray_gap: int, default=10
        Расстояние между ядром и лучами

    ray_count: int, default=8
        Количество лучей

    ray_width: int, default=3
        Толщина лучей

    """
    origin = simple_draw.get_point(center_x, center_y)
    angle_step = round(360 / ray_count)
    for next_angle in range(angle, 360 + angle, angle_step):
        ray_start_point = simple_draw.get_vector(origin, next_angle, length=core_radius + ray_gap).end_point
        simple_draw.vector(start=ray_start_point, angle=next_angle, length=ray_length, width=ray_width)
    simple_draw.circle(origin, core_radius, width=0)


def set_new_destination(submarine, h_resolution, v_resolution, image_width, image_height):
    """Задаёт новую точку назначения субмарины и пересчитывает вертикальную и горизонтальную скорости

    Parameters
    ----------
    submarine: dict
        Список основных параметров субмарины. См. generate_submarine

    h_resolution, v_resolution: int
        Горизонтальный и вертикальный размер окна. Нужны для того, чтобы спрайт не убежал за край экрана

    image_width, image_height: int
        Горизонтальный и вертикальный размер спрайта. Нужны для того, чтобы спрайт не убежал за край экрана

    """
    # создаём новую точку назначения
    submarine['destination_x'] = random.randint(0, h_resolution - image_width)
    submarine['destination_y'] = random.randint(0, v_resolution - image_height)

    # находим путь - гипотенузу треугольника
    path = ((submarine['x'] - submarine['destination_x']) ** 2 +
            (submarine['y'] - submarine['destination_y']) ** 2) ** 0.5

    # теперь найдём количество шагов (время), за которое преодолеем данный путь (проверить округление вверх)
    steps = path / submarine['speed']

    # а теперь найдём вертикальную и горизонтальную скорость
    submarine['h_speed'] = -(submarine['x'] - submarine['destination_x']) / steps
    submarine['v_speed'] = -(submarine['y'] - submarine['destination_y']) / steps


def generate_submarine(x, y, h_resolution, v_resolution, image_width, image_height):
    """Создаёт рандомизированную субмарину

    Parameters
    ----------
    x, y: int
            Координаты правого нижнего угла спрайта

    h_resolution, v_resolution: int
        Горизонтальный и вертикальный размер окна. Нужны для того, чтобы спрайт не убежал за край экрана

    image_width, image_height: int
        Горизонтальный и вертикальный размер спрайта. Нужны для того, чтобы спрайт не убежал за край экрана

    Returns
    -------
    Словарь параметров субмарины
    """
    submarine = {'x': x, 'y': y, 'speed': 10}
    set_new_destination(submarine, h_resolution, v_resolution, image_width, image_height)
    return submarine


def scale_sprite(sprite, scale):
    """Масштабирование спрайта

    Parameters
    ----------
    sprite: pygame.image
        Целевой спрайт

    scale: float
        Желаемый масштаб

    Returns
    -------
    Отмасштабированный спрайт
    """
    return pygame.transform.scale(sprite, (round(sprite.get_width() * scale), round(sprite.get_height() * scale)))


def draw_sprite(screen, sprite, x, y, h_speed=1):
    """Отрисовывает спрайт с отражением по горизонтали в необходимую сторону

    Parameters
    ----------
    screen: pygame.display
        Экран, на который будет выводиться спрайт

    sprite: pygame.image
        Целевой спрайт

    x, y: int
            Координаты правого нижнего угла спрайта


    h_speed: int, default=1
        Направление отражения спрайта

    Returns
    -------

    """
    sprite = pygame.transform.flip(sprite, 1 if h_speed < 0 else 0, 0)
    screen.blit(
        sprite, (int(x), screen.get_height() - int(y) - sprite.get_height())
    )


if __name__ == "__main__":
    simple_draw.resolution = (1300, 900)
    simple_draw.start_drawing()
    draw_house(x=100, y=0, wall_width=370, wall_height=350,
               roof_width=450, roof_height=100, brick_width=60, brick_height=30)

    draw_tree(x=600, trunk_length=150, init_branch_length=100)
    simple_draw.finish_drawing()
    simple_draw.pause()


