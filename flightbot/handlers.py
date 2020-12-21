"""
Здесь находятся все хендлеры-валидаторы для сценариев бота.
Все хендлеры должны принимать только текст и контекст (словарь) и возвращать только флаг валидности
"""
import re

import scenarios
from skyscanner_api import *

re_date = re.compile(r'^(\d{2})-(\d{2})-(\d{4})$')


def handle_origin_city(text, context):
    city = get_city(text.strip())
    if city:
        context['origin'] = city
        return 0
    return 1


def handle_dest_city(text, context):
    city = get_city(text.strip())
    if city:
        context['dest'] = city
        return 0
    return 1


def reverse_date(date_str):
    components = date_str.split('-')
    return '-'.join(components[::-1])


def handle_arrival_date(text, context):
    match = re.match(re_date, text)
    if match:
        date = reverse_date(text)
        flight_dates = get_dates(context['origin'], context['dest'], date)
        # если на выбранную дату рейс есть, то запоминаем его.
        # если рейсов нет, то подтягиваем рейсы за выбранный месяц и предлагаем пользователю даты после выбранной им
        if flight_dates:
            context['flight'] = get_flight(context['origin'], context['dest'], flight_dates[0])
            return 0
        else:
            return check_next_dates(context, date)
    return 1


def check_next_dates(context, date):
    flight_dates = get_dates(context['origin'], context['dest'], date[:7])
    if flight_dates:
        user_date = datetime.strptime(date, '%Y-%m-%d')
        flight_dates = [reverse_date(date) for date in flight_dates
                        if datetime.strptime(date, '%Y-%m-%d') > user_date]
        flight_dates = sorted(set(flight_dates))[:5]
        context['dates'] = '\n'.join(flight_dates)
        return 2
    return 3
