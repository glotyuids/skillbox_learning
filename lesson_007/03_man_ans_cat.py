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
        if self.house.money >= 50:
            cprint('{} сходил в магазин за едой'.format(self.name), color='magenta')
            self.house.money -= 50
            self.house.food += 50
        else:
            cprint('{} денег на еду нет!'.format(self.name), color='red')

    def buy_cat_food(self):
        if self.house.money >= 50:
            cprint('{} сходил в зоомагазин за кормом для кота'.format(self.name), color='magenta')
            self.house.money -= 50
            self.house.cat_food += 50
        else:
            cprint('{} на кошачий корм денег нет!'.format(self.name), color='red')

    def clean_house(self):
        cprint('{} убрался в доме'.format(self.name), color='magenta')
        self.fullness -= 10
        self.house.dirtiness -= 100

    def go_to_the_house(self, house):
        self.house = house
        self.fullness -= 10
        cprint('{} Вьехал в дом'.format(self.name), color='cyan')

    def take_cat_from_animal_shelter(self):
        cat_names = ['Феликс', 'Том', 'Сильвестр', 'Гарфилд', 'в сапогах',
                     'Чешир', 'Артемис', 'Мяут', 'Котобус', 'Мистер Кэт']
        cprint('{} Взял кота из приюта'.format(self.name), color='cyan')
        return Cat(name=choice(cat_names), house=self.house)

    def act(self):
        if self.fullness <= 0:
            cprint('{} умер...'.format(self.name), color='red')
            quit()
            return
        dice = randint(1, 6)
        if self.fullness < 20:
            self.eat()
        elif self.house.food < 10:
            self.shopping()
        elif self.house.money < 50:
            self.work()
        elif self.house.cat_food < 10:
            self.buy_cat_food()
        elif self.house.dirtiness > 100:
            self.clean_house()
        elif dice == 1:
            self.work()
        elif dice == 2:
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

    def sleep(self):
        cprint('Кот {} целый день дрых как скотина'.format(self.name), color='green')
        self.fullness -= 10

    def rip_wallpapers(self):
        if randint(0,100) > 35:
            cprint('Кот {} подрал обои. Не забыть бы их подклеить'.format(self.name), color='green')
            self.house.dirtiness += 5
        else:
            cprint('Кот {} Нагадил мимо лотка. Надо конфуз убрать'.format(self.name), color='red')
            self.house.dirtiness += 50
        self.fullness -= 10

    def act(self):
        if self.fullness <= 0:
            cprint('Кот {} умер...'.format(self.name), color='red')
            quit()
            return
        dice = randint(1, 6)
        if self.fullness < 20:
            self.eat()
        elif dice == 4:
            self.eat()
        elif dice > 4:
            self.rip_wallpapers()
        else:
            self.sleep()


beavis = Man(name='Бивис')

my_sweet_home = House()
beavis.go_to_the_house(house=my_sweet_home)
cat = beavis.take_cat_from_animal_shelter()

for day in range(1, 366):
    print('================ день {} =================='.format(day))
    beavis.act()
    cat.act()
    print('--- в конце дня ---')
    print(beavis)
    print(cat)
    print(my_sweet_home)

# Усложненное задание (делать по желанию)
# Создать несколько (2-3) котов и подселить их в дом к человеку.
# Им всем вместе так же надо прожить 365 дней.

# (Можно определить критическое количество котов, которое может прокормить человек...)
