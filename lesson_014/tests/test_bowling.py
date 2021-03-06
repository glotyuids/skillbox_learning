import unittest
import bowling


class BowlingTest(unittest.TestCase):
    def test_scoring(self):
        result = bowling.get_score('Х4/34-4------------')
        # TODO везде говорится, что эначение для проверки передаётся первым параметром, аожидаемый результат - вторым.
        #  Но если посмотреть результат теста, то будет видно,
        #  что значение Expected берётся из первого параметра, а Actual - из второго.
        #  Исходя из этого я и писал остальные тесты
        self.assertEqual(46, result, 'Некорректный подсчёт очков по старым правилам')

        result = bowling.get_score('Х4/34-4------------', new_rules=True)
        self.assertEqual(44, result, 'Некорректный подсчёт очков по новым правилам')

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

        with self.assertRaises(ValueError) as cm:
            bowling.get_score('Х55')
        exc = cm.exception
        self.assertEqual('За фрейм сбито 10 кеглей, но результат записан не как спейр, а как два числа. '
                         'Фрейм 2. Количество кеглей за этот фрейм: 5 + 5 = 10',
                         exc.args[0])

    def test_incorrect_sequence_length(self):
        with self.assertRaises(bowling.FrameCountError):
            bowling.get_score('X' * 9)
        with self.assertRaises(bowling.FrameCountError):
            bowling.get_score('Х' * 11)

    def test_incomplete_last_frame(self):
        with self.assertRaises(IndexError) as cm:
            bowling.get_score('Х4')
        exc = cm.exception
        self.assertEqual('Последний фрейм не завершён - нет второго броска',
                         exc.args[0])


if __name__ == '__main__':
    unittest.main()
