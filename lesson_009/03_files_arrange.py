# -*- coding: utf-8 -*-

import os
import shutil
import time
import zipfile
from datetime import datetime


ARCHIVE_NAME = 'icons.zip'
RESULT_DIR = 'icons_by_date'


# Нужно написать скрипт для упорядочивания фотографий (вообще любых файлов)
# Скрипт должен разложить файлы из одной папки по годам и месяцам в другую.
# Например, так:
#   исходная папка
#       icons/cat.jpg
#       icons/man.jpg
#       icons/new_year_01.jpg
#   результирующая папка
#       icons_by_year/2018/05/cat.jpg
#       icons_by_year/2018/05/man.jpg
#       icons_by_year/2017/12/new_year_01.jpg
#
# Входные параметры основной функции: папка для сканирования, целевая папка.
# Имена файлов в процессе работы скрипта не менять, год и месяц взять из времени создания файла.
# Обработчик файлов делать в обьектном стиле - на классах.
#
# Файлы для работы взять из архива icons.zip - раззиповать проводником в папку icons перед написанием кода.
# Имя целевой папки - icons_by_year (тогда она не попадет в коммит)
#
# Пригодятся функции:
#   os.walk
#   os.path.dirname
#   os.path.join
#   os.path.normpath
#   os.path.getmtime
#   time.gmtime
#   os.makedirs
#   shutil.copy2
#
# Чтение документации/гугла по функциям - приветствуется. Как и поиск альтернативных вариантов :)
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.

# Все замечания аналогичны
# Готово

class BaseSorter:
    def __init__(self, input_dir, result_dir):
        self.input_dir = os.path.normpath(input_dir)
        self.result_dir = os.path.normpath(result_dir)
        self.filelist = []
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)

    def sort_files(self):
        self.prepare_files()  # может архив распаковать надо будет
        self.process_files()  # обрабатываем файлы

    def get_filelist(self):
        for directory, _, files in os.walk(self.input_dir):
            for file in files:
                if file[0] != '.':  # игнорируем dot-файлы
                    self.filelist.append(os.path.join(directory, file))

    def process_files(self):
        print(f'Сортировка {os.path.abspath(self.input_dir)} \nПожалуйста, подождите...')
        print(f'╒{" progressbar ":═^20}╕')
        self.get_filelist()
        total_files = len(self.filelist)
        step = total_files // 19
        os.write(1, ' '.encode(encoding='utf-8'))
        for number, file_name in enumerate(self.filelist):
            if number % step == 0:
                os.write(1, '▓'.encode(encoding='utf-8'))
            creation_time = self.get_creation_time(file_name)
            dest_dir = os.path.join(self.result_dir,
                                    str(creation_time[0]), f'{creation_time[1]:0>2}', f'{creation_time[2]:0>2}')
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            self.copy_file(file_name, dest_dir)
        print(f'\nСортировка завершена. \n'
              f'Результат находится в {os.path.abspath(self.result_dir)}')

    def get_creation_time(self, file_name):
        # под юниксами os.path.getctime возвращает время последнего изменения файла, поэтому st_birthtime
        creation_time = os.stat(file_name).st_birthtime
        return time.gmtime(creation_time)
        # module time не импортирован
        # Видимо, когда подчищал код, случайно снёс. Пофиксил

    def copy_file(self, src, dst):
        shutil.copy2(src, dst)

    def prepare_files(self):
        pass


# class RoleUnzipFiles:
#     def prepare_files(self):
#         # почему-то extractall() не сохраняет мету файлов, поэтому будем извращаться)
#         # будем подменять время изменения каждого распакованного файла на то, которое есть в мете архивированного
#         with zipfile.ZipFile(self.input_dir, 'r') as archive:
#             for filename in archive.namelist():
#                 if archive.getinfo(filename).is_dir():
#                     continue
#
#                 archive.extract(filename)
#                 creation_time = archive.getinfo(filename).date_time
#                 creation_time = datetime(*creation_time)
#                 creation_time = time.mktime(creation_time.timetuple())
#                 os.utime(filename, (creation_time, creation_time))
#
#         self.input_dir = os.path.splitext(self.input_dir)[0]
#
#
# class RoleDontUnzip():
#     def get_filelist(self):
#         with zipfile.ZipFile(self.input_dir, mode='r') as archive:
#             for file in archive.namelist():
#                 if not archive.getinfo(file).is_dir():
#                     self.filelist.append(os.path.normpath(file))
#
#     def copy_file(self, src, dst):
#         # extract() извлекает файлы с учётом всго пути, поэтому пришлось извращаться с побайтовым копированием
#         dst = os.path.join(dst, os.path.split(src)[1])
#         with zipfile.ZipFile(self.input_dir, mode='r') as archive:
#             with archive.open(src, mode='r') as archived_file, open(dst, mode='wb') as dest_file:
#                 shutil.copyfileobj(archived_file, dest_file)
#
#     def get_creation_time(self, file_name):
#         with zipfile.ZipFile(self.input_dir, mode='r') as archive:
#             return archive.getinfo(file_name).date_time


class UnzipAndSortFiles(BaseSorter):
    def prepare_files(self):
        # почему-то extractall() не сохраняет мету файлов, поэтому будем извращаться)
        # будем подменять время изменения каждого распакованного файла на то, которое есть в мете архивированного
        with zipfile.ZipFile(self.input_dir, 'r') as archive:
            for filename in archive.namelist():
                if archive.getinfo(filename).is_dir():
                    continue

                archive.extract(filename)
                creation_time = archive.getinfo(filename).date_time
                creation_time = datetime(*creation_time)
                creation_time = time.mktime(creation_time.timetuple())
                os.utime(filename, (creation_time, creation_time))

        self.input_dir = os.path.splitext(self.input_dir)[0]


class DontUnzipAndSortFiles(BaseSorter):
    def get_filelist(self):
        with zipfile.ZipFile(self.input_dir, mode='r') as archive:
            for file in archive.namelist():
                if not archive.getinfo(file).is_dir():
                    self.filelist.append(os.path.normpath(file))

    def copy_file(self, src, dst):
        # extract() извлекает файлы с учётом всго пути, поэтому пришлось извращаться с побайтовым копированием
        dst = os.path.join(dst, os.path.split(src)[1])
        with zipfile.ZipFile(self.input_dir, mode='r') as archive:
            with archive.open(src, mode='r') as archived_file, open(dst, mode='wb') as dest_file:
                shutil.copyfileobj(archived_file, dest_file)

    def get_creation_time(self, file_name):
        with zipfile.ZipFile(self.input_dir, mode='r') as archive:
            return archive.getinfo(file_name).date_time


# Базовый класс реализует копирование файлов из input_dir в result_dir в соответствии с годом/месяцем/днём создания
# Доступные роли:
#   RoleUnzipFiles - распаковка файлов в директорию рядом с архивом
#   RoleDontUnzip - сортировка файлов без распаковки архива
# class UserSorterClass(RoleDontUnzip, BaseSorter):
#     pass


sorter = DontUnzipAndSortFiles(input_dir=ARCHIVE_NAME, result_dir=RESULT_DIR)
sorter.sort_files()

# Усложненное задание (делать по желанию)
# Нужно обрабатывать zip-файл, содержащий фотографии, без предварительного извлечения файлов в папку.
# Это относится ктолько к чтению файлов в архиве. В случае паттерна "Шаблонный метод" изменяется способ
# получения данных (читаем os.walk() или zip.namelist и т.д.)
# Документация по zipfile: API https://docs.python.org/3/library/zipfile.html
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
