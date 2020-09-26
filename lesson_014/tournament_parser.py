import os
from collections import defaultdict
from tabulate import tabulate

from bowling import get_score


class Tour:
    def __init__(self, tour_results):
        self.tour_results = tour_results
        self._scores = {}
        self.errors = {}
        self._get_scores()
        self.name_field_width = max([len(name) for name in self._scores.keys()])

    @property
    def winners(self):
        """
        Возвращает список победителей
        Returns
        -------
        list of strings
        """
        max_score = max(self._scores.values())
        if max_score == -1:
            return []
        else:
            return [name for (name, score) in self._scores.items() if score == max_score]

    @property
    def scores(self):
        """
        Возвращает словарь с итогами тура
        Returns
        -------
        Словарь вида {имя_игрока: набранные_очки}. Если была ошибка парсинга, то возвращается 0 очков
        """
        return {name: (score if score != -1 else 0) for (name, score) in self._scores.items()}

    def get_total_log(self, name_field_width=None):
        """
        Возвращает список строк итоговым логом тура (входные строки, очки и победитель)

        Parameters
        ----------
        name_field_width: int, default=10
            Ширина поля для имени

        Returns
        -------
        total_log: list[str]
        """
        name_field_width = name_field_width if name_field_width is not None else self.name_field_width
        total_log = [self.tour_results[0]]
        for line in self.tour_results[1:-1]:
            name, rolls = line.split()
            if name in self.errors.keys():
                # f"" удобнее и быстрее
                # TODO Поправил. Я изначально хотел использовать f-строки, но не до конца разобрался с переменными
                #  в спецификаторе формата (вернее увидел ошибку, но не стал разбираться и пошёл другим путём).
                #  Сейчас наконец-то дошли руки, спасибо)
                total_log.append(f'{name:<{name_field_width}}  {rolls:<20}  {self.errors[name]}\n')
            else:
                total_log.append(f'{name:<{name_field_width}}  {rolls:<20}  {self._scores[name]}\n')
        winners = self.winners
        winners = ['Никто: у всех игроков в этом туре имеются ошибки в записи ходов'] if len(winners) == 0 else winners
        total_log.append('winner is ' + ', '.join(winners) + '\n\n')
        return total_log

    def _get_scores(self):
        """
        Считает очки игроков в этом туре.
        Собирает словарь вида {имя_игрока: набранные_очки}.
        Если была ошибка парсинга, то ошибка откладывается в отдельный словарь вида {имя_игрока: текст_ошибки},
        а в словарь очков добавляется запись {имя_игрока: -1}
        """
        for line in self.tour_results[1:-1]:
            name, game_result = line.split()
            try:
                score = get_score(game_result)
            except Exception as exc:
                self._scores[name] = -1
                self.errors[name] = 'Error: ' + str(exc)
            else:
                self._scores[name] = score


class Tournament:

    NAME = -1
    PLAYS = 0
    SCORE = 1
    WINS = 2

    def __init__(self, results_filename):
        self.results_file = results_filename
        self.stats = defaultdict(lambda: [0, 0, 0])

    def tours(self):
        """
        Генератор туров.
        Берет из файла каждый тур и возвращает его как отдельный список строк

        Yields
        -------
        tour_results: list[str]
        """
        with open(self.results_file, mode='r') as results:
            tour_results = []
            for line in results:
                if line != '\n':
                    tour_results.append(line)
                elif len(tour_results) == 0 or tour_results[-1] == '\n':
                    continue
                else:
                    yield tour_results
                    tour_results = []
            if len(tour_results) > 0 and tour_results[-1] != '\n':
                yield tour_results

    def count_scores(self, out_file_name=os.devnull):
        """
        Метод перебирает все туры в файле, находит набранные игроками очки, победителя и записывает это в out_file_name.
        Если имя файла не указано, то лог турнира никуда не пишется.
        Также считает для каждого игрока количество сыгранных туров и побед.

        Parameters
        ----------
        out_file_name: str, default=os.devnull
            Имя файла для записи результатов турнира

        """
        with open(out_file_name, mode='w') as out_file:
            for tour_results in self.tours():
                tour = Tour(tour_results)
                # считаем количество игр и количество побед для каждого игрока
                for name in tour.scores.keys():
                    self.stats[name][Tournament.SCORE] += tour.scores[name]
                    self.stats[name][Tournament.PLAYS] += 1
                for name in tour.winners:
                    self.stats[name][Tournament.WINS] += 1
                # выводим лог тура в файл
                tour_log = tour.get_total_log()
                out_file.writelines(tour_log)

    def print_stats(self, sort_by=-1, reverse=False):
        """
        Выводит на консоль статистику по турниру

        Parameters
        ----------
        sort_by: int, default=Tournament.NAME
            Способ сортировки:
                Tournament.NAME - по имени игрока (по алфавиту)
                Tournament.PLAYS - по количеству сыгранных туров
                Tournament.SCORE - по количеству очков
                Tournament.WINS - по количеству побед

        reverse: bool, default=False
            Сортировка в обратном порядке
        """
        # Распаковываем словарь вида {name:[plays, score, wins], } в список [[name, plays, score, wins], ]
        # и сортируем статистику по выбранному критерию. По умолчанию сортировка происходит по возрастанию,
        # соответственно, сортировка по имени происходит как должна.
        # А вот сортировку по другим параметрам по умолчанию неплохо было бы делать по убыванию,
        # поэтому в остальных случаях реверс инвертируем
        sorted_stats = [(name, *value) for name, value in self.stats.items()]
        sorted_stats = sorted(sorted_stats, key=lambda player: player[sort_by + 1],
                              reverse=reverse if sort_by == Tournament.NAME else not reverse)

        print(tabulate(sorted_stats, headers=['Игрок', 'сыграно матчей', 'заработано очков', 'всего побед'],
                       tablefmt="pretty", colalign=('left',)))


if __name__ == '__main__':
    world_cup = Tournament('tournament.txt')
    world_cup.count_scores()
    world_cup.print_stats(sort_by=Tournament.WINS)
