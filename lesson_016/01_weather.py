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

from abc import abstractmethod
import datetime as dt
import os
import re

from tabulate import tabulate

import engine


class UserInterface:
    """ Реализует необходимый функционал для работы консольного интерфейса """

    def __init__(self, db_url=None):
        self.wants_exit = False
        self.state = None
        self.weather = None
        self.get_weather()
        self.db = engine.DatabaseUpdater(db_url or 'sqlite:///weather.db')
        self.img_maker = engine.ImageMaker()
        self.start_date = dt.datetime.now().date() - dt.timedelta(days=6)
        self.end_date = dt.datetime.now().date()
        self.stats = None
        self.set_state(MainMenu)

    def set_state(self, state):
        """ Меняет своё состояние и контекст у меню """
        self.state = state()
        self.state.context = self

    def get_weather(self):
        """ Запрашивает у пользоваетеля город, ищет его на сервере и создаёт новый WeatherMaker """
        weather = None
        while not weather:
            city = input('Введите город: ')
            try:
                weather = engine.WeatherMaker(city)
            except engine.BadResponseException as exc:
                print(exc)
                print('Проверьте соединение с интернетом')
            except engine.EmptyResponseException as exc:
                print(f'{exc}. Попробуйте ещё раз')
        self.weather = weather

    def print_weather(self):
        """ Выводит на консоль таблицу с погодой за текущий период """
        data = [list(stat.dict.values()) for stat in self.stats]
        for stat in data:
            del stat[0]
        print(tabulate(data, tablefmt="pretty",
                       headers=['Дата', 'Дневная t', 'Ночная t', 'Погода',
                                'Давление', 'Влажность', 'Скорость ветра', 'Направление ветра']))

    def get_last_week(self):
        """
        Тянет из бд погоду за последнюю неделю
        (если нет, то сначала тащит с сервера и кидает в бд)
        и выводит её на консоль в виде таблицы
        """
        self.start_date = dt.datetime.now().date() - dt.timedelta(days=6)
        self.end_date = dt.datetime.now().date()
        self.stats = self.db.get_stats(city=self.weather.city,
                                       start_date=self.start_date,
                                       end_date=self.end_date)
        if len(self.stats) < 7:
            self.stats = self.weather.get_range(self.start_date, self.end_date)
            self.db.add_stats(self.stats)
        self.print_weather()

    def run(self):
        """ Запускает пользовательский интерфейс """
        self.get_last_week()
        while not self.wants_exit:
            self.state.menu()


class Menu:
    """ Базовый класс для меню """

    def __init__(self):
        self.context = None
        self.avail_actions = None

    def print_actions(self):
        """ Выводит на консоль список доступных действий """
        for _, action in self.avail_actions.items():
            print(action['text'])

    def handle_input(self):
        """ Обрабатывает пользовательский ввод в меню, запускает хендлеры """
        while True:
            user_input = input('>: ')
            if user_input not in self.avail_actions.keys():
                print('Неверная команда. Попробуйте ещё раз:')
            else:
                break
        payload = self.avail_actions[user_input]['payload']
        args = self.avail_actions[user_input]['payload_args']
        payload(*args)

    def set_dates(self):
        """ Запрашивает у пользователя диапазон дат и задаёт этот диапазон в контексте """
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

    @abstractmethod
    def menu(self):
        """ Выводит текущее меню и обрабатывает пользовательский ввод """

    def get_avail_actions(self):
        """ Здесь задаётся список доступных пунктов меню и их хендлеры """


class MainMenu(Menu):
    """ Главное меню """

    def get_new_city(self):
        """
        Запрашивает у пользователя город, задаёт его контексту
        и выводит прогноз за последнюю неделю на консоль
        """
        self.context.get_weather()
        self.context.get_last_week()

    def get_avail_actions(self):
        self.avail_actions = {
            '1': {
                'text': '1. Добавить прогнозы в базу данных',
                'payload': self.context.set_state,
                'payload_args': [AddToDBMenu]
            },
            '2': {
                'text': '2. Получить прогнозы из базы данных',
                'payload': self.context.set_state,
                'payload_args': [GetFromDBMenu]
            },
            '3': {
                'text': '3. Создать изображения из полученных прогнозов',
                'payload': self.context.set_state,
                'payload_args': [GetImagesMenu]
            },
            '4': {
                'text': '4. Вывести прогноз на консоль',
                'payload': self.context.print_weather,
                'payload_args': []
            },
            '5': {
                'text': '5. Изменить город',
                'payload': self.get_new_city,
                'payload_args': []
            },
            '6': {
                'text': '6. Выйти из программы',
                'payload': self.context.set_state,
                'payload_args': [ExitMenu]
            }
        }

    def menu(self):
        print(f'\nТекущий город: {self.context.weather.city}')
        print(f'Текущий диапазон: {self.context.stats[0].date.strftime("%d-%m-%Y")} - '
              f'{self.context.stats[-1].date.strftime("%d-%m-%Y")}')
        print('Выберите действие:')
        self.get_avail_actions()
        self.print_actions()
        self.handle_input()


class ExitMenu(Menu):
    """ Меню выхода из программы """

    def exit_handler(self):
        """ Хендлер выхода из программы"""
        self.context.wants_exit = True

    def get_avail_actions(self):
        self.avail_actions = {
            '1': {
                'text': '1. Нет, вернуться назад',
                'payload': self.context.set_state,
                'payload_args': [MainMenu]
            },
            '2': {
                'text': '2. Да, выйти из программы',
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
    """ Меню добавления данных в бд """

    def menu(self):
        """
        Запрашивает у пользователя диапазон дат,
        тянет с сервера погоду за этот диапазон и заливает её в бд
        """
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
        context.db.add_stats(stats)
        context.set_state(MainMenu)


class GetFromDBMenu(Menu):
    """ Меню запроса данных из бд """

    def menu(self):
        """
        Запрашивает у пользователя диапазон дат, тянет из бд погоду за этот диапазон.
        Если погоды нет - ругается и просит выбрать другой диапазон
        """
        context = self.context
        print('\nВведите дату, либо диапазон дат через косую черту')
        print('в формате дд-мм-гггг/дд-мм-гггг, '
              'либо введите "назад" для возвращения в главное меню')
        stats = []
        while not stats:
            result = self.set_dates()
            if not result:
                continue

            stats = context.db.get_stats(context.weather.city,
                                         context.start_date,
                                         context.end_date)
            if not stats:
                print('Погода в данном диапазоне дат в базе данных не найдена.\n'
                      'Попробуйте ещё раз')
        context.stats = stats
        self.context.start_date = min([stat.date for stat in stats])
        self.context.end_date = max([stat.date for stat in stats])
        context.set_state(MainMenu)


class GetImagesMenu(Menu):
    """ Меню генерации картинок """

    def create_cards(self):
        """
        Спрашивает у пользователя место для сохранения
        и сохраняет погоду в отдельные карточки для каждого дня.
        При пустом вводе сохраняет в папку cards рядом со скриптом
        """
        print('\nКуда будем сохранять изображения? '
              'Введите путь, либо оставьте пустым, чтобы сохранить в папку cards рядом со скриптом')
        user_input = input('>: ')
        if not user_input:
            path = os.path.join(os.getcwd(), 'cards')
        else:
            path = os.path.normpath(user_input)
        os.makedirs(path, exist_ok=True)

        context = self.context
        for stat in context.stats:
            img = context.img_maker.get_image(stat)
            full_name = os.path.join(path, str(stat.date) + '.png')
            context.img_maker.save_image(full_name, img)
        print(f'Все изображения сохранены в {path}')

    def create_calendar(self):
        """
        Спрашивает у пользователя место для сохранения
        и сохраняет погоду в картинку - общий календарь.
        При пустом вводе сохраняет в папку рядом со скриптом
        """
        print('\nКуда будем сохранять изображения? '
              'Введите путь, либо оставьте пустым, чтобы сохранить в папку рядом со скриптом')
        user_input = input('>: ')
        if not user_input:
            path = os.getcwd()
        else:
            path = os.path.normpath(user_input)
        os.makedirs(path, exist_ok=True)

        context = self.context
        start_date = context.start_date
        end_date = context.end_date

        img = context.img_maker.get_calendar(context.stats)
        start_year = '' if start_date.year == end_date.year else f'-{start_date.year}'
        start_month = '' if not start_year and start_date.month == end_date.month else f'-{start_date.month}'
        file_name = context.weather.city + ' '
        file_name += f'{context.start_date.day}{start_month}{start_year} - '
        file_name += context.end_date.strftime("%d-%m-%Y")

        full_name = os.path.join(path, f'{file_name}.png')
        context.img_maker.save_image(full_name, img)
        print(f'Календарь сохранён в {full_name}')

    def get_avail_actions(self):
        self.avail_actions = {
            '1': {
                'text': '1. Создать отдельные карточки для каждого дня',
                'payload': self.create_cards,
                'payload_args': []
            },
            '2': {
                'text': '2. Создать календарь для выбранного диапазона',
                'payload': self.create_calendar,
                'payload_args': []
            },
            '3': {
                'text': '3. Вернуться в главное меню',
                'payload': self.context.set_state,
                'payload_args': [MainMenu]
            }
        }

    def menu(self):
        self.get_avail_actions()
        print()
        self.print_actions()
        self.handle_input()


if __name__ == '__main__':
    interface = UserInterface()
    interface.run()
