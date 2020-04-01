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


CAT_NAMES = ['Феликс', 'Том', 'Сильвестр', 'Гарфилд', 'в сапогах', 'Чешир', 'Артемис', 'Мяут', 'Котобус', 'Мистер Кэт']


class Man:

    def __init__(self, name, desired_number_of_cats=0):
        self.name = name
        self.fullness = 50
        self.house = None
        self.desired_number_of_cats = desired_number_of_cats
        # TODO для оптимизации жизни добавим человеку намерения.они нужны на случай перекрывающихся потребностей:
        #  например, человек хочет есть, но нет еды. В предыдущей реализации
        self.intentions = []

    def __str__(self):
        return f'Я - {self.name}, сытость {self.fullness}, хочу еще {self.desired_number_of_cats} котов'

    def eat(self):
        if self.house.food >= 10:
            cprint('{} поел'.format(self.name), color='yellow')
            self.fullness += 10
            self.house.food -= 10
            if self.intentions and self.intentions[-1] == 'eat':
                del self.intentions[-1]
        else:
            cprint('{} нет еды'.format(self.name), color='red')
            # self.fullness -= 10
            self.intentions.append('buy_food')
            self.shopping(min_food=30, min_cat_food=self.house.cats_number * 20)

    def work(self):
        cprint('{} сходил на работу'.format(self.name), color='blue')
        self.house.money += 150
        self.fullness -= 10
        if self.intentions and self.intentions[-1] == 'work':
            del self.intentions[-1]

    def watch_MTV(self):
        cprint('{} смотрел MTV целый день'.format(self.name), color='green')
        self.fullness -= 10
        if self.intentions and self.intentions[-1] == 'watch_mtv':
            del self.intentions[-1]

    def shopping(self, min_food=0, min_cat_food=0):
        # TODO Оптимизировал процесс закупок. Теперь человек закупается в одном торговом центре,
        #  а значит покупая один ресурс он может попутно докупить и другой.

        # TODO Энергия тратится только если человек дошёл до магазина.
        #  Если денег не хватило, то энергия не тратится - человек пересчитал их дома до похода в магазин
        before_shopping_money = self.house.money

        if self.intentions[-1] == 'buy_cat_food':
            if self.house.cat_food < min_cat_food:
                self.buy_cat_food(shopping_mall=True)
            if self.house.food < min_food + 20:
                self.buy_food(shopping_mall=True)
        else:
            if self.house.food < min_food:
                self.buy_food(shopping_mall=True)
            if self.house.cat_food < min_cat_food + 20:
                self.buy_cat_food(shopping_mall=True)

        if self.house.money != before_shopping_money:
            self.fullness -= 10
        else:
            self.intentions.append('work')
            self.work()

    def buy_cat_food(self, shopping_mall=False):

        want_to_buy = self.house.cats_number * 20
        price = want_to_buy

        if price <= self.house.money < price * 2:
            cprint('{} сходил в зоомагазин и купил {} кошачьего корма'
                   .format(self.name, want_to_buy), color='magenta')
            self.house.money -= price
            self.house.cat_food += want_to_buy
            if not shopping_mall:
                self.fullness -= 10
            if self.intentions and self.intentions[-1] == 'buy_cat_food':
                del self.intentions[-1]

        elif self.house.money >= price * 3:
            cprint('{} сходил в зоомагазин и купил {} кошачьего корма'
                   .format(self.name, want_to_buy * 2), color='magenta')
            self.house.money -= price * 2
            self.house.cat_food += want_to_buy * 2
            if not shopping_mall:
                self.fullness -= 10
            if self.intentions and self.intentions[-1] == 'buy_cat_food':
                del self.intentions[-1]
        else:
            cprint('{} на кошачий корм денег нет!'.format(self.name), color='red')
            if self.intentions[-1] != 'work':
                self.intentions.append('work')

    def buy_food(self, shopping_mall=False):
        if 50 <= self.house.money < 100:
            cprint('{} сходил в магазин за едой'.format(self.name), color='magenta')
            self.house.money -= 50
            self.house.cat_food += 50
            if not shopping_mall:
                self.fullness -= 10
            if self.intentions and self.intentions[-1] == 'buy_food':
                del self.intentions[-1]
        elif self.house.money >= 150:
            cprint('{} купил целый ящик доширака'.format(self.name), color='magenta')
            self.house.money -= 100
            self.house.cat_food += 100
            if not shopping_mall:
                self.fullness -= 10
            if self.intentions and self.intentions[-1] == 'buy_food':
                del self.intentions[-1]
        else:
            cprint('{} денег на еду нет!'.format(self.name), color='red')
            if self.intentions[-1] != 'work':
                self.intentions.append('work')

    def clean_house(self):
        if self.house.dirtiness >= 500 and self.house.money >= 50:
            self.call_cleaning()
        else:
            cprint('{} убрался в доме'.format(self.name), color='magenta')
            self.fullness -= 10
            self.house.dirtiness -= 100
        if self.intentions and self.intentions[-1] == 'clean_house':
            del self.intentions[-1]

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
        # Любое действие отнимает 10 от сытости
        self.fullness -= 10
        self.desired_number_of_cats -= 1
        self.house.cats_number += 1
        if self.intentions and self.intentions[-1] == 'take_new_cat':
            del self.intentions[-1]
        cprint('{} Взял кота из приюта'.format(self.name), color='cyan')
        return Cat(name=choice(CAT_NAMES), house=self.house)

    def act(self, my_cats):
        # + work
        # + eat
        # + buy_food
        # + buy_cat_food
        # + watch_mtv
        # + clean_house
        # + take_new_cat
        if self.fullness <= 0:
            cprint('{} умер...'.format(self.name), color='red')
            quit(1)
        dice = randint(1, 6)


        if self.fullness < 20:
            self.intentions.append('eat')
        elif self.house.food < 30:
            self.intentions.append('buy_food')
        elif self.house.money < 50:
            self.intentions.append('work')

        if not self.intentions:
            if self.house.cat_food < self.house.cats_number * 20:
                self.intentions.append('buy_cat_food')
            elif self.house.dirtiness > 100:
                self.intentions.append('clean_house')
            elif self.desired_number_of_cats > 0:
                self.intentions.append('take_new_cat')
            elif 1 <= dice <= 3:
                self.intentions.append('work')
            elif dice == 4:
                self.intentions.append('eat')
            else:
                self.intentions.append('watch_mtv')

        print(f'Намерения: {self.intentions}')

        if self.intentions:
            if self.intentions[-1] == 'work':
                self.work()
            elif self.intentions[-1] == 'eat':
                self.eat()
            elif self.intentions[-1] == 'buy_food':
                self.shopping(min_food=30, min_cat_food=self.house.cats_number * 20)
            elif self.intentions[-1] == 'buy_cat_food':
                self.shopping(min_food=30, min_cat_food=self.house.cats_number * 20)
            elif self.intentions[-1] == 'watch_mtv':
                self.watch_MTV()
            elif self.intentions[-1] == 'clean_house':
                self.clean_house()
            elif self.intentions[-1] == 'take_new_cat':
                my_cats.append(self.take_cat_from_animal_shelter())


class House:

    def __init__(self):
        self.food = 50
        self.cats_number = 0
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


beavis = Man(name='Бивис', desired_number_of_cats=100)

my_sweet_home = House()
beavis.go_to_the_house(house=my_sweet_home)
cats = [beavis.take_cat_from_animal_shelter()]
day_last_cat_taken = 0
current_cats_number = 1

for day in range(1, 366):
    print('================ день {} =================='.format(day))
    beavis.act(cats)
    for cat in cats:
        cat.act()
    my_sweet_home.check_status()

    if current_cats_number < my_sweet_home.cats_number:
        current_cats_number = my_sweet_home.cats_number
        day_last_cat_taken = day

    print('--- в конце дня ---')
    print(beavis)
    for cat in cats:
        print(cat)
    print(my_sweet_home)
    print('Последнего кота заселили на {} день'.format(day_last_cat_taken))


# Усложненное задание (делать по желанию)
# Создать несколько (2-3) котов и подселить их в дом к человеку.
# Им всем вместе так же надо прожить 365 дней.

# (Можно определить критическое количество котов, которое может прокормить человек...)
