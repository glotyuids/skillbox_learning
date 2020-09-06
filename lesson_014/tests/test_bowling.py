import unittest
import bowling


class BowlingTest(unittest.TestCase):
    def test_scoring(self):
        result = bowling.get_score('Х4/34-4')
        # TODO везде говорится, что эначение для проверки передаётся первым параметром, аожидаемый результат - вторым.
        #  Но если посмотреть результат теста, то будет видно,
        #  что значение Expected берётся из первого параметра, а Actual - из второго.
        #  Исходя из этого я и писал остальные тесты
        self.assertEqual(46, result, 'Некорректный подсчёт очков')

    def test_incorrect_symbol_first_roll(self):
        with self.assertRaises(ValueError) as cm:
            bowling.get_score('aХ4/34-4')
        exc = cm.exception
        self.assertEqual('Некорректный символ в последовательности. Фрейм 1. Бросок 1. Полученный символ: a',
                         exc.args[0])

    def test_incorrect_symbol_second_roll(self):
        with self.assertRaises(ValueError) as cm:
            bowling.get_score('Х4X')
        exc = cm.exception
        self.assertEqual('Некорректный символ в последовательности. Фрейм 2. Бросок 2. Полученный символ: X',
                         exc.args[0])

    def test_long_sequence(self):
        with self.assertRaises(bowling.FrameCountError):
            bowling.get_score('Х2/3/4/5/6/7/8/9/0/X')


if __name__ == '__main__':
    unittest.main()
