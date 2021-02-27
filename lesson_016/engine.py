from dataclasses import dataclass
import datetime as dt
from bs4 import BeautifulSoup
import requests
import re


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
    @dataclass
    class Stats:
        date: dt.date
        temp_day: int
        temp_night: int
        temp_units: str = '°C'
        descr: str
        press: int
        press_units: str = 'мм'
        humidity: int
        humidity_units: str = '%'
        wind_speed: int
        wind_speed_units: str = 'м/с'
        wind_dir: str

    def __init__(self, city):
        self.city = city

    def parse_month(self, year, month):
        response = requests.get('https://pogoda.mail.ru/prognoz/belgorod/february-2009/')
        if response.status_code == 200:
            html_doc = BeautifulSoup(response.text, features='html.parser')
            dates = html_doc.find_all('div', {'class': 'day__date'})
            dates = [day.text for day in dates]

            temps = html_doc.find_all('div', {'class': 'day__temperature'})
            temps = [re.findall(r'(?:(-?\d+)°)', temp.text) for temp in temps]
            day_temps = [temp[0] for temp in temps]
            night_temps = [temp[1] for temp in temps]


            # list_of_names = html_doc.find_all('a', {'class': 'home-link home-link_black_yes inline-stocks__link'})

            # for names, values in zip(list_of_names, list_of_values):
            #     print(names.text, values.text)
