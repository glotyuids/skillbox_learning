# -*- coding: utf-8 -*-

# На основе своего кода из lesson_009/02_log_parser.py напишите итератор (или генератор)
# котрый читает исходный файл events.txt и выдает число событий NOK за каждую минуту
# <время> <число повторений>
#
# пример использования:
#
# grouped_events = <создание итератора/генератора>  # Итератор или генератор? выбирайте что вам более понятно
# for group_time, event_count in grouped_events:
#     print(f'[{group_time}] {event_count}')
#
# на консоли должно появится что-то вроде
#
# [2018-05-17 01:57] 1234

import os


LOG_FILE = 'events.txt'


class BaseLogAnalyzerIter:
    def __init__(self, log_file):
        self.log_file = os.path.normpath(log_file)
        self.read_offset = 0

    @staticmethod
    def get_datetime(string):
        return string[1: 17]

    @staticmethod
    def is_required_event(string):
        return 'NOK' in string

    @staticmethod
    def get_pos(file):
        return file

    def __iter__(self):
        self.read_offset = 0
        return self

    def __next__(self):
        with open(self.log_file, mode='r', encoding='utf-8') as log:
            log.seek(self.read_offset, 0)
            current_time = self.get_datetime(log.readline())
            log.seek(self.read_offset, 0)
            current_minute_NOKs = 0
            # ну, раз из for-циклов в текстовом режиме вызывать tell() нельзя, пойдём другим путём
            while True:
                self.read_offset = log.tell()
                line = log.readline()
                if line == '':
                    raise StopIteration
                if current_time != self.get_datetime(line):
                    break
                if self.is_required_event(line):
                    current_minute_NOKs += 1
            return current_time, current_minute_NOKs


class GroupLogByHourIter(BaseLogAnalyzerIter):
    def get_datetime(self, string):
        return string[1: 14]


class GroupLogByMonthIter(BaseLogAnalyzerIter):
    def get_datetime(self, string):
        return string[1: 8]


class GroupLogByYearIter(BaseLogAnalyzerIter):
    def get_datetime(self, string):
        return string[1: 5]


grouped_events = BaseLogAnalyzerIter(log_file=LOG_FILE)
for group_time, event_count in grouped_events:
    print(f'[{group_time}] {event_count}')


