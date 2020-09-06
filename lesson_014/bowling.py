
class FrameCountError(Exception):
    pass


class ScoreCounter:
    _state = None

    def __init__(self, game_result):
        self.set_state(FirstRoll())
        self.game_result = game_result

        self.frame_score = 0
        self.frame_results = []

    def set_state(self, state):
        self._state = state
        self._state.context = self

    def get_score(self):
        for roll in self.game_result:
            self._state.count_score(roll)
        return sum(self.frame_results)


class State:
    context = None

    def count_score(self, roll):
        pass


class FirstRoll(State):
    def count_score(self, roll):
        if len(self.context.frame_results) >= 10:
            raise FrameCountError('Количество фреймов в последовательности больше 10')
        if roll in 'XxХх':
            result = 20
        else:
            if roll == '-':
                result = 0
            elif roll.isdigit():
                result = int(roll)
            else:
                raise ValueError(f'Некорректный символ в последовательности. '
                                 f'Состояние: {__class__.__name__}. Полученный символ: {roll}')

            self.context.set_state(SecondRoll())

        self.context.frame_results.append(result)


class SecondRoll(State):
    def count_score(self, roll):
        if roll == '/':
            self.context.frame_results[-1] = 15
        else:
            if roll == '-':
                result = 0
            elif roll.isdigit():
                result = int(roll)

                if self.context.frame_results[-1] + result > 10:
                    raise ValueError(f'Количество кеглей, сбитых за один фрейм, не должно быть больше 10. '
                                     f'Количество кеглей за этот фрейм: {self.context.frame_results[-1]} + {result} = '
                                     f'{self.context.frame_results[-1] + result}')
            else:
                raise ValueError(f'Некорректный символ в последовательности. '
                                 f'Состояние: {__class__.__name__}. Полученный символ: {roll}')

            self.context.frame_results[-1] += result

        self.context.set_state(FirstRoll())


def get_score(game_result):
    counter = ScoreCounter(game_result)
    return counter.get_score()


if __name__ == '__main__':
    print(get_score('Х4/34-4'))
