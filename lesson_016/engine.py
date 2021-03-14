import calendar
from contextlib import contextmanager
import datetime as dt
from dataclasses import dataclass
import json
import locale
import os
import re
import sys
from tempfile import NamedTemporaryFile

from bs4 import BeautifulSoup
from dateutil import rrule
import cv2
import imgkit
import requests
from playhouse.db_url import connect

from assets import calendar_template as html_tmpl
from db_models import WeatherStats, db_proxy
import defaults
from assets import detailed_big_template as template


class BadResponseException(Exception):
    pass


class EmptyResponseException(Exception):
    pass


@dataclass
class Stats:
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
        return self.__dict__


class BlockPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


class WeatherMaker:

    def __init__(self, city):
        self.city, self.city_url = '', ''
        self.set_city(city)

    def set_city(self, city):
        response = requests.get(f'https://pogoda.mail.ru/ext/suggest/?q={city}')
        if response.status_code != 200:
            raise BadResponseException('Response status code is ' + str(response.status_code))
        response = json.loads(response.text)
        if not response:
            raise EmptyResponseException('Город не найден')
        self.city_url = response[0]['url']
        self.city = response[0]['name']

    def parse_month(self, date):
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
        weather_stats = []
        for month in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
            weather_stats.extend(self.parse_month(month))
        if not weather_stats:
            return []
        start_offset = (start_date - weather_stats[0].date).days if start_date > weather_stats[0].date else None
        end_offset = (end_date - weather_stats[-1].date).days if weather_stats[-1].date > end_date else None
        return weather_stats[start_offset:end_offset]


class ImageMaker:

    save_image = cv2.imwrite

    def __init__(self):
        self.font = cv2.freetype.createFreeType2()
        self.im_template = cv2.imread(template.BACKGROUND_IM)

    def get_image(self, stat):
        """
        Возвращает красивую картинку с прогнозом на день

        :param stat: объект типа Stats

        :return:  ndarray/cv2 image
        """
        im_color = cv2.applyColorMap(self.im_template, template.CMAPS[stat.descr])
        with setlocale(locale.LC_ALL, defaults.locale):
            for field in template.fields:
                params = dict(defaults.units, **stat.dict)
                params.update(weather_icon=template.ICONS[stat.descr])
                text = field['text'].format(**params)

                self.font.loadFontData(fontFileName=field['font'], id=0)

                if field.get('v_center', False):
                    (text_width, text_height), _ = self.font.getTextSize(text, field['font_size'], -1)
                else:
                    text_height = 0

                self.font.putText(img=im_color,
                                  text=text,
                                  org=(field['pos'][0], field['pos'][1] + text_height//2),
                                  fontHeight=field['font_size'],
                                  color=field['color'],
                                  thickness=-1, line_type=cv2.LINE_AA, bottomLeftOrigin=True)

        return im_color

    def get_calendar(self, stats):
        """
        Возвращает cv2 изображение календаря с прогнозом

        :param stats: список объектов класса Stats

        :return: ndarray/cv2 image
        """
        cal = CalendarMaker().formatrange(stats)

        # Изображение генерируется во временный файл, передаётся в cv2.imread и уничтожается
        tmp_file = NamedTemporaryFile(suffix='.png')
        with BlockPrints():
            imgkit.from_string(cal, tmp_file.name, options={'crop-w': '864'})
        img = cv2.imread(tmp_file.name)
        return img


class CalendarMaker(calendar.HTMLCalendar):
    def formatday(self, day, weekday, **kwargs):
        """
        Возвращает HTML код ячейки календаря

        :param day: день месяца
        :param weekday: день недели
        :param kwargs: в кваргах передаётся stats - список объектов класса Stats

        :return: str
        """
        stats = kwargs['stats']

        if day == 0 or not stats:
            return '<td class="noday">&nbsp;</td>' \
                   % {"weekday": self.cssclasses[weekday]}

        stat = next((stat for stat in stats
                     if stat.date == dt.date(kwargs['theyear'], kwargs['themonth'], day)),
                    None)
        if not stat:
            return '<td class="noday">&nbsp;</td>' \
                   % {"weekday": self.cssclasses[weekday]}

        params = dict(defaults.units, **stat.dict)
        params.update(day=day,
                      weekday=self.cssclasses[weekday],
                      weather_icon=template.ICONS[stat.descr])
        return html_tmpl.day.format(**params)

    def formatweek(self, theweek, **kwargs):
        """
        Возвращает HTML код недели из ячеек. Если в неделе только noday, то пустую строку

        :param theweek:
        :param kwargs: в кваргах передаётся stats - список объектов класса Stats

        :return: str
        """
        s = ''.join(self.formatday(d, wd, **kwargs) for (d, wd) in theweek)
        s = '<tr>%s</tr>' % s
        s = re.sub(r'<tr>(<td class="noday">&nbsp;<\/td>){7}<\/tr>', '', s)
        return s

    def formatmonth(self, theyear, themonth, withyear=True, **kwargs):
        """
        Возвращает готовый HTML код месяца. Если в кваргах нет дат этого месяца, то пустую строку

        :param theyear: номер года
        :param themonth: номер месяца
        :param withyear: флаг, писать ли в календаре год
        :param kwargs: в кваргах передаётся stats - список объектов класса Stats

        :return: str
        """
        stats = kwargs.get('stats', None)
        if not stats:
            return '<h1>&nbsp;&nbsp;Error. No weather stats&nbsp;&nbsp;</h1>'

        stat = next((stat for stat in stats
                     if (stat.date.year, stat.date.month) == (theyear, themonth)),
                    None)
        if not stat:
            return ''

        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % (
            self.cssclass_month))
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear, **kwargs))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, theyear=theyear, themonth=themonth, **kwargs))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def formatmonthname(self, theyear, themonth, withyear=True, **kwargs):
        """
        Возвращает html код заголовка календаря с месяцем, годом и городом

        :param theyear: номер года
        :param themonth: номер месяца
        :param withyear: флаг, писать ли в заголовке год
        :param kwargs: в кваргах передаётся stats - список объектов класса Stats, оттуда дёргается город

        :return: str
        """
        city = kwargs['stats'][0].city
        if withyear:
            s = '%s %s' % (defaults.month_name[themonth], theyear)
        else:
            s = '%s' % defaults.month_name[themonth]
        return html_tmpl.month_header.format(month=s, city=city)

    def formatrange(self, stats):
        """
        Возвращает html код календарей (один за другим) в диапазоне дат от самой меньшей в списке до самой большей

        :param stats: список объектов класса Stats

        :return: str
        """
        start_date = min(stats, key=lambda stat: stat.date).date
        end_date = max(stats, key=lambda stat: stat.date).date
        cal = html_tmpl.header + html_tmpl.css
        cal += '<div class="wrapper"><br>'
        for month in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
            with setlocale(locale.LC_ALL, 'ru_RU.UTF-8'):
                month = self.formatmonth(theyear=month.year, themonth=month.month, withyear=True, stats=stats)
                cal += month + '<br><br>' if month else ''
        cal = cal[:-4] + '</div>'
        cal += html_tmpl.footer
        return cal


class DatabaseUpdater:
    def __init__(self, db_url):
        db = connect(db_url)
        db_proxy.initialize(db)
        WeatherStats.create_table()

    def add_stats(self, stats):
        stats = [stats, ] if not isinstance(stats, list) else stats
        for stat in stats:
            _ = (WeatherStats
                 .insert(**stat.dict)
                 .on_conflict('replace')
                 .execute())

    def get_stats(self, city, start_date, end_date=None):
        if end_date:
            stats = WeatherStats.select().where(
                (WeatherStats.city == city) &
                (WeatherStats.date >= start_date) &
                (WeatherStats.date <= end_date)
            )
        else:
            stats = WeatherStats.get(
                (WeatherStats.city == city) &
                (start_date == WeatherStats.date)
            )
        return stats


@contextmanager
def setlocale(*args, **kw):
    current = locale.setlocale(locale.LC_ALL)
    yield locale.setlocale(*args, **kw)
    locale.setlocale(locale.LC_ALL, current)


def view_image(image, name_of_window):
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    cv2.imshow(name_of_window, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    start_date = dt.date(2021, 1, 5)
    end_date = dt.date(2021, 3, 31)
    weather = WeatherMaker('belgorod')
    stats = weather.get_range(start_date, end_date)
    image = ImageMaker().get_calendar(stats)
    view_image(image, ' ')
