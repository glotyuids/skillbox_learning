# -*- coding: utf-8 -*-

# Подсчитать статистику по буквам в романе Война и Мир.
# Входные параметры: файл для сканирования
# Статистику считать только для букв алфавита (см функцию .isalpha() для строк)
#
# Вывести на консоль упорядоченную статистику в виде
# +---------+----------+
# |  буква  | частота  |
# +---------+----------+
# |    А    |   77777  |
# |    Б    |   55555  |
# |   ...   |   .....  |
# |    a    |   33333  |
# |    б    |   11111  |
# |   ...   |   .....  |
# +---------+----------+
# |  итого  | 9999999  |
# +---------+----------+
#
# Упорядочивание по частоте - по убыванию. Ширину таблицы подберите по своему вкусу
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.

import os


class BaseTextAnalyzer():
    def __init__(self, filename):
        self.processed_data = []
        self.filename = os.path.normpath(filename)

    def analyze(self):
        self.prepare_file()         # может его распаковать надо будет. а может сконвертить из одного формата в другой
        self.process_data()         # собираем статистику
        self.postprocess_data()     # обработка данных. В данном случае та или иная сортировка
        self.output_data()          # выводим данные (в консоль, файл и т.д. - зависит от метода)
        
    def prepare_file(self):
        pass

    def process_data(self):
        stats = {}
        with open(self.filename, mode='r', encoding='cp1251') as file:
            for line in file:
                for char in line[:-1]:
                    if char.isalpha():
                        if char in stats:
                            stats[char] += 1
                        else:
                            stats[char] = 1
        self.processed_data = [[count, char] for char, count in stats.items()]

    def postprocess_data(self):
        pass

    def output_data(self):
        print('╔═════════╤══════════╗ \n'
              '║  буква  │ частота  ║ \n'
              '╟─────────┼──────────╢')

        for count, char in self.processed_data:
            print(f'║{char:^9}│{count:8d}  ║')

        print('╟─────────┼──────────╢')

        chars_count = sum([count for count, _ in self.processed_data])
        print(f'╟  итого  │{chars_count:8d}  ║')

        print('╚═════════╧══════════╝')


class SortByCount:
    def postprocess_data(self):
        self.processed_data.sort(key=lambda data: data[0])


class SortByAlphabet:
    def postprocess_data(self):
        self.processed_data.sort(key=lambda data: data[1])


class RevSortByAlphabet:
    def postprocess_data(self):
        self.processed_data.sort(key=lambda data: data[1], reverse=True)


class UnzipTxtFile:
    def prepare_file(self):
        import zipfile
        with zipfile.ZipFile(self.filename, 'r') as archive:
            archived_files = archive.namelist()
            archive.extract(archived_files[0], path=os.path.dirname(filename))
            self.filename = os.path.join(os.path.dirname(filename), archived_files[0])


class OutputToFile:
    def output_data(self):
        results_file = os.path.splitext(self.filename)[0] + '_stats.txt'
        with open(results_file, mode='w') as file:
            file.write('╔═════════╤══════════╗ \n'
                       '║  буква  │ частота  ║ \n'
                       '╟─────────┼──────────╢ \n')

            for count, char in self.processed_data:
                file.write(f'║{char:^9}│{count:8d}  ║ \n')

            file.write('╟─────────┼──────────╢ \n')

            chars_count = sum([count for count, _ in self.processed_data])
            file.write(f'╟  итого  │{chars_count:8d}  ║ \n')

            file.write('╚═════════╧══════════╝ \n')
        print(f'Статистика записана в файл {results_file}')


class UserAnalyzer(UnzipTxtFile, RevSortByAlphabet, OutputToFile, BaseTextAnalyzer):
    pass


filename = 'python_snippets/voyna-i-mir.txt.zip'

analyzer = UserAnalyzer(filename)
analyzer.analyze()

# После выполнения первого этапа нужно сделать упорядочивание статистики
#  - по частоте по возрастанию
#  - по алфавиту по возрастанию
#  - по алфавиту по убыванию
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://goo.gl/Vz4828
#   и пример https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4
