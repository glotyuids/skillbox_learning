import datetime as dt
import json
import locale
import re
from contextlib import contextmanager
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup
from dateutil import rrule

import engine.defaults as defaults


class BadResponseException(Exception):
    pass


class EmptyResponseException(Exception):
    pass


@dataclass
class Stats:
    """ Датакласс для хранения прогноза за один день """
    city: str
    date: dt.date
    temp_day: int
    temp_night: int
    descr: str
    press: int
    humidity: int
    wind_speed: int
    wind_dir: str

    def __repr__(self):
        return f"{self.city}, {self.date.strftime('%d-%m-%y')}, " \
               f"{self.temp_day}/{self.temp_night}, {self.descr}"

    @property
    def dict(self):
        """ Возвращает поля с данными в виде словаря """
        return self.__dict__


class WeatherMaker:
    """ Парсер погоды с pogoda.mail.ru """
    def __init__(self, city):
        self.city, self.city_url = '', ''
        self.set_city(city)

    def set_city(self, city):
        """
        Ищет на сервере передныый город, и берёт из ответа корректное название города
        и url, по которому запрашивается погода

        :param city: str название города
        """
        response = requests.get(f'https://pogoda.mail.ru/ext/suggest/?q={city}')
        if response.status_code != 200:
            raise BadResponseException('Response status code is ' + str(response.status_code))
        response = json.loads(response.text)
        if not response:
            raise EmptyResponseException('Город не найден')
        self.city_url = response[0]['url']
        self.city = response[0]['name']

    def parse_month(self, date):
        """
        Парсит погоду за месяц

        :param date: datetime.date Дата, из которой берутся год и месяц

        :return: [Stats, ] список прогнозов погоды за месяц
        """
        month_name, year = date.strftime('%B').lower(), date.year
        response = requests.get(f'https://pogoda.mail.ru{self.city_url}{month_name}-{str(year)}/')
        if response.status_code != 200:
            return None

        html_doc = BeautifulSoup(response.text, features='html.parser')

        dates = html_doc.find_all('div', {'class': 'day__date'})
        dates = [re.search(r'\d{,2} \w+ \d{4}', date.text)[0] for date in dates]
        with setlocale(locale.LC_ALL, defaults.locale):
            dates = [dt.datetime.strptime(date, '%d %B %Y').date() for date in dates]

        temps = html_doc.find_all('div', {'class': 'day__temperature'})
        temps = [re.findall(r'(?:(-?\d+)°)', temp.text) for temp in temps]
        day_temps = [temp[0] for temp in temps]
        night_temps = [temp[1] for temp in temps]

        descriptions = html_doc.find_all('div', {'class': 'day__description'})
        descriptions = [descr.text.strip('\n') for descr in descriptions]

        pressures = html_doc.find_all('span', {'class': 'icon_preasure'})
        pressures = [press.parent.text for press in pressures]
        pressures = [re.search(r'(\d+) мм', press)[1] for press in pressures]

        humidities = html_doc.find_all('span', {'class': 'icon_humidity'})
        humidities = [humidity.parent.text for humidity in humidities]
        humidities = [re.search(r'(\d+)%', humidity)[1] for humidity in humidities]

        winds = html_doc.find_all('span', {'class': 'icon_wind'})
        winds = [wind.parent.attrs['title'] for wind in winds]
        winds = [re.search(r'(?P<speed>\d+) м/c (?P<dir>\S+)', wind) for wind in winds]
        wind_speeds = [wind['speed'] for wind in winds]
        wind_dirs = [wind['dir'] for wind in winds]

        days = []
        for day in zip([self.city]*len(dates), dates, day_temps, night_temps,
                       descriptions, pressures, humidities, wind_speeds, wind_dirs):
            days.append(Stats(*day))
        return days

    def get_range(self, start_date, end_date):
        """
        Парсит погоду за заданный период, включая обе даты

        :param start_date: datetime.date Первый день диапазона
        :param end_date: datetime.date Последний день диапазона

        :return: [Stats, ] список прогнозов погоды за период
        """
        weather_stats = []
        for month in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
            weather_stats.extend(self.parse_month(month))
        if not weather_stats:
            return []
        start_offset = (start_date - weather_stats[0].date).days if start_date > weather_stats[0].date else None
        end_offset = (end_date - weather_stats[-1].date).days if weather_stats[-1].date > end_date else None
        return weather_stats[start_offset:end_offset]


@contextmanager
def setlocale(*args, **kw):
    """ Контекстный менеджер для смены локали """
    current = locale.setlocale(locale.LC_ALL)
    yield locale.setlocale(*args, **kw)
    locale.setlocale(locale.LC_ALL, current)
