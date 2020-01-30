#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть список песен группы Depeche Mode со временем звучания с точностью до долей минут
# Точность указывается в функции round(a, b)
# где a, это число которое надо округлить, а b количество знаков после запятой
# более подробно про функцию round смотрите в документации https://docs.python.org/3/search.html?q=round

violator_songs_list = [
    ['World in My Eyes', 4.86],
    ['Sweetest Perfection', 4.43],
    ['Personal Jesus', 4.56],
    ['Halo', 4.9],
    ['Waiting for the Night', 6.07],
    ['Enjoy the Silence', 4.20],
    ['Policy of Truth', 4.76],
    ['Blue Dress', 4.29],
    ['Clean', 5.83],
]

# распечатайте общее время звучания трех песен: 'Halo', 'Enjoy the Silence' и 'Clean' в формате
#   Три песни звучат ХХХ.XX минут
# Обратите внимание, что делать много вычислений внутри print() - плохой стиль.
# Лучше заранее вычислить необходимое, а затем в print(xxx, yyy, zzz)

total_duration = 0
playlist = ['Halo', 'Enjoy the Silence', 'Clean']
for song in violator_songs_list:
    if song[0] in playlist:
        total_duration += song[1]
total_duration = round(total_duration, 2)
print(f'Три песни звучат {total_duration} минут')

# Есть словарь песен группы Depeche Mode
violator_songs_dict = {
    'World in My Eyes': 4.76,
    'Sweetest Perfection': 4.43,
    'Personal Jesus': 4.56,
    'Halo': 4.30,
    'Waiting for the Night': 6.07,
    'Enjoy the Silence': 4.6,
    'Policy of Truth': 4.88,
    'Blue Dress': 4.18,
    'Clean': 5.68,
}

# распечатайте общее время звучания трех песен: 'Sweetest Perfection', 'Policy of Truth' и 'Blue Dress'
#   А другие три песни звучат ХХХ минут

total_duration = (
        violator_songs_dict['Sweetest Perfection']
        + violator_songs_dict['Policy of Truth']
        + violator_songs_dict['Blue Dress']
)
total_duration = round(total_duration, 2)
print(f'А другие три песни звучат {total_duration} минут')

# зачет! Посмотрите как избавиться от бекслешей при разбиении строк длинных вычислений.
# Как насчёт такого варианта (кажется вы не новичок):

total_duration = round(sum(
    value for key, value in violator_songs_dict.items()
    if key in ['Sweetest Perfection', 'Policy of Truth', 'Blue Dress']
), 2)
# TODO Лихой трюк) Я не сразу разобрался что в этом генераторе списков происходит.
#  "key, value" ввело в заблуждение - никгда не извлекал в циклах сразу два значения.
#  Когда понял этот момент, дальше всё встало на свои места.
#  Спасибо за пример, надо будет попрактиковаться, чтобы закрепить
