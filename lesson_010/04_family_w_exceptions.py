# -*- coding: utf-8 -*-

from termcolor import cprint
from random import randint, choice, sample
from tabulate import tabulate


PRINT_LOG = False


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
        self.residents = []
        self.pets = []

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
    def eat(self, food_amount=30):
        if self.home.food >= food_amount:
            self.home.food -= food_amount
            self.fullness += food_amount
            lgprint(f'{self.name} {self._right_sex_word("поел", "поела")}')
            return True
        else:
            lgprint(f'{self.name} {self._right_sex_word("остался голодным", "осталась голодной")} - еды нет')
            return False

    def play_with_cat(self):
        lgprint(f'{self.name} {self._right_sex_word("поиграл", "поиграла")} с котом')
        self.happiness += 5
        self.fullness -= 10

    def act(self):
        if self.fullness < 0:
            lgprint(f'{self.name} {self._right_sex_word("умер", "умерла")} от голода')
            return 1
        if self.happiness < 10:
            lgprint(f'{self.name} {self._right_sex_word("уехал", "уехала")} в дурку')
            return 2
        if self.home.dirtiness > 90:
            self.happiness -= 10
        return 0


class Parent(Human):

    def __init__(self, salary=150, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.salary = salary

    def work(self):
        lgprint(f'{self.name} {self._right_sex_word("сходил", "сходила")} на работу')
        self.home.money += self.salary
        self.fullness -= 10

    def gaming(self):
        lgprint(f'{self.name} {self._right_sex_word("сыграл", "сыграла")} катку в Doom Crossing: Eternal Horizons')
        self.happiness += 20
        self.fullness -= 10
        self.chilling_number += 1

    def act(self):
        disease = super().act()
        if disease:
            return disease

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

        return 0


class ElderChild(Human):

    def chilling(self):
        if self.home.money >= 350:
            lgprint(f'{self.name} {self._right_sex_word("ушёл", "ушла")} на тусовку в клуб')
            self.home.money -= 350
            self.happiness += 60
            self.fullness -= 10
            self.chilling_number += 1
            return True

        lgprint(f'{self.name} не {self._right_sex_word("смог", "смогла")} попасть на тусовку - денег нет')
        return False

    def clean_house(self):
        lgprint(f'{self.name} {self._right_sex_word("убрал", "убрала")} дома')
        self.home.dirtiness -= 100 if self.home.dirtiness > 100 else self.home.dirtiness
        self.fullness -= 10

    def buy_food(self):
        if 50 <= self.home.money < 100:
            lgprint(f'{self.name} {self._right_sex_word("сходил", "сходила")} в магазин за едой')
            self.home.money -= 50
            self.home.food += 50
            self.fullness -= 10
            return True

        if self.home.money >= 100:
            lgprint(f'{self.name} {self._right_sex_word("купил", "купила")} целый ящик доширака')
            self.home.money -= 100
            self.home.food += 100
            self.fullness -= 10
            return True

        lgprint(f'{self.name} еды не {self._right_sex_word("купил", "купила")} - денег нет')
        return False

    def buy_cat_food(self):
        if 50 <= self.home.money < 100:
            lgprint(f'{self.name} {self._right_sex_word("сходил", "сходила")} в зоомагазин за кошачьим кормом')
            self.home.money -= 50
            self.home.cat_food += 50
            self.fullness -= 10
            return True

        if self.home.money >= 100:
            lgprint(f'{self.name} {self._right_sex_word("купил", "купила")} много кошачьего корма')
            self.home.money -= 100
            self.home.cat_food += 100
            self.fullness -= 10
            return True

        lgprint(f'{self.name} корма не {self._right_sex_word("купил", "купила")} - денег нет')
        return False

    def act(self):
        disease = super().act()
        if disease:
            return disease

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

        return 0


class YoungerChild(Human):

    def act(self):
        disease = super().act()
        if disease:
            return disease

        self.happiness = 100
        dice = randint(1, 6)
        if self.fullness <= 10:
            if not self.eat():
                self.sleep()
        elif dice < 3:
            if not self.eat():
                self.sleep()
        else:
            self.sleep()

        return 0

    def eat(self):
        return super().eat(food_amount=10)

    def sleep(self):
        lgprint(f'{self.name} сегодня весь день {self._right_sex_word("спал", "спала")}')
        self.fullness -= 10


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
            lgprint(f'Кот {self.name} поел')
            self.fullness += 20
            self.home.cat_food -= 10
            return True

        lgprint(f'Мяу! Кот {self.name} нет еды')
        return False

    def sleep(self):
        lgprint(f'Кот {self.name} целый день дрых как скотина')
        self.fullness -= 10

    def rip_wallpapers(self):
        if randint(0, 100) > 20:
            lgprint(f'Кот {self.name} подрал обои. Не забыть бы их подклеить')
            self.home.dirtiness += 5
        else:
            lgprint(f'Кот {self.name} Нагадил мимо лотка. Надо конфуз убрать')
            self.home.dirtiness += 50
        self.fullness -= 10

    def act(self):
        if self.fullness < 0:
            lgprint(f'Кот {self.name} умер...')
            return 3

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

        return 0




class Simulation:

    def __init__(self, money_incidents, food_incidents):
        self.money_incidents = money_incidents
        self.food_incidents = food_incidents
        self.max_cats = 0
        self.money_incidents_days = []
        self.food_incidents_days = []
        self.seed_incidents()

    def seed_incidents(self, money_incidents=None, food_incidents=None):
        """
        Метод создаёт список дней, когда будут возникать проблемы с деньгами и едой

        Parameters
        ----------
        money_incidents: int, default=None
            Количество проблем с деньгами в году

        food_incidents: int, default=None
            Количество проблем с едой в году
        """
        self.money_incidents = money_incidents if money_incidents is not None else self.money_incidents
        self.food_incidents = food_incidents if food_incidents is not None else self.food_incidents
        self.money_incidents_days = sample(range(1, 366), self.money_incidents)
        self.food_incidents_days = sample(range(1, 366), self.food_incidents)

    def live_a_year(self, salary, attempt, cats_number=0):
        """
        В этом методе семья проживает год своей жизни

        Parameters
        ----------
        salary: int
            Зарплата главы семейства

        attempt: int
            Номер попытки. Здесь нужен только для корректного вывода на консоль

        cats_number: int, default=0
            Количество кошек в доме

        Returns
        -------
        True, если семья дожила до конца года и False - если нет
        """
        home = House()
        home.residents.append(Parent(name='Папа Сережа', sex='male', salary=salary, home=home))
        home.residents.append(ElderChild(name='Дочка Маша', sex='female', home=home))
        home.residents.append(YoungerChild(name='Сынок Коля', sex='male', home=home))
        #  Предполагалось, что это будет осуществляться автоматически при создании "жителя", то есть в __init__
        for _ in range(cats_number):
            home.pets.append(Cat(home=home))

        for day in range(1, 366):
            lgprint(f'=============== {cats_number} кошек - Попытка {attempt} - День {day} ===============', color='red')
            if day in self.money_incidents_days:
                lgprint('Из копилки пропала половина денег!', color='red')
                home.money //= 2
            if day in self.food_incidents_days:
                lgprint('Из холодильника пропала половина еды!', color='red')
                home.food //= 2

            diseases = sum([someone.act() for someone in home.residents + home.pets])
            if diseases:
                return False
            home.get_old()
            for someone in home.residents + home.pets + [home]:
                lgprint(someone, color='cyan')

        return True

    def experiment(self, salary):
        """
        В этом методе проводится эксперимент по поиску максимального количество кошек, с которым семья может выжить.
        Для сглаживания случайностей моделирование делается 3 раза, если два раза из трёх выжили - эксперимент успешен.

        В цикле просто посследовательно увеличиваем количество котов и проводим эксперимент
            (для оптимизации расчёта кол-ва кошек можно было бы использовать метод умножения на два и вычитания половин,
            но здесь это лишь усложнит код)
        Выход из цикла происходит при неудачном результате эксперимента


        Parameters
        ----------
        salary: int
            Зарплата главы семейства

        Returns
        -------
        Максимальное количество кошек, которое может прокормить семейство при заданных вводных
        """
        cats_number = 0
        while True:
            cats_number += 1

            success_attempts = 0
            for attempt in range(1, 4):
                attempt_result = self.live_a_year(salary=salary, attempt=attempt, cats_number=cats_number)
                success_attempts += 1 if attempt_result else 0
                if success_attempts == 1 and attempt == 2:
                    break
                if success_attempts == 2:
                    break

            if success_attempts >= 2:
                lgprint(f'\n{cats_number} кошек - успешный эксперимент\n', color='green')
            else:
                lgprint(f'\n{cats_number} кошек - неудачный эксперимент\n', color='red')
                break

        return cats_number - 1


def lgprint(*args, **kwargs):
    if PRINT_LOG:
        cprint(*args, **kwargs)


print('\nВыполняется симуляция, пожалуйста подождите...')
cprint('\nЭто процесс длительный, занимает порядка 30 секунд, \n'
       'поскольку будет проведено около 2 592 симуляций, \n'
       'прожито около 946 080 дней! \n'
       'Как раз примерно столько времени назад родился Пифагор, а в Афинах начали чеканить монеты', color='cyan')
print('\nМаксимальное количество кошек будет выводиться в ячейках таблиц, \n'
      'столбцы - количество фейлов с деньгами, строки - количество фейлов с едой')
print('Данные сгруппированы по таблицам в соответствии с зарплатой')


experiment_results = {}
for salary in range(50, 401, 50):
    experiment_results[salary] = {}
    for food_incidents in range(0, 6):
        experiment_results[salary][food_incidents] = {}
        for money_incidents in range(0, 6):
            life = Simulation(money_incidents=money_incidents, food_incidents=food_incidents)
            max_cats = life.experiment(salary)
            experiment_results[salary][food_incidents][money_incidents] = max_cats

print('')
for salary, incidents in experiment_results.items():
    cprint('\nЗарплата: ', color='yellow', end='')
    print(salary)
    cprint(' ↓ Фейлы с едой | → Фейлы с деньгами', color='yellow')
    print(tabulate(incidents.values(), headers="keys", showindex=incidents.keys(), tablefmt="github"))
