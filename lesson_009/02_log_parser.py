# -*- coding: utf-8 -*-

# Имеется файл events.txt вида:
#
# [2018-05-17 01:55:52.665804] NOK
# [2018-05-17 01:56:23.665804] OK
# [2018-05-17 01:56:55.665804] OK
# [2018-05-17 01:57:16.665804] NOK
# [2018-05-17 01:57:58.665804] OK
# ...
#
# Напишите программу, которая считывает файл
# и выводит число событий NOK за каждую минуту в другой файл в формате
#
# [2018-05-17 01:57] 1234
# [2018-05-17 01:58] 4321
# ...
#
# Входные параметры: файл для анализа, файл результата
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.

import os


LOG_FILE = 'events.txt'
RESULTS_FILE = 'results.txt'
# Исправьте константы согласно РЕР8
# Done


class BaseLogAnalyzer:
    time_slice = [1, 17]
    # Cоздайте атрибут - типа "правая_граница_признака_времени" - и метод для его установки.
    #  Этот метод переопределяйте в наследниках
    # TODO Мне показалось, что такой подход будет более гибким. Но тут скорее следовало бы создать методы
    #  get_data (возврат даты нужного формата из строки) и get_event (вытаскивание из лога и обработка статуса)

    def __init__(self, log_file, results_file):
        self.log_file = os.path.normpath(log_file)
        self.results_file = os.path.normpath(results_file)

    def analyze(self):
        self.process_data()  # обрабатываем лог
        self.postprocess_result_file()
        # может результаты в архив упаковать надо будет, приводить к нужному формату или просто вывести на консоль

    def process_data(self):
        print(f'Обработка лога {os.path.abspath(self.log_file)}')
        with open(self.log_file, mode='r', encoding='utf-8') as log:
            with open(self.results_file, mode='w', encoding='utf-8') as results:
                current_time = log.read(self.time_slice[1])
                current_time = current_time[self.time_slice[0]: self.time_slice[1]]
                log.seek(0, 0)
                current_minute_NOKs = 0
                for line in log:
                    if current_time != line[self.time_slice[0]: self.time_slice[1]]:
                        results.write(f'[{current_time}] {current_minute_NOKs}\n')
                        current_time = line[self.time_slice[0]: self.time_slice[1]]
                        current_minute_NOKs = 0
                    if 'NOK' in line:
                        current_minute_NOKs += 1
                results.write(f'[{current_time}] {current_minute_NOKs}\n')

    def postprocess_result_file(self):
        print(f'Результат обработки лога записан в файл {os.path.abspath(self.results_file)}')


class GroupByHour:
    time_slice = [1, 14]


class GroupByMonth:
    time_slice = [1, 8]


class GroupByYear:
    time_slice = [1, 5]


class PrintResults:
    def postprocess_result_file(self):
        with open(self.results_file, mode='r', encoding='utf-8') as results:
            for line in results:
                print(line, end='')


# Базовый класс реализует обработку лога log_file с подсчётом NOK'ов по минутам и выводом результата в results_file
# Доступные роли:
#   GroupByHour - подсчёт NOK'ов по часам
#   GroupByMonth - подсчёт NOK'ов по месяцам
#   GroupByYear - подсчёт NOK'ов по годам
#   PrintResults -  вывод результата на консоль, а не в файл
class UserAnalyzer(GroupByHour, PrintResults, BaseLogAnalyzer):
    pass
# TODO Сделайте на явном наследовании


log_analyzer = UserAnalyzer(log_file=LOG_FILE, results_file=RESULTS_FILE)
log_analyzer.analyze()

# После выполнения первого этапа нужно сделать группировку событий
#  - по часам
#  - по месяцу
#  - по году
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
