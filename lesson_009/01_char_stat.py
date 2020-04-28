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


FILENAME = 'python_snippets/voyna-i-mir.txt'
# Имена констант пишутся большими буквами, распологаются сразу после импортов модулей
# Done


class BaseTextAnalyzer:
    def __init__(self, filename):
        self.processed_data = []
        self.filename = os.path.normpath(filename)

    def run(self):  # Имя шаблонного метода может быть более общее и простое, типа "запустить", "выполнить"
        # поправил
        self.prepare_file()  # может его распаковать надо будет. а может сконвертить из одного формата в другой
        self.process_data()  # собираем статистику
        self.postprocess_data()  # обработка данных. В данном случае та или иная сортировка
        self.output_data()  # выводим данные (в консоль, файл и т.д. - зависит от метода)

    def prepare_file(self):
        pass

    def process_data(self):
        print(f'Обработка файла {os.path.abspath(self.filename)}')
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


class RoleSortByCount:
    def postprocess_data(self):
        self.processed_data.sort(key=lambda data: data[0])


class RoleSortByAlphabet:
    def postprocess_data(self):
        self.processed_data.sort(key=lambda data: data[1])


class RoleRevSortByAlphabet:
    def postprocess_data(self):
        self.processed_data.sort(key=lambda data: data[1], reverse=True)


class RoleUnzipTxtFile:
    def prepare_file(self):
        import zipfile
        with zipfile.ZipFile(self.filename, 'r') as archive:
            archived_files = archive.namelist()
            archive.extract(archived_files[0], path=os.path.dirname(self.filename))
            self.filename = os.path.join(os.path.dirname(self.filename), archived_files[0])


class RoleOutputToFile:
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
        print(f'Статистика записана в файл {os.path.abspath(results_file)}')


class AnalyzeAndSortByCount(BaseTextAnalyzer):
    def postprocess_data(self):
        self.processed_data.sort(key=lambda data: data[0])


class AnalyzeAndSortByAlphabet(BaseTextAnalyzer):
    def postprocess_data(self):
        self.processed_data.sort(key=lambda data: data[1])


class AnalyzeAndRevSortByAlphabet(BaseTextAnalyzer):
    def postprocess_data(self):
        self.processed_data.sort(key=lambda data: data[1], reverse=True)


# Базовый класс реализует подсчёт количества каждой буквы в filename и вывод результата на консоль в виде таблицы
# Доступные роли:
#   RoleSortByCount - сортировка данных по возрастанию количества букв
#   RoleSortByAlphabet - сортировка данных по алфавиту по возрастанию
#   RoleRevSortByAlphabet - сортировка данных по алфавиту по убыванию
#   RoleUnzipTxtFile - распаковка анализируемого файла из архива
#   RoleOutputToFile - вывод результата в текстовый файл рядом с анализируемым. К имени добавляется постфикс '_stats'
class UserAnalyzer(RoleUnzipTxtFile, RoleRevSortByAlphabet, RoleOutputToFile, BaseTextAnalyzer):
    pass


# 1) имя класса слишком общее, оно должно отражать основное назначение класса и специфику
#  Тут в названии скорее имелось ввиду, что тот, кто будет с этим кодом работать,
#  может собирать свой кастомный класс из доступных ролей

#  2) множественное наследование достаточно сложная тема, в этом случае нужно смотреть на MRO -
#  https://www.google.ru/search?q=python+mro
#  и вот тут запутататься и получить непредсказуемое ошибки от перемены мест классов наследования - очень легко, из-за
#  чего есть мнение, что множественно наследование это антипаттерн. Поэтому сделайте на явном наследовании.
#  Да, про MRO Вадим в лекции о множественном наследовании говорил. И поскольку тут нет дочерних классов,
#  а роли ни от кого не наследуются и никому не наследуют, то порядок разрешения будет в порядке перечисления классов.
#  Само собой, базовый класс всегда должен находиться в конце - об этом я забыл написать в комменте с описанием

#   Решение с ролями мне показалось достаточно изящным, так что, если позволите, я его пока здесь оставлю -
#   позже закину к себе в сниппеты, а для выполнения задания создам дочерние классы от BaseTextAnalyzer на основе ролей


analyzer = AnalyzeAndRevSortByAlphabet(filename=FILENAME)
analyzer.run()

# После выполнения первого этапа нужно сделать упорядочивание статистики
#  + по частоте по возрастанию
#  + по алфавиту по возрастанию
#  + по алфавиту по убыванию
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://goo.gl/Vz4828
#   и пример https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4

# зачет!
