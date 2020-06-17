# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПРОЦЕССНОМ стиле
#
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
# TODO Внимание! это задание можно выполнять только после зачета lesson_012/02_volatility_with_threads.py !!!

import os
import csv
import multiprocessing

TRADES_DIR = 'trades'


class TTradeAnalyzer(multiprocessing.Process):
    def __init__(self, ticker_filename, pipe, semaphore, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ticker_filename = ticker_filename
        self.volatility = None
        self.pipe = pipe
        self.semaphore = semaphore
        with open(self.ticker_filename) as ticker_file:
            trades = csv.DictReader(ticker_file)
            self.ticker_name = next(trades)['SECID']

    def run(self):
        with self.semaphore:
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
            self.pipe.send({'name': self.ticker_name, 'volatility': self.volatility})


# инициалиация объектов
trades_list = [os.path.join(TRADES_DIR, ticker) for ticker in os.listdir(TRADES_DIR)]
trades_list = [ticker for ticker in trades_list if os.path.isfile(ticker)]
volatility_list = []
analyzers_list = []
pipes = []

# попробую ограничить количество одновременно работающих воркеров количеством ядер/потоков процессора - 1
availiable_cpus = multiprocessing.cpu_count() - 1 if multiprocessing.cpu_count() > 1 else 1
semaphore = multiprocessing.BoundedSemaphore(availiable_cpus)

# Обработка файлов
for ticker in trades_list:
    parent_conn, child_conn = multiprocessing.Pipe()
    pipes.append(parent_conn)
    analyzers_list.append(TTradeAnalyzer(ticker, child_conn, semaphore))

for analyzer in analyzers_list:
    analyzer.start()

for conn in pipes:
    volatility_list.append(conn.recv())

for analyzer in analyzers_list:
    analyzer.join()

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

