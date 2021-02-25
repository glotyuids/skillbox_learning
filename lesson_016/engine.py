from dataclasses import dataclass
import datetime as dt
import beautifulsoup4

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
        pass