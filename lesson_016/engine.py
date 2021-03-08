import calendar
from contextlib import contextmanager
import datetime as dt
from dataclasses import dataclass
import locale
import re
from tempfile import NamedTemporaryFile

from bs4 import BeautifulSoup
from dateutil import rrule
import cv2
import requests

from assets import detailed_big_template as template


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
    temp_units: str = '°'
    press_units: str = 'мм'
    humidity_units: str = '%'
    wind_speed_units: str = 'м/с'

    def __repr__(self):
        return f"{self.city}, {self.date.strftime('%d-%m-%y')}, " \
               f"{self.temp_day}/{self.temp_night}{self.temp_units}, {self.descr}"

    @property
    def dict(self):
        return self.__dict__


class WeatherMaker:

    def __init__(self, city):
        self.city = city

    def parse_month(self, date):
        month_name, year = date.strftime('%B').lower(), date.year
        response = requests.get(f'https://pogoda.mail.ru/prognoz/{self.city}/{month_name}-{str(year)}/')
        if response.status_code != 200:
            return None

        html_doc = BeautifulSoup(response.text, features='html.parser')

        city = re.search(r"name: 'citiesDropdown',\W+text: '(.+)',", response.text)[1]

        dates = html_doc.find_all('div', {'class': 'day__date'})
        dates = [re.search(r'\d{,2} \w+ \d{4}', date.text)[0] for date in dates]
        with setlocale(locale.LC_ALL, 'ru_RU.UTF-8'):
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
        for day in zip([city]*len(dates), dates, day_temps, night_temps,
                       descriptions, pressures, humidities, wind_speeds, wind_dirs):
            days.append(Stats(*day))
        return days

    def get_range(self, start_date, end_date):
        weather_stats = []
        for month in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
            weather_stats.extend(self.parse_month(month))
        start_offset = (start_date - weather_stats[0].date).days if start_date > weather_stats[0].date else None
        end_offset = (end_date - weather_stats[-1].date).days if weather_stats[-1].date > end_date else None
        return weather_stats[start_offset:end_offset]


class ImageMaker:

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
        with setlocale(locale.LC_ALL, 'ru_RU.UTF-8'):
            for field in template.fields:
                text = field['text'].format(weather_icon=template.ICONS[stat.descr], **stat.dict)
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
        imgkit.from_string(cal, tmp_file.name, options={'crop-w': '864'})
        img = cv2.imread(tmp_file.name)
        return img


class CalendarMaker(calendar.HTMLCalendar):
    month_name = {          # в локали месяцы лежат в родительном падеже, а мне нужен именительный
        1: 'январь',
        2: 'февраль',
        3: 'март',
        4: 'апрель',
        5: 'май',
        6: 'июнь',
        7: 'июль',
        8: 'август',
        9: 'сентябрь',
        10: 'октябрь',
        11: 'ноябрь',
        12: 'декабрь',
    }
    header = """
    <html>
      <head>
        <meta charset="utf-8">
      </head>

      <body>

      """
    footer = """
      </body>
    </html>
    """
    css = """

    <style type="text/css">
      @import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;500&display=swap');

      # @font-face {
      #   font-family: 'Weather Icons';
      #   src: url('assets/weathericons-regular-webfont.woff') format('woff'),
      #   url('assets/weathericons-regular-webfont.ttf') format('truetype');
      # }

      @font-face {
      font-family: 'Weather Icons'; 
      url('https://erikflowers.github.io/weather-icons/font/weathericons-regular-webfont.woff') format('woff'), 
      url('https://erikflowers.github.io/weather-icons/font/weathericons-regular-webfont.ttf') format('truetype'), 
      font-weight: normal;
      font-style: normal;
    }

      body {
        color: rgb(51, 51, 51);
        font-family: "Roboto Slab";
        width: 857px;
      }

      .wrapper {
        width: 857px;
      }

      table {
        border-collapse: collapse;
      }

      .month_name {
        font-size: 30;
        text-align: left;
        padding-left: 12;
        padding-bottom: 6;
      }
      th.city {
        font-size: 30;
        text-align: right;
         padding-right: 12;
        padding-bottom: 6;
      }

      tr:nth-child(2) {
        line-height: 1.5;
        font-size: 20;
      }

      .noday {
        height: 142px;
        width: 120px;
      }

      .day {
        height: 142px;
        width: 120px;
        border: 1px solid rgb(51, 51, 51);
      }    

      .sat > .date,  .sun > .date, th.sat, th.sun { 
        color: #ff4949;
      }

      .sun.day, .sat.day { 
        border-color: #ff4949;
      }

      .fri {
        border-right-width: 0;
      }

      .fri + .noday {
        border-left: 1px solid rgb(51 51 51);
      }

      .date {
        margin-top: -10px;
        padding-right: 10px;
        font-size: 24px;
        line-height: 1.528;
        text-align: right;
      }

      .icon {
        padding-top: 10px;
        font-size: 34px;
        font-family: "Weather Icons";
        line-height: 0.809;
        text-align: center;
      }

      .descr {
        font-size: 14.667px;
        line-height: 2.5;
        text-align: center;
      }

      .temp {
        font-size: 20px;
        line-height: 1.2;
        text-align: center;
        left: 17.625px;
        top: 102.17px;
        z-index: 4;
      }

    </style>
    """

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

        return """  <td class="{weekday} day">
                      <div class="date">{day}</div>
                      <div class="icon">{weather_icon}</div>
                      <div class="descr">{descr}</div>
                      <div class="temp">{temp_day}°  {temp_night}°</div>
          </td>""".format(weekday=self.cssclasses[weekday], day=day,
                          weather_icon=template.ICONS[stat.descr],
                          **stat.dict)

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
        Возвращает готовый HTML код месяца

        :param theyear: номер года
        :param themonth: номер месяца
        :param withyear: флаг, писать ли в календаре год
        :param kwargs: в кваргах передаётся stats - список объектов класса Stats

        :return: str
        """
        stats = kwargs.get('stats', None)
        if not stats:
            return '<h1>&nbsp;&nbsp;Error. No weather stats&nbsp;&nbsp;</h1>'

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
            s = '%s %s' % (self.month_name[themonth], theyear)
        else:
            s = '%s' % self.month_name[themonth]
        return '<tr><th colspan="3" class="month_name">{month}</th>' \
               '<th colspan="4" class="city">{city}</th></tr>'.format(month=s, city=city)

    def formatrange(self, stats):
        """
        Возвращает html код календарей (один за другим) в диапазоне дат от в stats[0] до stats[-1]

        :param stats: список объектов класса Stats

        :return: str
        """
        start_date = stats[0].date
        end_date = stats[-1].date
        cal = self.header + self.css
        cal += '<div class="wrapper"><br>'
        for month in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
            with setlocale(locale.LC_ALL, 'ru_RU.UTF-8'):
                cal += self.formatmonth(theyear=month.year, themonth=month.month, withyear=True, stats=stats)
                cal += '<br><br>'
        cal = cal[:-4] + '</div>'
        cal += self.footer
        return cal


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
