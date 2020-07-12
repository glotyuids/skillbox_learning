# -*- coding: utf-8 -*-


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru
import random
import string
import argparse

from PIL import Image, ImageFont, ImageDraw, ImageColor, features
from pdf417gen import encode
from pdf417gen import render_image as render_barcode
from transliterate import translit

from ticket_template_cp import template


class TTicket:
    data = {}

    def __init__(self, fio, from_, to, date, ticket_template):
        class_ = random.choice('FAJRDIWPYHKMLGVSNQOB')
        if class_ in 'FA':
            seat = random.choice('ABCDEF') + str(random.randint(1, 5))
        elif class_ in 'JRDIWP':
            seat = random.choice('ABCDEFGHI') + str(random.randint(6, 10))
        elif class_ in 'YHKMLGVSNQO':
            seat = random.choice('ABCDEFGHI') + str(random.randint(11, 41))
        else:
            seat = random.choice('BCDEFGH') + str(42)

        self.background = ticket_template.background
        self.image = None
        self.name = fio
        self.origin = from_
        self.dest = to
        self.date = date
        self.flight = 'AC ' + str(random.randint(1000, 9999))
        self.fare_code = class_
        self.seat = seat
        self.gate = random.choice('ABCDE') + str(random.randint(1, 99)).rjust(2, '0')
        self.brd_time = (str(random.randint(0, 23)).rjust(2, '0')
                         + ':' + str(random.choice(range(0, 60, 5))).rjust(2, '0'))

    def _get_data(self, data_type):
        if data_type in self.__dict__:
            return self.__dict__[data_type]
        return f'{data_type} is not defined'

    def _generate_barcode_data(self):
        barcode_data = 'M1'
        barcode_data += translit(self.name.replace(' ', '/'), 'ru', reversed=True).upper() + ' '
        barcode_data += 'E' + ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(0, 6)])
        barcode_data += ' ' + translit(self.origin, 'ru', reversed=True)[:3].upper()
        barcode_data += translit(self.dest, 'ru', reversed=True)[:3].upper()
        barcode_data += 'SU '
        barcode_data += self.flight[3:] + ' '
        barcode_data += '006' + self.fare_code + self.seat + ' '
        barcode_data += ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(0, 12)])
        barcode_data += self.seat
        return encode(barcode_data)

    def _generate_barcode(self):
        barcode_data = self._generate_barcode_data()
        barcode = render_barcode(barcode_data, padding=0)
        return barcode

    def generate(self):
        self.image = Image.open(template.background)
        canvas = ImageDraw.Draw(self.image)
        for field in template.fields:
            if field['data_type'] == 'barcode':
                barcode = self._generate_barcode()
                if field['rotate']:
                    barcode = barcode.transpose(field['rotate'])
                barcode = barcode.resize(field['size'])
                self.image.paste(barcode, field['pos'])
                continue
            font = ImageFont.truetype(field['font'], field['font_size'])
            field_width = field['width']
            text = self._get_data(field['data_type'])
            text = text.upper() if field['capital'] else text
            if field_width:
                while font.getsize(text)[0] > field_width:
                    text = text[:-1]
            canvas.text(field['pos'], text, font=font, fill=ImageColor.colormap['black'])


    def show(self):
        self.image.show()

    def save_to(self, file_name):
        self.image.save(file_name)


def make_ticket(fio, from_, to, date, filename=None):
    ticket = TTicket(fio, from_, to, date, template)
    ticket.generate()
    if filename:
        ticket.save_to(filename)
    else:
        ticket.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fio', action="store", dest="fio")
    parser.add_argument('--from', action="store", dest="from_")
    parser.add_argument('--to', action="store", dest="to")
    parser.add_argument('--date', action="store", dest="date")
    parser.add_argument('--save_to', action="store", dest="save_to", default=None)
    args = parser.parse_args()

    # make_ticket('Иванов И.И.', 'London Gatwick (LGW)', 'Naples International (NAP)', '15/02/2020')
    # make_ticket('Валько Дмитрий Олегович12345678901234567890', 'Белгород12345678901234567890', 'Москва12345678901234567890', '15/03/2020')
    make_ticket(args.fio, args.from_, args.to, args.date, args.save_to)

# Усложненное задание (делать по желанию).
# Написать консольный скрипт c помощью встроенного python-модуля argparse.
# Скрипт должен принимать параметры:
#   --fio - обязательный, фамилия.
#   --from - обязательный, откуда летим.
#   --to - обязательный, куда летим.
#   --date - обязательный, когда летим.
#   --save_to - необязательный, путь для сохранения заполненнего билета.
# и заполнять билет.
