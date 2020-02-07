# -*- coding: utf-8 -*-

# (цикл while)

# даны целые положительные числа a и b (a > b)
# Определить результат целочисленного деления a на b, с помощью цикла while,
# __НЕ__ используя ни одной из операций деления: ни деления с плавающей точкой /, ни целочисленного деления //
# и взятия остатка %
# Формат вывода:
#   Целочисленное деление ХХХ на YYY дает ZZZ

a, b = 179, 37

dividend, divisor = a, b
result = 0
while dividend > divisor:
    # TODO Хорошо! Но для случая когда числа делятся без остатка результат не верный - надо уточнить условие
    dividend -= divisor
    result += 1

print(f'Целочисленное деление {a} на {b} дает {result}')
