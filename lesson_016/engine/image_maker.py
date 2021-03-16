import datetime as dt
import calendar
import locale
import os
import re
import sys
from tempfile import NamedTemporaryFile
from contextlib import contextmanager

import cv2
import imgkit
from dateutil import rrule

import engine.defaults as defaults
from assets import calendar_template as html_tmpl
from assets import detailed_big_template as template


class BlockPrints:
    """ Контекстный менеджер для блокирования принтов в функциях """

    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


class ImageMaker:
    """ Генератор картинок """

    save_image = cv2.imwrite

    def __init__(self):
        self.font = cv2.freetype.createFreeType2()
        self.im_template = cv2.imread(template.BACKGROUND_IM)
        # не вижу, работаете ли вы с копией ниже, но было бы здорово изначально брать копию изображения
        # чтобы случайно нигде не сохранить правки в оригинал
        #  image_with_line = image_cv2.copy()
        # TODO По сути, копия здсь не нужна, поскольку, если я правильно всё понял,
        #  изображение находится в памяти не как файловый объект, а как массив numpy.ndarray,
        #  поэтому исходный файл в безопасности.
        #  Кроме того, шаблон сейчас используется только в одном месте,
        #  в методе, который применяет к изображению цветовую карту.
        #  Этот метод не изменяет исходный массив, а возвращает новый объект, с которым и ведётся работа,
        #  поэтому, опять же, исходное изображение в безопасности

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
                    (_, text_height), _ = self.font.getTextSize(text, field['font_size'], -1)
                else:
                    text_height = 0

                self.font.putText(img=im_color,
                                  text=text,
                                  org=(field['pos'][0], field['pos'][1] + text_height//2),
                                  fontHeight=field['font_size'],
                                  color=field['color'],
                                  thickness=-1, line_type=cv2.LINE_AA, bottomLeftOrigin=True)

        return im_color

    @staticmethod
    def get_calendar(stats):
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
    """ Генератор html-календаря с погодой """

    def formatday(self, day, weekday, **kwargs):
        """
        Возвращает HTML код ячейки календаря

        :param day: день месяца
        :param weekday: день недели
        :param kwargs: в кваргах передаётся stats - список объектов класса Stats

        :return: str Html код ячейки календаря с прогнозом
        """
        stats = kwargs['stats']

        if day == 0 or not stats:
            return '<td class="noday">&nbsp;</td>'

        stat = next((stat for stat in stats
                     if stat.date == dt.date(kwargs['theyear'], kwargs['themonth'], day)),
                    None)
        if not stat:
            return '<td class="noday">&nbsp;</td>'

        params = dict(defaults.units, **stat.dict)
        params.update(day=day,
                      weekday=self.cssclasses[weekday],
                      weather_icon=template.ICONS[stat.descr])
        return html_tmpl.day.format(**params)

    def formatweek(self, theweek, **kwargs):
        """
        Возвращает HTML код недели из ячеек. Если в неделе только noday, то пустую строку

        :param theweek: [(day, weekday), ] day - номер дня, weekday - номер дня недели
        :param kwargs: в кваргах передаётся stats - список объектов класса Stats

        :return: str Html код недели с прогнозом
        """
        # 's' - плохой пример нэйминга
        # TODO Тут и далее: я это понимаю.
        #  Но я наследовался от класса HTMLCalendar определённого во встроенной библиотеке calendar.
        #  Мне нужно было переопределить/поправить несколько методов класса,
        #  поэтому я эти методы просто скопировал в свой код и редактировал там, где это было необходимо.
        #  Остальное я просто не трогал, полностью рефакторить использованный код не стал
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

        :return: str Html код календаря на месяц с прогнозом
        """
        stats = kwargs.get('stats', None)
        if not stats:
            return '<h1>&nbsp;&nbsp;Error. No weather stats&nbsp;&nbsp;</h1>'

        stat = next((stat for stat in stats
                     if (stat.date.year, stat.date.month) == (theyear, themonth)),
                    None)
        if not stat:
            return ''
        # TODO v,a - тоже не очень хорошие примеры
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

        :return: str Html код заголовка календаря
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

        :return: str Полный html код страницы с набором календарей за заданный диапазон дат
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


@contextmanager
def setlocale(*args, **kw):
    """ Контекстный менеджер для смены локали """

    current = locale.setlocale(locale.LC_ALL)
    yield locale.setlocale(*args, **kw)
    locale.setlocale(locale.LC_ALL, current)


def view_image(image, name_of_window):
    """
    Выводит окно с изображением

    :param image: ndarray/cv2 image Изображение
    :param name_of_window: str Имя окна
    """
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    cv2.imshow(name_of_window, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
