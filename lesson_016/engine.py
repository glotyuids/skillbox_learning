from dataclasses import dataclass
import datetime as dt
from bs4 import BeautifulSoup
import requests
import re
import locale
from contextlib import contextmanager


@dataclass
class Stats:
    date: dt.date
    temp_day: int
    temp_night: int
    descr: str
    press: int
    humidity: int
    wind_speed: int
    wind_dir: str
    temp_units: str = '°C'
    press_units: str = 'мм'
    humidity_units: str = '%'
    wind_speed_units: str = 'м/с'

    def __repr__(self):
        return f"{self.date.strftime('%d-%m-%y')}, {self.temp_day}/{self.temp_night}{self.temp_units}, {self.descr}"


class WeatherMaker:

    @staticmethod
    @contextmanager
    def setlocale(*args, **kw):
        current = locale.setlocale(locale.LC_ALL)
        yield locale.setlocale(*args, **kw)
        locale.setlocale(locale.LC_ALL, current)

    def __init__(self, city):
        self.city = city

    def parse_month(self, year, month):
        month_name = dt.date(2001, month, 1).strftime('%B').lower()
        response = requests.get(f'https://pogoda.mail.ru/prognoz/{self.city}/{month_name}-{str(year)}/')
        if response.status_code != 200:
            return None

        html_doc = BeautifulSoup(response.text, features='html.parser')
        dates = html_doc.find_all('div', {'class': 'day__date'})
        dates = [re.search(r'\d{,2} \w+ \d{4}', date.text)[0] for date in dates]
        with self.setlocale(locale.LC_ALL, 'ru_RU.UTF-8'):
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
        for day in zip(dates, day_temps, night_temps, descriptions, pressures, humidities, wind_speeds, wind_dirs):
            days.append(Stats(*day))

        return days
