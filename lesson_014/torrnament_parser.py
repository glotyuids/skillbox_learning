from bowling import get_score

import io


class Tour:
    pass

    def get_player_results(self):
        pass


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
        for tour in self.tours():
            pass


if __name__ == '__main__':
    world_cup = Tournament('tournament.txt')
    world_cup.run()


