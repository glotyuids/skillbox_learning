import os
from collections import defaultdict

from bowling import get_score


class Tour:
    def __init__(self, tour_results):
        self.tour_results = tour_results
        self._scores = {}
        self.errors = {}
        self._get_scores()

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

    def get_total_log(self, name_field_width=10):
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
        total_log = [self.tour_results[0]]
        for line in self.tour_results[1:-1]:
            name, rolls = line.split()
            if name in self.errors.keys():
                total_log.append(name.ljust(name_field_width + 2) + rolls.ljust(22) + str(self.errors[name]) + '\n')
            else:
                total_log.append(name.ljust(name_field_width + 2) + rolls.ljust(22) + str(self._scores[name]) + '\n')
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

    def __init__(self, results_filename):
        self.results_file = results_filename
        self.wins_count = defaultdict(int)
        self.tours_count = defaultdict(int)
        self.name_field_width = self._get_longest_name_length()

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

    def _get_longest_name_length(self):
        """
        Находит длину самого большого имени в турнире

        Returns
        -------
        max_length: int
        """
        max_length = 0
        with open(self.results_file, mode='r') as results:
            for line in results:
                if not(line.startswith(('### Tour', 'winner', '\n'))):
                    name, _ = line.split()
                    max_length = len(name) if len(name) > max_length else max_length
        return max_length

    def count_scores(self, out_file_name=os.devnull):
        with open(out_file_name, mode='w') as out_file:
            tour_number = 0
            for tour_results in self.tours():
                tour = Tour(tour_results)
                # считаем количество игр и количество побед для каждого игрока
                for name in tour.scores.keys():
                    self.tours_count[name] += 1
                for name in tour.winners:
                    self.wins_count[name] += 1
                # выводим лог тура в файл
                tour_log = tour.get_total_log(self.name_field_width)
                out_file.writelines(tour_log)


if __name__ == '__main__':
    world_cup = Tournament('tournament.txt')
    world_cup.count_scores(out_file_name='bowling_results.txt')


