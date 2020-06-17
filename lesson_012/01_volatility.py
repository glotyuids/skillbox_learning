# -*- coding: utf-8 -*-


# Описание предметной области:
#
# При торгах на бирже совершаются сделки - один купил, второй продал.
# Покупают и продают ценные бумаги (акции, облигации, фьючерсы, етс). Ценные бумаги - это по сути долговые расписки.
# Ценные бумаги выпускаются партиями, от десятка до несколько миллионов штук.
# Каждая такая партия (выпуск) имеет свой торговый код на бирже - тикер - https://goo.gl/MJQ5Lq
# Все бумаги из этой партии (выпуска) одинаковы в цене, поэтому говорят о цене одной бумаги.
# У разных выпусков бумаг - разные цены, которые могут отличаться в сотни и тысячи раз.
# Каждая биржевая сделка характеризуется:
#   тикер ценнной бумаги
#   время сделки
#   цена сделки
#   обьем сделки (сколько ценных бумаг было куплено)
#
# В ходе торгов цены сделок могут со временем расти и понижаться. Величина изменения цен называтея волатильностью.
# Например, если бумага №1 торговалась с ценами 11, 11, 12, 11, 12, 11, 11, 11 - то она мало волатильна.
# А если у бумаги №2 цены сделок были: 20, 15, 23, 56, 100, 50, 3, 10 - то такая бумага имеет большую волатильность.
# Волатильность можно считать разными способами, мы будем считать сильно упрощенным способом -
# отклонение в процентах от полусуммы крайних значений цены за торговую сессию:
#   полусумма = (максимальная цена + минимальная цена) / 2
#   волатильность = ((максимальная цена - минимальная цена) / полусумма) * 100%
# Например для бумаги №1:
#   half_sum = (12 + 11) / 2 = 11.5
#   volatility = ((12 - 11) / half_sum) * 100 = 8.7%
# Для бумаги №2:
#   half_sum = (100 + 3) / 2 = 51.5
#   volatility = ((100 - 3) / half_sum) * 100 = 188.34%
#
# В реальности волатильность рассчитывается так: https://goo.gl/VJNmmY
#
# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью.
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
#
# Подготовка исходных данных
# 1. Скачать файл https://drive.google.com/file/d/1l5sia-9c-t91iIPiGyBc1s9mQ8RgTNqb/view?usp=sharing
#       (обратите внимание на значок скачивания в правом верхнем углу,
#       см https://drive.google.com/file/d/1M6mW1jI2RdZhdSCEmlbFi5eoAXOR3u6G/view?usp=sharing)
# 2. Раззиповать средствами операционной системы содержимое архива
#       в папку python_base/lesson_012/trades
# 3. В каждом файле в папке trades содержится данные по сделакам по одному тикеру, разделенные запятыми.
#   Первая строка - название колонок:
#       SECID - тикер
#       TRADETIME - время сделки
#       PRICE - цена сделки
#       QUANTITY - количество бумаг в этой сделке
#   Все последующие строки в файле - данные о сделках
#
# Подсказка: нужно последовательно открывать каждый файл, вычитывать данные, высчитывать волатильность и запоминать.
# Вывод на консоль можно сделать только после обработки всех файлов.
#
# Для плавного перехода к мультипоточности, код оформить в обьектном стиле, используя следующий каркас
#
# class <Название класса>:
#
#     def __init__(self, <параметры>):
#         <сохранение параметров>
#
#     def run(self):
#         <обработка данных>

import os
import csv

TRADES_DIR = 'trades'


class TTradeAnalyzer:
    def __init__(self, ticker_filename):
        self.ticker_filename = ticker_filename
        self.volatility = None
        with open(self.ticker_filename) as ticker_file:
            trades = csv.DictReader(ticker_file)
            self.ticker_name = next(trades)['SECID']

    def run(self):
        with open(self.ticker_filename) as ticker_file:
            trades = csv.DictReader(ticker_file)
            price = float(next(trades)['PRICE'])
            min_price, max_price = price, price
            for trade in trades:
                price = float(trade['PRICE'])
                min_price = price if price < min_price else min_price
                max_price = price if price > max_price else max_price
            half_sum = (max_price + min_price) / 2
            self.volatility = ((max_price - min_price) / half_sum) * 100


# Обработка файлов
trades_list = [os.path.join(TRADES_DIR, ticker) for ticker in os.listdir(TRADES_DIR)]
trades_list = [ticker for ticker in trades_list if os.path.isfile(ticker)]
volatility_list = []
for ticker in trades_list:
    trade_analyzer = TTradeAnalyzer(ticker)
    trade_analyzer.run()
    volatility_list.append({'name': trade_analyzer.ticker_name, 'volatility': trade_analyzer.volatility})

# Извлечение необходимых данных из результатов обработки
volatility_list.sort(key=lambda x: x['volatility'], reverse=True)
max_volat_list = volatility_list[:3]
null_volat_list = []
for ticker in volatility_list[::-1]:
    if ticker['volatility'] > 0:
        break
    null_volat_list.append(ticker['name'])
null_volat_list.sort()
min_volat_list = volatility_list[-(len(null_volat_list)+3):-(len(null_volat_list))]

# Вывод данных
print('    Максимальная волатильность:')
for ticker in max_volat_list:
    print(f'        {ticker["name"]} - {ticker["volatility"]:6.2f} %')
print('    Минимальная волатильность:')
for ticker in min_volat_list:
    print(f'        {ticker["name"]} - {ticker["volatility"]:6.2f} %')
print('    Нулевая волатильность:')
print(f'        {", ".join(null_volat_list)}')

# зачет!
