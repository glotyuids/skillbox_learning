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
    # Cоздайте атрибут - типа "правая_граница_признака_времени" - и метод для его установки.
    #  Этот метод переопределяйте в наследниках
    #  Мне показалось, что мой подход будет более гибким. Но тут для большей гибкости следовало бы создать методы
    #  get_datetime (возврат даты нужного формата из строки)
    #  и is_required_event (вытаскивание события из строки лога и его обработка)
    # -- Возможно дело вкуса, но по мне - установка атрибута акцентированнее намекает на то, что это именно ключевая
    # настройка.
    def __init__(self, log_file, results_file):
        self.log_file = os.path.normpath(log_file)
        self.results_file = os.path.normpath(results_file)

    def run(self):
        self.process_data()  # обрабатываем лог
        self.postprocess_result_file()
        # может результаты в архив упаковать надо будет, приводить к нужному формату или просто вывести на консоль

    def process_data(self):
        print(f'Обработка лога {os.path.abspath(self.log_file)}')
        with open(self.log_file, mode='r', encoding='utf-8') as log:
            with open(self.results_file, mode='w', encoding='utf-8') as results:
                current_time = self.get_datetime(log.readline())
                log.seek(0, 0)
                current_minute_NOKs = 0
                for line in log:
                    if current_time != self.get_datetime(line):
                        results.write(f'[{current_time}] {current_minute_NOKs}\n')
                        current_time = self.get_datetime(line)
                        current_minute_NOKs = 0
                    if self.is_required_event(line):
                        current_minute_NOKs += 1
                results.write(f'[{current_time}] {current_minute_NOKs}\n')

    def get_datetime(self, string):
        return string[1: 17]

    def is_required_event(self, string):
        return 'NOK' in string

    def postprocess_result_file(self):
        print(f'Результат обработки лога записан в файл {os.path.abspath(self.results_file)}')


class GroupLogByHour(BaseLogAnalyzer):
    def get_datetime(self, string):
        return string[1: 14]


class GroupLogByMonth(BaseLogAnalyzer):
    def get_datetime(self, string):
        return string[1: 8]


class GroupLogByYear(BaseLogAnalyzer):
    def get_datetime(self, string):
        return string[1: 5]


# Сделайте на явном наследовании
# Формальности соблюдены =)
log_analyzer = GroupLogByHour(log_file=LOG_FILE, results_file=RESULTS_FILE)
log_analyzer.run()

# После выполнения первого этапа нужно сделать группировку событий
#  - по часам
#  - по месяцу
#  - по году
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828

# зачет!
