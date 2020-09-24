from bowling import get_score

import io


class Tour:
    def __init__(self, tour_results):
        self.tour_results = tour_results
        self._scores = {}
        self.errors = {}
        self._get_scores()
        self.winner = max(self._scores, key=self._scores.get)
        if self.winner in self.errors.keys():
            self.winner = 'Никто: у всех игроков в этом туре имеются ошибки в записи ходов'

    @property
    def scores(self):
        """
        Возвращает словарь с итогами тура
        Returns
        -------
        Словарь вида {имя_игрока: набранные_очки}. Если была ошибка парсинга, то возвращается 0 очков
        """
        return {name: (score if score != -1 else 0) for (name, score) in self._scores.items()}

    def get_total_log(self):
        """
        Возвращает file-like текстовый объект с итоговым логом тура (входные строки, очки и победитель)

        Returns
        -------
        total_log: io.StringIO
        """
        total_log = io.StringIO()
        self.tour_results.seek(0)
        total_log.write(self.tour_results.readline())
        for line in self.tour_results.readlines()[:-1]:
            name, _ = line.split()
            if name in self.errors.keys():
                total_log.write(line[:-1] + '  \t' + str(self.errors[name]) + '\n')
            else:
                total_log.write(line[:-1] + '  \t' + str(self._scores[name]) + '\n')
        total_log.write('winner is ' + self.winner + '\n\n')
        total_log.seek(0)
        return total_log

    def _get_scores(self):
        """
        Считает очки игроков в этом туре.
        Собирает словарь вида {имя_игрока: набранные_очки}.
        Если была ошибка парсинга, то ошибка откладывается в отдельный словарь вида {имя_игрока: текст_ошибки},
        а в словарь очков добавляется запись {имя_игрока: -1}
        """
        for line in self.tour_results.readlines()[1:-1]:
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

    def tours(self):
        """
        Генератор туров.
        Берет из файла каждый тур и возвращает его как отдельный текстовый file-like объект

        Yields
        -------
        tour_results: io.StringIO
        """
        with open(self.results_file, mode='r') as results:
            tour_results = io.StringIO()
            for line in results:
                if line != '\n':
                    tour_results.write(line)
                else:
                    tour_results.seek(0)
                    yield tour_results
                    tour_results = io.StringIO()
            yield tour_results

    def run(self):
        for tour_results in self.tours():
            another_tour = Tour(tour_results)
            tour_log = another_tour.get_total_log()
            for line in tour_log:
                print(line, end='')
            print(another_tour.scores)
            break


if __name__ == '__main__':
    world_cup = Tournament('tournament.txt')
    world_cup.run()


