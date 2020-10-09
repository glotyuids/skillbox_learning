class FrameCountError(Exception):
    pass


class ScoreCounter:
    _state = None
    frames_count = 10

    def __init__(self, game_result):
        self.set_state(FirstRoll())
        self.game_result = game_result

        self.frame_results = []
        self.pins = []
        self.multipliers = [0, 0]

    def set_state(self, state):
        self._state = state
        self._state.context = self

    def get_score(self):
        for roll in self.game_result:
            self._state.count_score(roll)
        if len(self.frame_results) < self.frames_count:
            raise FrameCountError(f'Количество фреймов в последовательности меньше {self.frames_count}')
        return sum(self.frame_results)


class State:
    context = None

    def count_score(self, roll):
        pass


class FirstRoll(State):
    def count_score(self, roll):
        if roll == '\0':
            return
        if len(self.context.frame_results) >= self.context.frames_count:
            raise FrameCountError(f'Количество фреймов в последовательности больше {self.context.frames_count}')
        if roll in 'XxХх':
            result = 20
            pins = 10
        else:
            if roll == '-':
                result = pins = 0
            elif roll.isdigit():
                result = pins = int(roll)
            else:
                raise ValueError(f'Некорректный символ в последовательности. '
                                 f'Фрейм {len(self.context.frame_results) + 1}. Бросок 1. Полученный символ: {roll}')

            self.context.set_state(SecondRoll())

        self.context.frame_results.append(result)
        self.context.pins.append(pins)


class SecondRoll(State):
    def count_score(self, roll):
        if roll == '\0':
            raise IndexError('Последний фрейм не завершён - нет второго броска')
        if roll == '/':
            self.context.frame_results[-1] = 15
            pins = 10 - self.context.pins[-1]
        else:
            if roll == '-':
                result = pins = 0
            elif roll.isdigit():
                result = pins = int(roll)

                if self.context.frame_results[-1] + result == 10:
                    raise ValueError(f'За фрейм сбито 10 кеглей, но результат записан не как спейр, а как два числа. '
                                     f'Фрейм {len(self.context.frame_results)}. '
                                     f'Количество кеглей за этот фрейм: {self.context.frame_results[-1]} + {result} = '
                                     f'{self.context.frame_results[-1] + result}')
                if self.context.frame_results[-1] + result > 10:
                    raise ValueError(f'Количество кеглей, сбитых за один фрейм, не должно быть больше 10. '
                                     f'Фрейм {len(self.context.frame_results)}. '
                                     f'Количество кеглей за этот фрейм: {self.context.frame_results[-1]} + {result} = '
                                     f'{self.context.frame_results[-1] + result}')
            else:
                raise ValueError(f'Некорректный символ в последовательности. '
                                 f'Фрейм {len(self.context.frame_results)}. Бросок 2. Полученный символ: {roll}')

            self.context.frame_results[-1] += result

        self.context.set_state(FirstRoll())
        self.context.pins.append(pins)


def get_score(game_result):
    counter = ScoreCounter(game_result + '\0')
    return counter.get_score()


if __name__ == '__main__':
    # ваше решение не обрабатывает след. неправильные для 10 фреймовой игры по 10 кеглей на фрейм данные
    input = 'X' * 3 + '252/' + 'X' * 5
    #input = 'X' * 9 + '55'
    print(get_score(input))
