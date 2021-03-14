# -*- coding: utf-8 -*-

# В очередной спешке, проверив приложение с прогнозом погоды, вы выбежали
# навстречу ревью вашего кода, которое ожидало вас в офисе.
# И тут же день стал хуже - вместо обещанной облачности вас встретил ливень.

# Вы промокли, настроение было испорчено, и на ревью вы уже пришли не в духе.
# В итоге такого сокрушительного дня вы решили написать свою программу для прогноза погоды
# из источника, которому вы доверяете.

# Для этого вам нужно:

# Создать модуль-движок с классом WeatherMaker, необходимым для получения и формирования предсказаний.
# В нём должен быть метод, получающий прогноз с выбранного вами сайта (парсинг + re) за некоторый диапазон дат,
# а затем, получив данные, сформировать их в словарь {погода: Облачная, температура: 10, дата:datetime...}

# Добавить класс ImageMaker.
# Снабдить его методом рисования открытки
# (использовать OpenCV, в качестве заготовки брать lesson_016/python_snippets/external_data/probe.jpg):
#   С текстом, состоящим из полученных данных (пригодится cv2.putText)
#   С изображением, соответствующим типу погоды
# (хранятся в lesson_016/python_snippets/external_data/weather_img ,но можно нарисовать/добавить свои)
#   В качестве фона добавить градиент цвета, отражающего тип погоды
# Солнечно - от желтого к белому
# Дождь - от синего к белому
# Снег - от голубого к белому
# Облачно - от серого к белому

# Добавить класс DatabaseUpdater с методами:
#   Получающим данные из базы данных за указанный диапазон дат.
#   Сохраняющим прогнозы в базу данных (использовать peewee)

# Сделать программу с консольным интерфейсом, постаравшись все выполняемые действия вынести в отдельные функции.
# Среди действий, доступных пользователю, должны быть:
#   Добавление прогнозов за диапазон дат в базу данных
#   Получение прогнозов за диапазон дат из базы
#   Создание открыток из полученных прогнозов
#   Выведение полученных прогнозов на консоль
# При старте консольная утилита должна загружать прогнозы за прошедшую неделю.

# Рекомендации:
# Можно создать отдельный модуль для инициализирования базы данных.
# Как далее использовать эту базу данных в движке:
# Передавать DatabaseUpdater url-путь
# https://peewee.readthedocs.io/en/latest/peewee/playhouse.html#db-url
# Приконнектится по полученному url-пути к базе данных
# Инициализировать её через DatabaseProxy()
# https://peewee.readthedocs.io/en/latest/peewee/database.html#dynamically-defining-a-database
import re
from abc import abstractmethod
import datetime as dt

from tabulate import tabulate

import engine


class Utility:
    def __init__(self, db_url=None):
        self.wants_exit = False
        self.state = None
        self.weather = self.get_weather()
        self.db = engine.DatabaseUpdater(db_url or 'sqlite:///weather.db')
        self.start_date = dt.datetime.now().date() - dt.timedelta(days=7)
        self.end_date = dt.datetime.now().date()
        self.stats = None
        self.set_state(MainMenu)

    def set_state(self, state):
        self.state = state()
        self.state.context = self

    def get_weather(self):
        weather = None
        while not weather:
            city = input('Введите ваш город: ')
            try:
                weather = engine.WeatherMaker(city)
            except engine.BadResponseException as exc:
                print(exc)
                print('Проверьте соединение с интернетом')
            except engine.EmptyResponseException as exc:
                print(f'{exc}. Попробуйте ещё раз')
        return weather

    def print_weather(self):
        data = [list(stat.dict.values()) for stat in self.stats]
        for stat in data:
            del stat[0]
        print(tabulate(data, tablefmt="pretty",
                       headers=['Дата', 'Дневная t', 'Ночная t', 'Погода',
                                'Давление', 'Влажность', 'Скорость ветра', 'Направление ветра']))

    def run(self):
        self.stats = self.db.get_stats(city=self.weather.city,
                                       start_date=self.start_date,
                                       end_date=self.end_date)
        if len(self.stats) < 7:
            self.stats = self.weather.get_range(self.start_date, self.end_date)
            self.db.add_stats(self.stats)
        self.print_weather()
        while not self.wants_exit:
            self.state.menu()


class Menu:
    def __init__(self):
        self.context = None
        self.avail_actions = None

    def print_actions(self):
        for _, action in self.avail_actions.items():
            print(action['text'])

    def handle_input(self):
        while True:
            user_input = input('>: ')
            if user_input not in self.avail_actions.keys():
                print('Неверная команда. Попробуйте ещё раз:')
            else:
                break
        payload = self.avail_actions[user_input]['payload']
        args = self.avail_actions[user_input]['payload_args']
        payload(*args)

    @abstractmethod
    def menu(self):
        pass


class MainMenu(Menu):
    def get_avail_actions(self):
        self.avail_actions = {
            '1': {
                'text': '1. Добавить прогнозы в базу данных',
                'payload': self.context.set_state,
                'payload_args': [AddToDBMenu]
            },
            # '2': {
            #     'text': '2. Получить прогнозы из базы данных',
            #     'payload': self.context.set_state,
            #     'payload_args': [GetFromDBMenu]
            # },
            # '3': {
            #     'text': '3. Создать изображения из полученных прогнозов',
            #     'payload': self.context.set_state,
            #     'payload_args': [GetImagesMenu]
            # },
            '4': {
                'text': '4. Вывести прогноз на консоль',
                'payload': self.context.print_weather,
                'payload_args': []
            },
            '5': {
                'text': '5. Выйти из программы',
                'payload': self.context.set_state,
                'payload_args': [ExitMenu]
            }
        }


    def menu(self):
        print(f'\nТекущий диапазон: {self.context.stats[0].date.strftime("%d-%m-%Y")} - '
              f'{self.context.stats[-1].date.strftime("%d-%m-%Y")}')
        print('Выберите действие:')
        self.get_avail_actions()
        self.print_actions()
        self.handle_input()


class ExitMenu(Menu):
    def exit_handler(self):
        self.context.wants_exit = True

    def get_avail_actions(self):
        self.avail_actions = {
            '1': {
                'text': '1. Нет, вернуться назад',
                'enabled': True,
                'payload': self.context.set_state,
                'payload_args': [MainMenu]
            },
            '2': {
                'text': '2. Да, выйти из программы',
                'enabled': True,
                'payload': self.exit_handler,
                'payload_args': []
            }
        }

    def menu(self):
        self.get_avail_actions()
        print('\nВы уверены?')
        self.print_actions()
        self.handle_input()


class AddToDBMenu(Menu):
    def set_dates(self):
        while True:
            user_input = input('>: ')
            if user_input.lower() == 'назад':
                return False
            mtch = re.match(r'^(\d{1,2}-\d{1,2}-\d{4})(/(\d{1,2}-\d{1,2}-\d{4}))?$', user_input)
            if not mtch:
                print('Ошибка в дате. Попробуйте ещё раз')
                continue

            dates = user_input.split('/')
            try:
                dates = [dt.datetime.strptime(date, '%d-%m-%Y').date() for date in dates]
            except ValueError:
                print('Ошибка в дате. Попробуйте ещё раз')
                continue

            self.context.start_date = min(dates)
            self.context.end_date = max(dates)
            return True

    def menu(self):
        context = self.context
        print('\nВведите дату, либо диапазон дат через косую черту')
        print('в формате дд-мм-гггг/дд-мм-гггг, '
              'либо введите "назад" для возвращения в главное меню')
        stats = []
        while not stats:
            result = self.set_dates()
            if not result:
                continue

            stats = context.weather.get_range(context.start_date, context.end_date)
            if not stats:
                print('Погода в данном диапазоне дат на сервере не найдена.\n'
                      'Попробуйте ещё раз')
        context.stats = stats
        context.set_state(MainMenu)


if __name__ == '__main__':
    util = Utility()
    util.run()


