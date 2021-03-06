# -*- coding: utf-8 -*-

# Прибежал менеджер и сказал что нужно срочно просчитать протокол турнира по боулингу в файле tournament.txt
#
# Пример записи из лога турнира
#   ### Tour 1
#   Алексей	35612/----2/8-6/3/4/
#   Татьяна	62334/6/4/44X361/X
#   Давид	--8/--8/4/8/-224----
#   Павел	----15623113-95/7/26
#   Роман	7/428/--4-533/34811/
#   winner is .........
#
# Нужно сформировать выходной файл tournament_result.txt c записями вида
#   ### Tour 1
#   Алексей	35612/----2/8-6/3/4/    98
#   Татьяна	62334/6/4/44X361/X      131
#   Давид	--8/--8/4/8/-224----    68
#   Павел	----15623113-95/7/26    69
#   Роман	7/428/--4-533/34811/    94
#   winner is Татьяна

# Код обаботки файла расположить отдельном модуле, модуль bowling использовать для получения количества очков
# одного участника. Если захочется изменить содержимое модуля bowling - тесты должны помочь.
#
# Из текущего файла сделать консольный скрипт для формирования файла с результатами турнира.
# Параметры скрипта: --input <файл протокола турнира> и --output <файл результатов турнира>

from tournament_parser import Tournament
import argparse


if __name__ == '__main__':
    # форматирование хелпа сделано аналогично первому заданию.
    nbsp = '\u00A0'
    parser = argparse.ArgumentParser(description='Утилита считает результаты турнира и выводит их в файл')
    parser.add_argument('--input', action='store', dest='tournament_file', required=True,
                        help=(f'Текстовый протокол турнира.{nbsp * 27} '
                              f'Туры записываются в формате:{nbsp * 26} '
                              f'### Tour 1{nbsp * 44} '
                              f'Имя_игрока_1 броки_игрока_1{nbsp * 27} '
                              f'Имя_игрока_2 броки_игрока_2{nbsp * 27} '
                              f'...{nbsp * 51} '
                              f'Имя_игрока_n броки_игрока_n{nbsp * 27} '
                              f'winner is .........{nbsp * 35} '
                              f'\n{nbsp * 53} '
                              f'### Tour 2{nbsp * 44} '
                              f'...{nbsp * 52} '))
    parser.add_argument('--output', action='store', dest='results_file', required=True,
                        help=f'Текстовый файл, в который запишутся результаты турнира')
    args = parser.parse_args()

    tournament = Tournament(args.tournament_file)
    tournament.count_scores(args.results_file)
    tournament.print_stats(sort_by=Tournament.WINS)

# Усложненное задание (делать по желанию)
#
# После обработки протокола турнира вывести на консоль рейтинг игроков в виде таблицы:
#
# +----------+------------------+--------------+
# | Игрок    |  сыграно матчей  |  всего побед |
# +----------+------------------+--------------+
# | Татьяна  |        99        |      23      |
# ...
# | Алексей  |        20        |       5      |
# +----------+------------------+--------------+
# Зачет!