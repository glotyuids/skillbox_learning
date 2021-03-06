"""
Здесь находятся все хендлеры-валидаторы для сценариев бота.
Все хендлеры должны принимать только текст и контекст (словарь) и возвращать только флаг валидности
"""
import re
from datetime import datetime

import skyscanner_api as skyapi

MAX_PASS_CAPACITY = 853     # столько пассажиров вмещает А380-800 - рекорд среди самолётов
re_date = re.compile(r'^(\d{2})-(\d{2})-(\d{4})$')
re_phone = re.compile(r'^(([7,8]|\+\d{1,3})[\-\s]?)(\(?\d{3}\)?[\-s]?)[\d\-\s]{7,10}$')


def handle_origin_city(text, context):
    city = skyapi.get_city(text.strip())
    if city:
        context['origin'] = city
        return 0
    return 1


def handle_dest_city(text, context):
    city = skyapi.get_city(text.strip())
    if city:
        context['dest'] = city
        return 0
    return 1


def handle_edit_origin_city(text, context):
    city = skyapi.get_city(text.strip())
    if city:
        context['origin'] = city
        ret_code = handle_arrival_date(context['flight'].arrival_date, context)
        if ret_code == 0:
            return 0
        return 2
    return 1


def handle_edit_dest_city(text, context):
    city = skyapi.get_city(text.strip())
    if city:
        context['dest'] = city
        ret_code = handle_arrival_date(context['flight'].arrival_date, context)
        if ret_code == 0:
            return 0
        return 2
    return 1


def reverse_date(date_str):
    components = date_str.split('-')
    return '-'.join(components[::-1])


def handle_arrival_date(text, context):
    match = re.match(re_date, text)
    if match:
        date = reverse_date(text)
        flight_dates = skyapi.get_dates(context['origin'], context['dest'], date)
        # если на выбранную дату рейс есть, то запоминаем его.
        # если рейсов нет, то подтягиваем рейсы за выбранный месяц и предлагаем пользователю даты после выбранной им
        if flight_dates:
            context['flight'] = skyapi.get_flight(context['origin'], context['dest'], flight_dates[0])
            return 0
        return check_next_dates(context, date)
    return 1


def check_next_dates(context, date):
    flight_dates = skyapi.get_dates(context['origin'], context['dest'], date[:7])
    if flight_dates:
        user_date = datetime.strptime(date, '%Y-%m-%d')
        flight_dates = [reverse_date(date) for date in flight_dates
                        if datetime.strptime(date, '%Y-%m-%d') > user_date]
        flight_dates = sorted(set(flight_dates))[:5]
        context['dates'] = '\n'.join(flight_dates)
        return 2
    return 3


def seats_handler(text, context):
    if not text.isdecimal():
        return 1
    if int(text) > MAX_PASS_CAPACITY:
        return 2
    if int(text) < 1:
        return 3
    context['seats'] = int(text)
    return 0


def comment_handler(text, context):
    if text == '-':
        context['comment'] = ''
    else:
        context['comment'] = text
    return 0


def verify_data_handler(text, context):
    if text.lower() == "далее":
        result = 0
    elif text.lower() == "вылет":
        result = 2
    elif text.lower() in ["прилёт", "прилет", ]:
        result = 3
    elif text.lower() == "дата":
        result = 4
    elif text.lower() == "места":
        result = 5
    elif text.lower() == "коммент":
        result = 6
    else:
        result = 1
    return result


def phone_handler(text, context):
    match = re.match(re_phone, text)
    if match:
        context['phone'] = text
        return 0
    return 1
