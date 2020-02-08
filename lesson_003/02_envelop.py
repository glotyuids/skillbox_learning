# -*- coding: utf-8 -*-

# (if/elif/else)

# Заданы размеры envelop_x, envelop_y - размеры конверта и paper_x, paper_y листа бумаги
#
# Определить, поместится ли бумага в конверте (стороны листа параллельны сторонам конверта)
# Не забывайте, что лист бумаги можно перевернуть и попробовать вставить в конверт другой стороной.
# Результат проверки вывести на консоль (ДА/НЕТ)
# Использовать только операторы if/elif/else, можно вложенные

envelop_x, envelop_y = 10, 7
paper_x, paper_y = 8, 9
# проверить для
# paper_x, paper_y = 9, 8
# paper_x, paper_y = 6, 8
# paper_x, paper_y = 8, 6
# paper_x, paper_y = 3, 4
# paper_x, paper_y = 11, 9
# paper_x, paper_y = 9, 11
# (просто раскоментировать нужную строку и проверить свой код)

if (
        ((paper_x <= envelop_x) and (paper_y <= envelop_y))
        or ((paper_y <= envelop_x) and (paper_x <= envelop_y))
):
    print('ДА')
else:
    print('НЕТ')
# 1) Считается плохой практикой использовать бекслеши, хотя возможно это уже пофиксили, но раньше интерпретатор
#  "путался" в них. Поправил форматирование для того чтобы бекслеши исключить
#  2) Операторы лучше использовать по назначению. Вы применили битовый оператор вместо логического, а это далеко не одно
#  и тоже. Вот отличная статья со стека:
#  https://stackoverflow.com/questions/3845018/boolean-operators-vs-bitwise-operators
#  Наиболее показательна эта часть:
#       >>> 0 < 1 & 0 < 2
#       False
#       >>> 0 < 1 and 0 < 2
#       True
# И это ещё не считая того, что логические операторы не будут считать всю конструкцию если сразу ясен результат,
# а побитовые будут вычислять всё до упора
# TODO Не задумывался раньше об этом. Считал, что |/or и &/and равноценны. Спасибо за ценную информацию.
#  Также учёл и отметил для себя момент с бекслешами. Спасибо за объяснение причин такого к ним отношения :)

# Для исключения дублирования кода вывода положительного ответа, объедините условия с помощью логического ИЛИ
# Усложненное задание, решать по желанию.
# Заданы размеры hole_x, hole_y прямоугольного отверстия и размеры brick_х, brick_у, brick_z кирпича (все размеры
# могут быть в диапазоне от 1 до 1000)
#
# Определить, пройдет ли кирпич через отверстие (грани кирпича параллельны сторонам отверстия)

hole_x, hole_y = 8, 9
brick_x, brick_y, brick_z = 9, 10, 8
# brick_x, brick_y, brick_z = 11, 2, 10
# brick_x, brick_y, brick_z = 10, 11, 2
# brick_x, brick_y, brick_z = 10, 2, 11
# brick_x, brick_y, brick_z = 2, 10, 11
# brick_x, brick_y, brick_z = 2, 11, 10
# brick_x, brick_y, brick_z = 3, 5, 6
# brick_x, brick_y, brick_z = 3, 6, 5
# brick_x, brick_y, brick_z = 6, 3, 5
# brick_x, brick_y, brick_z = 6, 5, 3
# brick_x, brick_y, brick_z = 5, 6, 3
# brick_x, brick_y, brick_z = 5, 3, 6
# brick_x, brick_y, brick_z = 11, 3, 6
# brick_x, brick_y, brick_z = 11, 6, 3
# brick_x, brick_y, brick_z = 6, 11, 3
# brick_x, brick_y, brick_z = 6, 3, 11
# brick_x, brick_y, brick_z = 3, 6, 11
# brick_x, brick_y, brick_z = 3, 11, 6
# (просто раскоментировать нужную строку и проверить свой код)

# Решение "в лоб", перебором
if (
        ((brick_x <= hole_x) and (brick_y <= hole_y))
        or ((brick_y <= hole_x) and (brick_x <= hole_y))
        or ((brick_x <= hole_x) and (brick_z <= hole_y))
        or ((brick_z <= hole_x) and (brick_x <= hole_y))
        or ((brick_y <= hole_x) and (brick_z <= hole_y))
        or ((brick_z <= hole_x) and (brick_y <= hole_y))
):
    print('ДА')
else:
    print('НЕТ')


# Альтернативное решение
# Великолепно! А можно было выкинуть максимальный размер кирпича и решить задачу алгоритмом конверта с листом.
hole = [hole_x, hole_y]
brick = [brick_x, brick_y, brick_z]
hole.sort()
brick.sort()
if (brick[0] <= hole[0]) and (brick[1] <= hole[1]):
    print('ДА')
else:
    print('НЕТ')

#  Таким образом? :)
# Like! But bitwise operators are not allowed here
brick = [brick_x, brick_y, brick_z]
brick.remove(max(brick))
if (
        ((brick[0] <= hole_x) and (brick[1] <= hole_y))
        or ((brick[1] <= hole_x) and (brick[0] <= hole_y))
):
    print('ДА')
else:
    print('НЕТ')

