# -*- coding: utf-8 -*-

# Создать пакет, в который скопировать функции отрисовки из предыдущего урока
#  - радуги
#  - стены
#  - дерева
#  - смайлика
#  - снежинок
# Функции по модулям разместить по тематике. Название пакета и модулей - по смыслу.
# Создать модуль с функцией отрисовки кирпичного дома с широким окном и крышей.

# С помощью созданного пакета нарисовать эпохальное полотно "Утро в деревне".
# На картине должны быть:
#  - кирпичный дом, в окошке - смайлик.
#  - слева от дома - сугроб (предположим что это ранняя весна)
#  - справа от дома - дерево (можно несколько)
#  - справа в небе - радуга, слева - солнце (весна же!)
# пример см. lesson_005/results/04_painting.jpg
# Приправить своей фантазией по вкусу (коты? коровы? люди? трактор? что придумается)

import pygame
import simple_draw as sd
import cliparts.decorations as decorations
import cliparts.particle_generator as pg

# TODO Этот модуль должен состоять из вызовов функций импортированных из модулей отрисовки частей картины и главного
#  цикла анимации. Все переменные необходимые для отрисовки частей картины должны находится в соответствующих модулях.
#  Для инициализации переменных создайте функции init(). Статические части должны рисоваться вызовом функции draw(),
#  анимированные - draw_step()

pygame.init()
sd.resolution = (1300, 900)
screen = pygame.display.set_mode(sd.resolution)

# Сделаем интро-экран. Чтоб как у взрослых)
intro_sprite = pygame.image.load('resources/splash.jpg')
sd.start_drawing()
decorations.draw_sprite(screen=screen, sprite=intro_sprite,
                        x=sd.resolution[0] // 2 - intro_sprite.get_width() // 2,
                        y=sd.resolution[1] // 2 - intro_sprite.get_height() // 2)
sd.finish_drawing()
sd.sleep(2)


# генерируем фон, чтобы потом не тратить на него ресурсы
sd.start_drawing()
sd.clear_screen()
smoke_origin = decorations.draw_house(x=100, y=0, wall_width=370, wall_height=350,
                                      roof_width=450, roof_height=100, brick_width=60, brick_height=30)
decorations.draw_smile(x=270, y=100, scale=5)
decorations.draw_tree(x=650, trunk_length=150, init_branch_length=100)
sd.finish_drawing()
sd.take_background()

# счётчик нужен для процессов, которые происходят не каждую итерацию цикла
steps_from_start = 1

# подтягиваем цвета радуги. создаём новую переменную, потому что порядок цветов будет изменяться
rainbow_colors = decorations.rainbow_colors

# создаём первое облачко дыма
house_smoke_scale = 1.5
smoke = [pg.generate_cloud(*smoke_origin, scale=house_smoke_scale), ]

# немного смещаем вверх точку генерации дыма, чтобы было красивее
smoke_origin = (smoke_origin[0], smoke_origin[1] + 30)

# генерим первоначальный список снежинок
blizzard = []
for _ in range(20):
    blizzard.append(pg.generate_snowflake())

# инициализируем параметры для анимирования солнца
sun_angle = 0
sun_radius = 160
sun_core_radius = 50
sun_size_direction = 1

# запускаем шарманку
pygame.mixer.music.load("resources/music.mid")
pygame.mixer.music.play(-1)

# инициализируем спрайт и связанные с ним переменные
reference_sprite = pygame.image.load('resources/image.png')
sprite_scale = 0.3
sprite = decorations.scale_sprite(reference_sprite, sprite_scale)
submarine = decorations.generate_submarine(200, 200, *sd.resolution, sprite.get_width(), sprite.get_height())



while True:  # TODO Больше двух пустых строк не допускает РЕР8
    sd.start_drawing()
    sd.draw_background()
    # ----- рисуем радугу -----
    decorations.draw_rainbow(colors=rainbow_colors, center_x=150, center_y=-250)
    if steps_from_start % 4 == 0:
        rainbow_colors = decorations.shift_list(rainbow_colors, 1)

    # ----- рисуем солнце -----
    decorations.draw_sun(center_x=200, center_y=700,
                         angle=sun_angle, core_radius=sun_core_radius,
                         ray_length=sun_radius - sun_core_radius - 10)
    sun_angle = (sun_angle - 2) % 360
    if sun_core_radius >= 100:
        sun_size_direction = -1
    elif sun_core_radius <= 50:
        sun_size_direction = 1
    sun_core_radius += 2 * sun_size_direction

    # ----- рисуем дым -----
    smoke = pg.draw_smoke(smoke)

    for i, cloud in enumerate(smoke):
        if cloud['y'] > sd.resolution[1] + max(cloud['radii']) * 2:
            del smoke[i]

    if (steps_from_start + 2) % 4 == 0:
        smoke.append(pg.generate_cloud(*smoke_origin, scale=house_smoke_scale))
        smoke.append(pg.generate_cloud(submarine['x']+sprite.get_width()//2, submarine['y'] + sprite.get_height()))

    # ----- рисуем субмарину -----
    sprite = decorations.scale_sprite(reference_sprite, sprite_scale)
    decorations.draw_sprite(screen=screen, sprite=sprite, x=submarine['x'], y=submarine['y'],
                            h_speed=submarine['h_speed'])

    submarine['x'] += submarine['h_speed']
    submarine['y'] += submarine['v_speed']

    # проверяем достижение нужной точки
    if abs(submarine['x'] - submarine['destination_x']) < abs(submarine['h_speed']):
        decorations.set_new_destination(submarine, *sd.resolution, sprite.get_width(), sprite.get_height())

    # ----- рисуем снегопад -----
    blizzard = pg.draw_blizzard(blizzard)

    for i, snowflake in enumerate(blizzard):
        if snowflake['y'] < 0 - snowflake['length']:
            del blizzard[i]
            blizzard.append(pg.generate_snowflake())

    sd.finish_drawing()

    steps_from_start += 1

    sd.sleep(0.042)
    if sd.user_want_exit():
        break

sd.pause()
# Усложненное задание (делать по желанию)
# Анимировать картину.
# Пусть слева идет снегопад, радуга переливается цветами, смайлик моргает, солнце крутит лучами, етс.
# Задержку в анимировании все равно надо ставить, пусть даже 0.01 сек - так библиотека устойчивей работает.
