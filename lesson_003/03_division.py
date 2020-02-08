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

if divisor == 0:
    print('Делить на ноль нельзя')
    quit()

negative_result = False
negative_result = not negative_result if dividend < 0 else negative_result
negative_result = not negative_result if divisor < 0 else negative_result

result = 0
dividend, divisor = abs(dividend), abs(divisor)
while dividend >= divisor:
    # Хорошо! Но для случая когда числа делятся без остатка результат не верный - надо уточнить условие
    #  Не подумал( Поправил условие. Попутно обработал ноль и отрицательные числа
    dividend -= divisor
    result += 1
result = -result if negative_result else result

print(f'Целочисленное деление {a} на {b} дает {result}')

# зачет! Удивили! С такой основательностью в 3м модуле эту задачу ещё никто не решал! Хорошее качество для программиста.
# Единственное - согласно ТЗ числа положительные.
