# -*- coding: utf-8 -*-

# Подземелье было выкопано ящеро-подобными монстрами рядом с аномальной рекой, постоянно выходящей из берегов.
# Из-за этого подземелье регулярно затапливается, монстры выживают, но не герои, рискнувшие спуститься к ним в поисках
# приключений.
# Почуяв безнаказанность, ящеры начали совершать набеги на ближайшие деревни. На защиту всех деревень не хватило
# солдат и вас, как известного в этих краях героя, наняли для их спасения.
#
# Карта подземелья представляет собой json-файл под названием rpg.json. Каждая локация в лабиринте описывается объектом,
# в котором находится единственный ключ с названием, соответствующем формату "Location_<N>_tm<T>",
# где N - это номер локации (целое число), а T (вещественное число) - это время,
# которое необходимо для перехода в эту локацию. Например, если игрок заходит в локацию "Location_8_tm30000",
# то он тратит на это 30000 секунд.
# По данному ключу находится список, который содержит в себе строки с описанием монстров а также другие локации.
# Описание монстра представляет собой строку в формате "Mob_exp<K>_tm<M>", где K (целое число) - это количество опыта,
# которое получает игрок, уничтожив данного монстра, а M (вещественное число) - это время,
# которое потратит игрок для уничтожения данного монстра.
# Например, уничтожив монстра "Boss_exp10_tm20", игрок потратит 20 секунд и получит 10 единиц опыта.
# Гарантируется, что в начале пути будет две локации и один монстр
# (то есть в коренном json-объекте содержится список, содержащий два json-объекта, одного монстра и ничего больше).
#
# На прохождение игры игроку дается 123456.0987654321 секунд.
# Цель игры: за отведенное время найти выход ("Hatch")
#
# По мере прохождения вглубь подземелья, оно начинает затапливаться, поэтому
# в каждую локацию можно попасть только один раз,
# и выйти из нее нельзя (то есть двигаться можно только вперед).
#
# Чтобы открыть люк ("Hatch") и выбраться через него на поверхность, нужно иметь не менее 280 очков опыта.
# Если до открытия люка время заканчивается - герой задыхается и умирает, воскрешаясь перед входом в подземелье,
# готовый к следующей попытке (игра начинается заново).
#
# Гарантируется, что искомый путь только один, и будьте аккуратны в рассчетах!
# При неправильном использовании библиотеки decimal человек, играющий с вашим скриптом рискует никогда не найти путь.
#
# Также, при каждом ходе игрока ваш скрипт должен запоминать следущую информацию:
# - текущую локацию
# - текущее количество опыта
# - текущие дату и время (для этого используйте библиотеку datetime)
# После успешного или неуспешного завершения игры вам необходимо записать
# всю собранную информацию в csv файл dungeon.csv.
# Названия столбцов для csv файла: current_location, current_experience, current_date
#
#
# Пример взаимодействия с игроком:
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло времени: 00:00
#
# Внутри вы видите:
# — Вход в локацию: Location_1_tm1040
# — Вход в локацию: Location_2_tm123456
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали переход в локацию Location_2_tm1234567890
#
# Вы находитесь в Location_2_tm1234567890
# У вас 0 опыта и осталось 0.0987654321 секунд до наводнения
# Прошло времени: 20:00
#
# Внутри вы видите:
# — Монстра Mob_exp10_tm10
# — Вход в локацию: Location_3_tm55500
# — Вход в локацию: Location_4_tm66600
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали сражаться с монстром
#
# Вы находитесь в Location_2_tm0
# У вас 10 опыта и осталось -9.9012345679 секунд до наводнения
#
# Вы не успели открыть люк!!! НАВОДНЕНИЕ!!! Алярм!
#
# У вас темнеет в глазах... прощай, принцесса...
# Но что это?! Вы воскресли у входа в пещеру... Не зря матушка дала вам оберег :)
# Ну, на этот-то раз у вас все получится! Трепещите, монстры!
# Вы осторожно входите в пещеру... (текст умирания/воскрешения можно придумать свой ;)
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло уже 0:00:00
# Внутри вы видите:
#  ...
#  ...
#
# и так далее...
import json
import re
from abc import abstractmethod
from collections import OrderedDict
from copy import deepcopy
from decimal import Decimal

remaining_time = '123456.0987654321'
exp_required = 280
# если изначально не писать число в виде строки - теряется точность!
field_names = ['current_location', 'current_experience', 'current_date']


class Player:
    def __init__(self, location):
        self.experience = 0
        self.journey_time = Decimal(0)
        self.current_location = location

    def goto(self, location):
        self.current_location = location
        self.journey_time += Decimal(self.current_location.travel_time)

    def attack(self, npc):
        self.journey_time += Decimal(npc.fight_time)
        self.experience += int(npc.experience)


class Location:
    def __init__(self, location_dict):
        self.name = list(location_dict.keys())[0]
        self.is_exit = location_dict[self.name] == 'You are winner'
        if not self.is_exit:
            self.npcs = [NPC(element) for element in location_dict[self.name] if type(element) == str]
            self.locations = [Location(element) for element in location_dict[self.name] if type(element) == dict]
        self._travel_time = None

    @property
    def travel_time(self):
        if self._travel_time is None:
            self._travel_time = re.search(r'tm(?P<time>\d+\.?\d*)', self.name).group('time')
        return self._travel_time

    def __repr__(self):
        return self.name


class NPC:
    def __init__(self, name):
        self.name = name
        self._fight_time = None
        self._experience = None

    @property
    def fight_time(self):
        if self._fight_time is None:
            self._fight_time = re.search(r'tm(?P<time>\d+\.?\d*)', self.name).group('time')
        return self._fight_time

    @property
    def experience(self):
        if self._experience is None:
            self._experience = re.search(r'exp(?P<exp>\d+)', self.name).group('exp')
        return self._experience


class Game:
    def __init__(self, raw_location, target_exp, remaining_time):
        self.root_location = Location(raw_location)
        self.target_exp = target_exp
        self.remaining_time = Decimal(remaining_time)
        self.player = None
        self.state = None
        self.reset()

    def reset(self):
        self.player = Player(deepcopy(self.root_location))
        self.set_state(MainMenu)

    def check_victory(self):
        if not self.player.experience >= self.target_exp:
            print('\nВы оказались слишком слабы, чтобы открыть эту дверь.\n'
                  'Вам не хватило опыта. Тупик! И обратно дороги нет! Вы попали в западню.\n'
                  'Вода поднимается всё выше. Надежды нет...\n'
                  'У вас темнеет в глазах... прощай, принцесса...\n'
                  'Но что это?! Вы воскресли у входа в пещеру... Не зря матушка дала вам оберег :)\n'
                  'Ну, на этот-то раз у вас все получится! Трепещите, монстры!\n'
                  'Вы осторожно входите в пещеру...')
            return False

        if not self.player.journey_time <= self.remaining_time:
            print('\nВы не успели открыть люк!!! НАВОДНЕНИЕ!!! Алярм!\n'
                  'У вас темнеет в глазах... прощай, принцесса...\n'
                  'Но что это?! Вы воскресли у входа в пещеру... Не зря матушка дала вам оберег :)\n'
                  'Ну, на этот-то раз у вас все получится! Трепещите, монстры!\n'
                  'Вы осторожно входите в пещеру...')
            return False

        print("\nThanks Link, you're the hero of Hyrule.\n"
              "Finally, peace returns to Hyrule.\n"
              "This ends the story.\n\n"
              "You are great.\n"
              "You have an amazing wisdom and power.")
        return True

    def check_gameover(self):
        if self.player.journey_time > self.remaining_time:
            print('\nВы не успели открыть люк!!! НАВОДНЕНИЕ!!! Алярм!\n'
                  'У вас темнеет в глазах... прощай, принцесса...\n'
                  'Но что это?! Вы воскресли у входа в пещеру... Не зря матушка дала вам оберег :)\n'
                  'Ну, на этот-то раз у вас все получится! Трепещите, монстры!\n'
                  'Вы осторожно входите в пещеру...')
            return True
        if not self.player.current_location.locations:
            print('\nТупик! И обратно дороги нет! Вы попали в западню.\n'
                  'Вода поднимается всё выше. Надежды нет...\n'
                  'У вас темнеет в глазах... прощай, принцесса...\n'
                  'Но что это?! Вы воскресли у входа в пещеру... Не зря матушка дала вам оберег :)\n'
                  'Ну, на этот-то раз у вас все получится! Трепещите, монстры!\n'
                  'Вы осторожно входите в пещеру...')
            return True
        return False

    def set_state(self, state):
        self.state = state()
        self.state.context = self

    def run(self):
        while True:
            if self.player.current_location.is_exit:
                if self.check_victory():
                    break
                else:
                    self.reset()

            if self.check_gameover():
                self.reset()

            self.state.menu()


class Menu:
    def __init__(self):
        self.context = None
        self.avail_actions = None

    @abstractmethod
    def menu(self):
        pass

    def print_actions(self):
        for _, action in self.avail_actions.items():
            if action['enabled']:
                print(action['text'])

    def handle_input(self):
        while True:
            user_input = input('>: ')
            if user_input not in self.avail_actions.keys():
                print('Такое действие в данный момент недоступно. Попробуйте ещё раз:')
            else:
                break
        payload = self.avail_actions[user_input]['payload']
        args = self.avail_actions[user_input]['payload_args']
        payload(*args)


class MainMenu(Menu):
    def print_stats(self):
        print(f'\nВы находитесь в {self.context.player.current_location.name}\n'
              f'У вас {self.context.player.experience} опыта '
              f'и осталось {self.context.remaining_time - self.context.player.journey_time:f} секунд до наводнения.\n'
              f'Прошло времени: 00:00')

    def print_npcs(self):
        for npc in self.context.player.current_location.npcs:
            print(f'- Монстра {npc.name}')

    def print_locations(self):
        for location in self.context.player.current_location.locations:
            print(f'- Вход в локацию: {location}')

    def get_avail_actions(self):
        npcs = self.context.player.current_location.npcs
        locations = self.context.player.current_location.locations
        self.avail_actions = OrderedDict()
        self.avail_actions = {
            '1': {
                'text': '1. Атаковать',
                'enabled': True if npcs else False,
                'payload': self.context.set_state,
                'payload_args': [AttackMenu]
            },
            '2': {
                'text': '2. Перейти в другую локацию',
                'enabled': True if locations else False,
                'payload': self.context.set_state,
                'payload_args': [TravelMenu]
            },
            '3': {
                'text': '3. Сдаться и выйти из игры',
                'enabled': True,
                'payload': exit,
                'payload_args': []
            }
        }

    def menu(self):
        self.print_stats()
        print('Внутри вы видите:')
        self.print_npcs()
        self.print_locations()
        print('Выберите действие:')
        self.get_avail_actions()
        self.print_actions()
        self.handle_input()


class AttackMenu(Menu):
    def attack_handler(self, index):
        npcs = self.context.player.current_location.npcs
        self.context.player.attack(npcs.pop(index))
        self.context.set_state(MainMenu)

    def get_avail_actions(self):
        npcs = self.context.player.current_location.npcs
        self.avail_actions = OrderedDict()
        number = 0
        for npc in npcs:
            number += 1
            self.avail_actions.update({
                str(number): {
                    'text': f'{number}. {npc.name}',
                    'enabled': True,
                    'payload': self.attack_handler,
                    'payload_args': [number - 1]
                }
            })

        self.avail_actions.update({
            str(number + 1): {
                'text': f'{number + 1}. Назад',
                'enabled': True,
                'payload': self.context.set_state,
                'payload_args': [MainMenu]
            },
            str(number + 2): {
                'text': f'{number + 2}. Сдаться и выйти из игры',
                'enabled': True,
                'payload': exit,
                'payload_args': []
            }
        })

    def menu(self):
        self.get_avail_actions()
        print('\nКакого монстра атаковать?')
        self.print_actions()
        self.handle_input()


class TravelMenu(Menu):
    def travel_handler(self, location):
        self.context.player.goto(location)
        self.context.set_state(MainMenu)

    def get_avail_actions(self):
        locations = self.context.player.current_location.locations
        self.avail_actions = OrderedDict()
        number = 0
        for location in locations:
            number += 1
            self.avail_actions.update({
                str(number): {
                    'text': f'{number}. {location.name}',
                    'enabled': True,
                    'payload': self.travel_handler,
                    'payload_args': [location]
                }
            })

        self.avail_actions.update({
            str(number + 1): {
                'text': f'{number + 1}. Назад',
                'enabled': True,
                'payload': self.context.set_state,
                'payload_args': [MainMenu]
            },
            str(number + 2): {
                'text': f'{number + 2}. Сдаться и выйти из игры',
                'enabled': True,
                'payload': exit,
                'payload_args': []
            }
        })

    def menu(self):
        self.get_avail_actions()
        print('\nКуда вы хотите перейти:')
        self.print_actions()
        self.handle_input()

# TODO Старайтесь рабочий код оборачивать в if __name__ == '__main__'
# TODO при этом такого рабочего кода должно быть минимум
# TODO Представьте, что человек захочет импортировать ваше творение
# TODO С каждым новым действием, которое необходимо для запуска - его желание будет всё меньше
# TODO так что все начальные приготовление и сам главный цикл - стоит поместить внутрь класса

# TODO в данном случае про if __name__ == '__main__' просто забыл. Исправил)

# TODO Классы стараюсь писать так, чтобы для их инициализации и завода требовалось
#  минимум лишних действий.
#  В данном случае оборачивание циклом инициализации игрока и игры обусловлено
#  необходимостью сбрасывать игрока и игру при геймовере и запускать игру снова.
#  То есть, если бы при геймовере нужно было завершать игру, то цикла не было бы.


if __name__ == '__main__':
    with open('rpg.json', 'r') as level_file:
        location = json.load(level_file)

    game = Game(location, exp_required, remaining_time)
    game.run()

# Учитывая время и опыт, не забывайте о точности вычислений!
