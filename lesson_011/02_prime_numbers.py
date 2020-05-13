# -*- coding: utf-8 -*-
from functools import reduce
from math import sqrt


def is_prime(number):
    for i in range(2, int(sqrt(number)) + 1):
        if number % i == 0:
            # Есть делитель? Составное!
            return False
    return True


# Есть функция генерации списка простых чисел

#  функцию генерирования простых чисел я перепишу - так будет быстрее работать
def get_prime_numbers(n):
    prime_numbers = []
    for number in range(2, n+1):
        if is_prime(number):
            prime_numbers.append(number)
    return prime_numbers

# Часть 1
# На основе алгоритма get_prime_numbers создать класс итерируемых обьектов,
# который выдает последовательность простых чисел до n
#
# Распечатать все простые числа до 10000 в столбик


class PrimeNumbers:
    def __init__(self, n):
        self.numbers_count = n
        self.last_prime = 1

    def is_prime(self, number):
        for i in range(2, int(sqrt(number)) + 1):
            if number % i == 0:
                return False
        return True

    def __iter__(self):
        self.last_prime = 1
        return self

    def __next__(self):
        for number in range(self.last_prime + 1, self.numbers_count + 1):
            if self.is_prime(number):
                self.last_prime = number
                return number
        raise StopIteration()

# prime_number_iterator = PrimeNumbers(n=10000)
# for number in prime_number_iterator:
#     print(number)


# зачет первой части

# Часть 2
# Теперь нужно создать генератор, который выдает последовательность простых чисел до n
# Распечатать все простые числа до 10000 в столбик


def prime_numbers_generator(n):
    for number in range(2, n + 1):
        if is_prime(number):
            yield number

# for number in prime_numbers_generator(n=10000):
#     print(number)


# Часть 3
# Написать несколько функций-фильтров, которые выдает True, если число:
# 1) "счастливое" в обыденном пониманиии - сумма первых цифр равна сумме последних
#       Если число имеет нечетное число цифр (например 727 или 92083),
#       то для вычисления "счастливости" брать равное количество цифр с начала и конца:
#           727 -> 7(2)7 -> 7 == 7 -> True
#           92083 -> 92(0)83 -> 9+2 == 8+3 -> True
# 2) "палиндромное" - одинаково читающееся в обоих направлениях. Например 723327 и 101
# 3) придумать свою (https://clck.ru/GB5Fc в помощь)
#
# Подумать, как можно применить функции-фильтры к полученной последовательности простых чисел
# для получения, к примеру: простых счастливых чисел, простых палиндромных чисел,
# простых счастливых палиндромных чисел и так далее. Придумать не менее 2х способов.
#
# Подсказка: возможно, нужно будет добавить параметр в итератор/генератор.
#  не совсем понимаю, зачем параметр? Передвавть в итератор/генератор функцию фильтра что ли?
# -- Именно так


def is_lucky(number):
    number = str(number)
    if len(number) < 2:
        return False
    left_half = number[:len(number) // 2]
    right_half = number[-(len(number) // 2):]
    left_sum = sum([int(digit) for digit in left_half])
    right_sum = sum([int(digit) for digit in right_half])
    return left_sum == right_sum


def is_palindrome(number):
    return str(number) == str(number)[::-1]


#  хотел сначала извиниться и отделаться каким-нибудь простым алгоритмом вроде проверки числа на квадрат
#  (находим корень от числа, а потом проверяем у него наличие дробной части с помощью math.modf),
#  но потом наткнулся на полупростые числа (https://vk.cc/atWbrH),
#  разработка алгоритма поиска которых показалась мне достаточно интересной

#  Вариант 1. В лоб. Медленно (хотя, после переписывания генератора уже не так медленно), неоптимально, но наглядно
def is_semiprime(number):
    primes = []
    for prime in prime_numbers_generator(n=number):
        primes.append(prime)
        if number / prime in primes:
            return True
    return False


#  Вариант 2. Быстрый и память не жрёт)
def is_semiprime_v2(number):
    # факторизируем число методом перебора делителей (во, какие умные слова я в википедии нашёл =D )
    factors_count = 0
    # в соответствии с методом достаточно искать до корня проверяемого числа
    for i in range(2, int(sqrt(number)) + 1):
        while number % i == 0:
            number /= i
            factors_count += 1
        if factors_count >= 2:
            break
    # Если оставшееся число больше 1, значит оно простое, потому что на остальные оно не разделилось
    if number > 1:
        factors_count += 1
    # если факторов больше или меньше двух, значит число не полупростое
    return factors_count == 2


#  способ номер 1
# # Фильтруем, на выходе получаем итератор
# lucky_semiprimes = filter(lambda x: is_lucky(x) and is_semiprime(x), range(10001))
# print(list(lucky_semiprimes))
# # Фильтруем, на выходе получаем генератор
# lucky_semiprimes_2 = (x for x in range(10001) if is_lucky(x) and is_semiprime_v2(x))
# print(list(lucky_semiprimes_2))


#  Способ номер 2: в прядке общего бреда можно поробовать применить здесь декораторы
# -- Уникальный способ, такое встретил впервые!
def filtered(func, filter_func_list):
    """
    Декоратор применяет к выводу функции func функции-фильтры из списка filter_func_list

    Parameters
    ----------
    func
        функция, вывод которой нужно отфильтровать

    filter_func_list
        список функций-фильтров, возвращающих флаги
    Returns
    -------
    Возвращает функцию, которая вовзращает отфильрованный вывод из func
    """
    if callable(filter_func_list):
        filter_func_list = [filter_func_list, ]

    def surrogate(*args, **kwargs):
        while True:
            gener = func(*args, **kwargs)
            for data in gener:
                check_data = lambda buffer, filter_func: buffer and filter_func(data)
                filter_result = reduce(check_data, filter_func_list, True)
                if filter_result:
                    yield data
            return
    return surrogate


# попробуем получить все счастливые полупростые числа в диапазоне от 5000 до 10000
lucky_semiprimes_fabric = filtered(range, [is_lucky, is_semiprime_v2])
lucky_semiprimes = lucky_semiprimes_fabric(5000, 10001)
for number in lucky_semiprimes:
    print(number)

# зачет!
