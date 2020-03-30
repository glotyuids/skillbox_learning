# -*- coding: utf-8 -*-

from random import randint, choice

# Доработать практическую часть урока lesson_007/python_snippets/08_practice.py

# + Необходимо создать класс кота. У кота есть аттрибуты - сытость и дом (в котором он живет).
# + Кот живет с человеком в доме.
# + Для кота дом характеризируется - миской для еды и грязью.
# + Изначально в доме нет еды для кота и нет грязи.

# + Доработать класс человека, добавив методы
#   + подобрать кота - у кота появляется дом.
#   + купить коту еды - кошачья еда в доме увеличивается на 50, деньги уменьшаются на 50.
#   + убраться в доме - степень грязи в доме уменьшается на 100, сытость у человека уменьшается на 20.
#   + Увеличить кол-во зарабатываемых человеком денег до 150 (он выучил пайтон и устроился на хорошую работу :)

# + Кот может есть, спать и драть обои - необходимо реализовать соответствующие методы.
# + Когда кот спит - сытость уменьшается на 10
# + Когда кот ест - сытость увеличивается на 20, кошачья еда в доме уменьшается на 10.
# + Когда кот дерет обои - сытость уменьшается на 10, степень грязи в доме увеличивается на 5
# + Если степень сытости < 0, кот умирает.
# + Так же надо реализовать метод "действуй" для кота, в котором он принимает решение
#   что будет делать сегодня

# Человеку и коту надо вместе прожить 365 дней.

from termcolor import cprint


class Man:

    def __init__(self, name):
        self.name = name
        self.fullness = 50
        self.house = None

    def __str__(self):
        return 'Я - {}, сытость {}'.format(
            self.name, self.fullness)

    def eat(self):
        if self.house.food >= 10:
            cprint('{} поел'.format(self.name), color='yellow')
            self.fullness += 10
            self.house.food -= 10
        else:
            cprint('{} нет еды'.format(self.name), color='red')

    def work(self):
        cprint('{} сходил на работу'.format(self.name), color='blue')
        self.house.money += 150
        self.fullness -= 10

    def watch_MTV(self):
        cprint('{} смотрел MTV целый день'.format(self.name), color='green')
        self.fullness -= 10

    def shopping(self):
        if 50 <= self.house.money < 100:
            cprint('{} сходил в магазин за едой'.format(self.name), color='magenta')
            self.house.money -= 50
            self.house.food += 50
        elif self.house.money >= 100:
            cprint('{} купил целый ящик доширака'.format(self.name), color='magenta')
            self.house.money -= 100
            self.house.food += 100
        else:
            cprint('{} денег на еду нет!'.format(self.name), color='red')
            #  Люди не умирали от голода, поскольку во время голода сытость не изменялась. Исправил
            # Отлично, что вы сами это оттестировали и нашли

    def buy_cat_food(self):
        if 50 <= self.house.money < 100:
            cprint('{} сходил в зоомагазин за кошачьим кормом'.format(self.name), color='magenta')
            self.house.money -= 50
            self.house.cat_food += 50
        elif self.house.money >= 100:
            cprint('{} купил много кошачьего корма'.format(self.name), color='magenta')
            self.house.money -= 100
            self.house.cat_food += 100
        else:
            cprint('{} на кошачий корм денег нет!'.format(self.name), color='red')

    def clean_house(self):
        if self.house.dirtiness >= 500 and self.house.money >= 50:
            self.call_cleaning()
        else:
            cprint('{} убрался в доме'.format(self.name), color='magenta')
            self.fullness -= 10
            self.house.dirtiness -= 100

    def call_cleaning(self):
        if self.house.money >= 50:
            cprint('{} вызвал клининг'.format(self.name), color='magenta')
            self.house.money -= 50
            self.house.dirtiness -= 500
        else:
            cprint('{} денег на клининг нет!'.format(self.name), color='red')

    def go_to_the_house(self, house):
        self.house = house
        self.fullness -= 10
        cprint('{} Вьехал в дом'.format(self.name), color='cyan')

    def take_cat_from_animal_shelter(self):
        # Изначально сытость уменьшалась на 10, но тогда на 4 коте человек умирал.
        #  Поэтому предположим, что приют находится прямо напротив дома
        # TODO Любое действие отнимает 10 от сытости
        self.fullness -= 0
        cat_names = ['Феликс', 'Том', 'Сильвестр', 'Гарфилд', 'в сапогах',
                     'Чешир', 'Артемис', 'Мяут', 'Котобус', 'Мистер Кэт']
        # TOdO Глобальная константа!
        cprint('{} Взял кота из приюта'.format(self.name), color='cyan')
        return Cat(name=choice(cat_names), house=self.house)

    def act(self, number_of_cats=0):
        if self.fullness <= 0:
            cprint('{} умер...'.format(self.name), color='red')
            quit(1)
        dice = randint(1, 6)
        if self.fullness < 20:
            self.eat()
        elif self.house.food < 30:
            self.shopping()
        elif self.house.money < 50:
            self.work()
        elif self.house.cat_food < number_of_cats * 20:
            self.buy_cat_food()
        elif self.house.dirtiness > 100:
            self.clean_house()
        elif 1 <= dice <= 3:
            self.work()
        elif dice == 4:
            self.eat()
        else:
            self.watch_MTV()


class House:

    def __init__(self):
        self.food = 50
        self.cat_food = 0
        self.dirtiness = 0
        self.money = 0

    def __str__(self):
        return 'В доме еды осталось {}, кошачьего корма осталось {}, денег осталось {}, грязи в доме {}'.format(
            self.food, self.cat_food, self.money, self.dirtiness)

    def check_status(self):
        if self.dirtiness < 100:
            cprint('Дом чист - приятно посмотреть', color='magenta')
        elif 100 <= self.dirtiness < 500:
            cprint('Дому требуется уборка', color='magenta')
        elif 500 <= self.dirtiness < 1500:
            cprint('Хозяевам самим уже не справиться. Нужен клининг!', color='magenta')
        else:
            cprint('В этой свалке уже сложно разглядеть очертания дома. Все были выселены', color='red')
            quit(3)


class Cat:
    def __init__(self, name, house):
        self.name = name
        self.fullness = 50
        self.house = house

    def __str__(self):
        return 'Я - кот {}, сытость {}'.format(
            self.name, self.fullness)

    def eat(self):
        if self.house.cat_food >= 10:
            cprint('Кот {} поел'.format(self.name), color='yellow')
            self.fullness += 20
            self.house.cat_food -= 10
        else:
            cprint('Мяу! Кот {} нет еды'.format(self.name), color='red')
            self.fullness -= 10

    def sleep(self):
        cprint('Кот {} целый день дрых как скотина'.format(self.name), color='green')
        self.fullness -= 10

    def rip_wallpapers(self):
        if randint(0, 100) > 20:
            cprint('Кот {} подрал обои. Не забыть бы их подклеить'.format(self.name), color='green')
            self.house.dirtiness += 5
        else:
            cprint('Кот {} Нагадил мимо лотка. Надо конфуз убрать'.format(self.name), color='red')
            self.house.dirtiness += 50
        self.fullness -= 10

    def act(self):
        if self.fullness <= 0:
            cprint('Кот {} умер...'.format(self.name), color='red')
            quit(2)
            return
        dice = randint(1, 6)
        if self.fullness < 20:
            self.eat()
        elif self.fullness > 100:
            if 1 <= dice <= 2:
                self.rip_wallpapers()
            else:
                self.sleep()
        elif 1 <= dice <= 2:
            self.eat()
        elif 3 <= dice <= 4:
            self.rip_wallpapers()
        else:
            self.sleep()


beavis = Man(name='Бивис')

my_sweet_home = House()
beavis.go_to_the_house(house=my_sweet_home)
cats = [beavis.take_cat_from_animal_shelter() for _ in range(8)]

for day in range(1, 366):
    print('================ день {} =================='.format(day))
    beavis.act(number_of_cats=len(cats))
    for cat in cats:
        cat.act()
    my_sweet_home.check_status()
    print('--- в конце дня ---')
    print(beavis)
    for cat in cats:
        print(cat)
    print(my_sweet_home)

# Усложненное задание (делать по желанию)
# Создать несколько (2-3) котов и подселить их в дом к человеку.
# Им всем вместе так же надо прожить 365 дней.

# (Можно определить критическое количество котов, которое может прокормить человек...)
