# -*- coding: utf-8 -*-


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru
import random
import string

from PIL import Image, ImageFont, ImageDraw, ImageColor
from ticket_template_cp import template


class TTicket:
    def __init__(self, fio, from_, to, date, ticket_template):
        self.full_name = fio
        self.from_ = from_
        self.to = to
        self.date = date
        self.class_ = random.choice('FAJRDIWPYHKMLGVSNQOB')
        if self.class_ in 'FA':
            self.seat = random.choice('ABCDEF') + str(random.randint(1, 5))
        elif self.class_ in 'JRDIWP':
            self.seat = random.choice('ABCDEFGHI') + str(random.randint(6, 10))
        elif self.class_ in 'YHKMLGVSNQO':
            self.seat = random.choice('ABCDEFGHI') + str(random.randint(11, 41))
        else:
            self.seat = random.choice('BCDEFGH') + str(42)

        self.background = ticket_template.background
        self.image = None
        self.data = {
            'name': self.full_name,
            'from': self.from_,
            'to': self.to,
            'date': self.date,
            'flight': (random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase)
                       + ' ' + str(random.randint(1000, 9999))),
            'class': self.class_,
            'seat': self.seat,
            'gate': random.choice('ABCDE') + str(random.randint(1, 99)).rjust(2, '0'),
            'brd_time': (str(random.randint(0, 23)).rjust(2, '0')
                         + ':' + str(random.choice(range(0, 60, 5))).rjust(2, '0')),
        }

    def _get_data(self, data_type):
        if data_type in self.data:
            return self.data[data_type]
        return f'{data_type} is not defined'

    def generate(self):
        self.image = Image.open(template.background)
        canvas = ImageDraw.Draw(self.image)
        for field in template.fields:
            if field['data_type'] == 'barcode':
                continue

            font = ImageFont.truetype(field['font'], field['font_size'])
            max_length = field['max_length']
            text = self._get_data(field['data_type'])
            text = text[:max_length]
            text = text.upper() if field['capital'] else text
            canvas.text(field['pos'], text, font=font, fill=ImageColor.colormap['black'])

    def show(self):
        self.image.show()

    def save_to(self, file_name):
        pass


def make_ticket(fio, from_, to, date):
    ticket = TTicket(fio, from_, to, date, template)
    ticket.generate()
    ticket.show()
    ticket.save_to('new_ticket.png')


if __name__ == '__main__':
    make_ticket('Иванов И.И.', 'London Gatwick (LGW)', 'Naples International (NAP)', '15/02/2020')

# Усложненное задание (делать по желанию).
# Написать консольный скрипт c помощью встроенного python-модуля argparse.
# Скрипт должен принимать параметры:
#   --fio - обязательный, фамилия.
#   --from - обязательный, откуда летим.
#   --to - обязательный, куда летим.
#   --date - обязательный, когда летим.
#   --save_to - необязательный, путь для сохранения заполненнего билета.
# и заполнять билет.
