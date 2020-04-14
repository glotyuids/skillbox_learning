# -*- coding: utf-8 -*-

from termcolor import cprint
from random import randint, choice

######################################################## Часть первая
#
# Создать модель жизни небольшой семьи.
#
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
# +   есть,
# +   играть в WoT,
# +   ходить на работу,

#  Не могу согласиться с предсавленной ниже концепцией жены, поэтому введём аналогичную позицию старшей дочери
#  Жена может:
#    есть,
#    покупать продукты,
#    покупать шубу,
#    убираться в доме,
#  -
#  Старшая дочь может:
#  + есть,
#   покупать продукты,
#  + тусить в клубе (на те же деньги),
#  + убираться в доме,
# -- Задание творческое (побуждающее к творчеству) - всё в ваших руках!

# Все они живут в одном доме, дом характеризуется:
# +   кол-во денег в тумбочке (в начале - 100)
# +   кол-во еды в холодильнике (в начале - 50)
# +   кол-во грязи (в начале - 0)
#
# + У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# + Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# + Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# + Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# + Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# + Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# + Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# + Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# + Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# + Степень счастья не должна падать ниже 10, иначе чел умрает от депресии.
#
# + Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.


class House:

    def __init__(self):
        self.dirtiness = 0
        self.__money = 100
        self.__food = 50
        self.cat_food = 30
        self.money_earned = 0
        self.money_spent = 0
        self.food_bought = 0
        self.food_eaten = 0
        # TODO себе: возможно, в дальнейшем имеет смысл завести список жителей (и животных)
        # -- Отличная идея, очень упрощает и автоматизирует основной цикл программы!

    def __str__(self):
        return f'Дом: денег - {self.money}, еды - {self.food}, грязи - {self.dirtiness}'

    def get_old(self):
        self.dirtiness += 5

    #  Для того, чтобы не искать по всему коду изменение количества денег и еды (чтобы собрать статистику)
    #  попробую применить сеттеры (без геттеров почему-то не работают), о которых недавно узнал
    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self, money):
        if money > self.__money:
            self.money_earned += money - self.__money
        elif money < self.__money:
            self.money_spent += self.__money - money
        self.__money = money

    @property
    def food(self):
        return self.__food

    @food.setter
    def food(self, food):
        if food > self.__food:
            self.food_bought += food - self.__food
        elif food < self.__food:
            self.food_eaten += self.__food - food
        self.__food = food


class Human:
    def __init__(self, name, home, sex):
        self.home = home
        self.name = name
        self.fullness = 30
        self.happiness = 100
        self.sex = sex  # string: male or female
        self.chilling_number = 0

    def __str__(self):
        return f'{self.name}: сытость {self.fullness}, счастье {self.happiness}'

    def _right_sex_word(self, male_word, female_word):
        return male_word if self.sex == 'male' else female_word

    #  каждый метод, где есть вероятность "пролететь" (питание, шоппинг и т.д.) должен возвращать статус выполнения,
    #  чтобы можно было отстроить логику в act()
    #  В точку!
    def eat(self):
        if self.home.food >= 30:
            self.home.food -= 30
            self.fullness += 30
            print(f'{self.name} {self._right_sex_word("поел", "поела")}')
            return True
        else:
            print(f'{self.name} {self._right_sex_word("остался голодным", "осталась голодной")} - еды нет')
            return False

    def play_with_cat(self):
        # TODO себе: возможно, стоит передавать коту маркер того, что он сегодня был "занят", либо вызывать
        #  метод cat.play_with_human(). Сделать атрибут-флаг игрались или нет,
        #  в методе обрабатывать голод и взводить флаг, а в cat.act() просто сбрасывать флаг, если он был взведён).
        #  То есть можно накрутить, например, отказ кота в игре, если он голоден.
        #  Но это потребует некоторого времени, поэтому отложим на потом.
        print(f'{self.name} {self._right_sex_word("поиграл", "поиграла")} с котом')
        self.happiness += 5
        self.fullness -= 10

    def act(self):
        if self.fullness < 0:
            print(f'{self.name} {self._right_sex_word("умер", "умерла")} от голода')
            exit(1)
        if self.happiness < 10:
            print(f'{self.name} {self._right_sex_word("уехал", "уехала")} в дурку')
            exit(2)
        if self.home.dirtiness > 90:
            self.happiness -= 10


class Parent(Human):

    def work(self):
        print(f'{self.name} {self._right_sex_word("сходил", "сходила")} на работу')
        self.home.money += 150
        self.fullness -= 10

    def gaming(self):
        print(f'{self.name} {self._right_sex_word("сыграл", "сыграла")} катку в Doom Crossing: Eternal Horizons')
        self.happiness += 20
        self.fullness -= 10
        self.chilling_number += 1

    def act(self):
        super().act()
        dice = randint(1, 6)
        #  Тут развитие идеи из прошлого модуля, но теперь без возможности улететь в рекурсию
        if self.fullness <= 20:
            if not self.eat():
                self.work()    # безусловная работа на случай, если на покупку еды не хватит денег
        elif self.home.money < 50:
            self.work()
        elif self.happiness <= 15:
            self.gaming()
        elif 1 <= dice <= 2:
            self.work()
        elif dice == 3:
            self.play_with_cat()
        elif dice == 4:
            self.eat()
        else:
            self.gaming()


class ElderChild(Human):

    def chilling(self):
        if self.home.money >= 350:
            print(f'{self.name} {self._right_sex_word("ушёл", "ушла")} на тусовку в клуб')
            self.home.money -= 350
            self.happiness += 60
            self.fullness -= 10
            self.chilling_number += 1
            return True

        print(f'{self.name} не {self._right_sex_word("смог", "смогла")} попасть на тусовку - денег нет')
        return False

    def clean_house(self):
        print(f'{self.name} {self._right_sex_word("убрал", "убрала")} дома')
        self.home.dirtiness -= 100 if self.home.dirtiness > 100 else self.home.dirtiness
        self.fullness -= 10

    def buy_food(self):
        if 50 <= self.home.money < 100:
            print(f'{self.name} {self._right_sex_word("сходил", "сходила")} в магазин за едой')
            self.home.money -= 50
            self.home.food += 50
            self.fullness -= 10
            return True

        if self.home.money >= 100:
            print(f'{self.name} {self._right_sex_word("купил", "купила")} целый ящик доширака')
            self.home.money -= 100
            self.home.food += 100
            self.fullness -= 10
            return True

        print(f'{self.name} еды не {self._right_sex_word("купил", "купила")} - денег нет')
        return False

    def buy_cat_food(self):
        if 50 <= self.home.money < 100:
            print(f'{self.name} {self._right_sex_word("сходил", "сходила")} в зоомагазин за кошачьим кормом')
            self.home.money -= 50
            self.home.cat_food += 50
            self.fullness -= 10
            return True

        if self.home.money >= 100:
            print(f'{self.name} {self._right_sex_word("купил", "купила")} много кошачьего корма')
            self.home.money -= 100
            self.home.cat_food += 100
            self.fullness -= 10
            return True

        print(f'{self.name} корма не {self._right_sex_word("купил", "купила")} - денег нет')
        return False

    def act(self):
        super().act()
        dice = randint(1, 6)
        if self.fullness <= 20:
            if not self.eat():
                if not self.buy_food():
                    self.clean_house()
        elif self.home.food < 30:
            if not self.buy_food():
                self.clean_house()
        elif self.home.cat_food < 20:
            if not self.buy_cat_food():
                self.clean_house()
        elif self.home.dirtiness >= 80:
            self.clean_house()
        elif self.happiness <= 15:
            if not self.chilling():
                self.play_with_cat()
        elif 1 <= dice <= 2:
            self.clean_house()
        elif dice == 3:
            self.play_with_cat()
        elif dice == 4:
            self.eat()
        else:
            self.chilling()


class Cat:
    NAMES = ['Феликс', 'Том', 'Сильвестр', 'Гарфилд', 'в сапогах', 'Чешир', 'Артемис', 'Мяут', 'Котобус', 'Мистер Кэт']

    def __init__(self, home, name=None):
        if name is None:
            name = choice(Cat.NAMES)
        self.name = name
        self.fullness = 30
        self.home = home

    def __str__(self):
        return f'Я - кот {self.name}, сытость {self.fullness}'

    def eat(self):
        if self.home.cat_food >= 10:
            print(f'Кот {self.name} поел')
            self.fullness += 20
            self.home.cat_food -= 10
            return True

        print(f'Мяу! Кот {self.name} нет еды')
        return False

    def sleep(self):
        print(f'Кот {self.name} целый день дрых как скотина')
        self.fullness -= 10

    def rip_wallpapers(self):
        if randint(0, 100) > 20:
            print(f'Кот {self.name} подрал обои. Не забыть бы их подклеить')
            self.home.dirtiness += 5
        else:
            print(f'Кот {self.name} Нагадил мимо лотка. Надо конфуз убрать')
            self.home.dirtiness += 50
        self.fullness -= 10

    def act(self):
        if self.fullness < 0:
            print(f'Кот {self.name} умер...')
            quit(3)

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


home = House()
serge = Parent(name='Папа Сережа', sex='male', home=home)
masha = ElderChild(name='Дочка Маша', sex='female', home=home)
cat = Cat(home=home)

for day in range(1, 366):  # Нумерация дней с 0 не полне привычна для обихода
    cprint('================== День {} =================='.format(day), color='red')
    serge.act()
    masha.act()
    cat.act()
    home.get_old()
    cprint(serge, color='cyan')
    cprint(masha, color='cyan')
    cprint(cat, color='cyan')
    cprint(home, color='cyan')

print(f'\nДенег заработано: {home.money_earned}\n'
      f'Денег потрачено: {home.money_spent}\n'
      f'Еды куплено: {home.food_bought}\n'
      f'Еды съедено: {home.food_eaten}')

print(f'\nПапа сыграл {serge.chilling_number} каток в Doom Crossing: Eternal Horizons\n'
      f'Дочь сходила {masha.chilling_number} раз в клуб\n')

# TODO после реализации первой части - отдать на проверку учителю

######################################################## Часть вторая
#
# После подтверждения учителем первой части надо
# +отщепить ветку develop и в ней начать добавлять котов в модель семьи
#
# + Кот может:
#  + есть,
#  + спать,
#  + драть обои
#
# + Люди могут:
#  + гладить кота (растет степень счастья на 5 пунктов)
#
# + В доме добавляется:
# +  еда для кота (в начале - 30)
#
# + У кота есть имя и степень сытости (в начале - 30)
# + Любое действие кота, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# + Еда для кота покупается за деньги: за 10 денег 10 еды.
# + Кушает кот максимум по 10 единиц еды, степень сытости растет на 2 пункта за 1 пункт еды.
# + Степень сытости не должна падать ниже 0, иначе кот умрет от голода.
#
# + Если кот дерет обои, то грязи становится больше на 5 пунктов


######################################################## Часть вторая бис
#
# После реализации первой части надо в ветке мастер продолжить работу над семьей - добавить ребенка
#
# Ребенок может:
#   есть,
#   спать,
#
# отличия от взрослых - кушает максимум 10 единиц еды,
# степень счастья  - не меняется, всегда ==100 ;)

# class Child:
#
#     def __init__(self):
#         pass
#
#     def __str__(self):
#         return super().__str__()
#
#     def act(self):
#         pass
#
#     def eat(self):
#         pass
#
#     def sleep(self):
#         pass


# TODO после реализации второй части - отдать на проверку учителем две ветки


######################################################## Часть третья
#
# после подтверждения учителем второй части (обоих веток)
# влить в мастер все коммиты из ветки develop и разрешить все конфликты
# отправить на проверку учителем.


# home = House()
# serge = Father(name='Сережа')
# masha = EldestDaughter(name='Маша')
# kolya = Child(name='Коля')
# murzik = Cat(name='Мурзик')
#
# for day in range(365):
#     cprint('================== День {} =================='.format(day), color='red')
#     serge.act()
#     masha.act()
#     kolya.act()
#     murzik.act()
#     cprint(serge, color='cyan')
#     cprint(masha, color='cyan')
#     cprint(kolya, color='cyan')
#     cprint(murzik, color='cyan')


# Усложненное задание (делать по желанию)
#
# Сделать из семьи любителей котов - пусть котов будет 3, или даже 5-10.
# Коты должны выжить вместе с семьей!
#
# Определить максимальное число котов, которое может прокормить эта семья при значениях зарплаты от 50 до 400.
# Для сглаживание случайностей моделирование за год делать 3 раза, если 2 из 3х выжили - считаем что выжили.
#
# Дополнительно вносить некий хаос в жизнь семьи
# - N раз в год вдруг пропадает половина еды из холодильника (коты?)
# - K раз в год пропадает половина денег из тумбочки (муж? жена? коты?!?!)
# Промоделировать - как часто могут случаться фейлы что бы это не повлияло на жизнь героев?
#   (N от 1 до 5, K от 1 до 5 - нужно вычислит максимумы N и K при котором семья гарантированно выживает)
#
# в итоге должен получится приблизительно такой код экспериментов
# for food_incidents in range(6):
#   for money_incidents in range(6):
#       life = Simulation(money_incidents, food_incidents)
#       for salary in range(50, 401, 50):
#           max_cats = life.experiment(salary)
#           print(f'При зарплате {salary} максимально можно прокормить {max_cats} котов')

