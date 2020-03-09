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

#  Этот модуль должен состоять из вызовов функций импортированных из модулей отрисовки частей картины и главного
#  цикла анимации. Все переменные необходимые для отрисовки частей картины должны находится в соответствующих модулях.
#  Для инициализации переменных создайте функции init(). Статические части должны рисоваться вызовом функции draw(),
#  анимированные - draw_step()

# TODO Надеюсь, на этот раз я правильно понял задачу

pygame.init()
sd.resolution = (1300, 900)
screen = pygame.display.set_mode(sd.resolution)

# Сделаем интро-экран. Чтоб как у взрослых)
decorations.draw_intro(screen=screen, image='resources/splash.jpg')
sd.sleep(2)

# генерируем фон, чтобы потом не тратить на него ресурсы
sd.start_drawing()
sd.clear_screen()
smoke_origin = decorations.draw_house()
decorations.draw_smile()
decorations.draw_tree()
sd.finish_drawing()
sd.take_background()

# счётчик нужен для процессов, которые происходят не каждую итерацию цикла
steps_from_start = 1

# создаём первое облачко дыма
smoke = pg.init_smoke(smoke_origin)

# генерим первоначальный список снежинок
blizzard = pg.blizzard_init()

# инициализируем солнце
sun = decorations.init_sun()

# инициализируем спрайт и подлодку
reference_sprite = pygame.image.load('resources/image.png')
submarine = decorations.init_submarine(screen=screen, sprite=reference_sprite)

# запускаем шарманку
pygame.mixer.music.load("resources/music.mid")
pygame.mixer.music.play(-1)

while True:
    sd.start_drawing()
    sd.draw_background()

    decorations.draw_rainbow_step(steps_from_start)
    decorations.draw_sun_step(sun)
    smoke = pg.draw_smoke_step(smoke, smoke_origin, submarine, steps_from_start)
    decorations.draw_sprite_step(reference_sprite, submarine, screen)
    blizzard = pg.draw_blizzard_step(blizzard)

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
