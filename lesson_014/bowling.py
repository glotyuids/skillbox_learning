class FrameCountError(Exception):
    pass


class ScoreCounter:
    _state = None
    frames_count = 10

    def __init__(self, game_result, new_rules=False):
        self.set_state(FirstRoll())
        self.game_result = game_result
        self.new_rules = new_rules

        self.frame_results = []

        # Вкратце по подсчёту очков по новым правилам:
        # мы не можем заглянуть в будущее, чтобы узнать, сколько кеглей собьёт игрок в следующих двух бросках.
        # Но мы можем сохранять на будущее множители, которые будут применяться к будущим броскам. То есть:
        # для игры «Х4/34» список сбитых кеглей будет     [10, 4, 6, 3, 4],
        # а список множителей, в соответствии с правилами [ 1, 2, 2, 2, 1]. В результате как раз и получим 40 очков.
        self.pins = []
        self.multipliers = [1, 1]

    def set_state(self, state):
        self._state = state
        self._state.context = self

    def get_score(self):
        for roll in self.game_result:
            self._state.count_score(roll)
        if len(self.frame_results) < self.frames_count:
            raise FrameCountError(f'Количество фреймов в последовательности меньше {self.frames_count}')
        return (sum(self.frame_results) if not self.new_rules
                else sum([pins * mult for pins, mult in zip(self.pins, self.multipliers)]))


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
        self.context.multipliers.append(1)
        if roll in 'XxХх':
            result = 20
            pins = 10
            self.context.multipliers[-2] += 1
            self.context.multipliers[-1] += 1
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

        self.context.multipliers.append(1)

        if roll == '/':
            self.context.frame_results[-1] = 15
            pins = 10 - self.context.pins[-1]
            self.context.multipliers[-2] += 1
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
    counter = ScoreCounter(game_result + '\0', new_rules=True)
    return counter.get_score()


if __name__ == '__main__':
    # ваше решение не обрабатывает след. неправильные для 10 фреймовой игры по 10 кеглей на фрейм данные
    input = 'Х4/34--------------'
    #input = 'X' * 9 + '55'
    print(get_score(input))
