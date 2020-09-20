from bowling import get_score

import io


class Tour:
    def __init__(self, tour_results):
        self.tour_results = tour_results
        self.scores = {}
        self._get_scores()
        self.winner = max(self.scores, key=self.scores.get)

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
        for line in self.tour_results.readlines()[1:-1]:
            name, _ = line.split()
            total_log.write(line[:-1] + '  \t' + str(self.scores[name]) + '\n')
        total_log.write('winner is ' + self.winner + '\n\n')
        total_log.seek(0)
        return total_log

    def _get_scores(self):
        """
        Считает очки игроков в этом туре.
        Собирает словарь вида {имя_игрока: набранные_очки}
        """
        for line in self.tour_results.readlines()[1:-1]:
            name, game_result = line.split()
            score = get_score(game_result)
            self.scores[name] = score


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
            break


if __name__ == '__main__':
    world_cup = Tournament('tournament.txt')
    world_cup.run()


