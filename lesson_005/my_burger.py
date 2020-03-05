# -*- coding: utf-8 -*-


def add_bun(top=False, my_burger=False):
    if my_burger:
        print('Всё на булочке с кунжутом.\n')
    else:
        print('И накрываем второй половинкой булочки, прижаренной на гриле\n' if top
              else 'Берём карамелизованную булочку\n', end='')


def add_beefsteak(my_burger=False):
    print('Две мясных котлеты гриль,\n' if my_burger
          else 'Сверху кладём два рубленых бифштекса из натуральной цельной говядины\n', end='')


def add_cucumber(my_burger=False):
    print('Огурцы, ' if my_burger else 'Добавляем пару кусочков маринованного огурчика\n', end='')


def add_tomato():
    pass    # помидор нам ни в одном рецепте не пригодится, но он есть в тексте задания, поэтому вот


def add_sauce(my_burger=False):
    print('Специальный соус, ' if my_burger
          else 'Заправляем горчицей, кетчупом, приправляем мелко рубленным луком-шалот\n', end='')


def add_cheese(my_burger=False):
    print('сыр,\n' if my_burger else 'Перемежая их квадратиками сыра «Чеддер»\n', end='')


def add_lettuce():
    print('салат ', end='')


def add_onion():
    print('и лук,\n', end='')


def pack():
    print('Только так!\n'
          'И это Биг Мак!')
