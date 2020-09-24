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
        # TODO отработать несколько победителей

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
        Возвращает список строк итоговым логом тура (входные строки, очки и победитель)

        Returns
        -------
        total_log: list of strings
        """
        total_log = [self.tour_results[0]]
        for line in self.tour_results[1:-1]:
            name, _ = line.split()
            if name in self.errors.keys():
                total_log.append(line[:-1] + '  \t' + str(self.errors[name]) + '\n')
            else:
                total_log.append(line[:-1] + '  \t' + str(self._scores[name]) + '\n')
        total_log.append('winner is ' + self.winner + '\n\n')
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

    def tours(self):
        """
        Генератор туров.
        Берет из файла каждый тур и возвращает его как отдельный список строк

        Yields
        -------
        tour_results: list of strings
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
            yield tour_results

    def run(self):
        with open('bowling_results.txt', mode='w') as out_file:
            tour_number = 0
            for tour_results in self.tours():
                tour = Tour(tour_results)
                tour_log = tour.get_total_log()
                out_file.writelines(tour_log)
                tour_number += 1
                print(str(tour_number), tour.scores)


if __name__ == '__main__':
    world_cup = Tournament('tournament.txt')
    world_cup.run()


