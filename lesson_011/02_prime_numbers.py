# -*- coding: utf-8 -*-


# Есть функция генерации списка простых чисел


def get_prime_numbers(n):
    prime_numbers = []
    for number in range(2, n+1):
        for prime in prime_numbers:
            if number % prime == 0:
                break
        else:
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
        self.prime_numbers = []
        self.last_prime = 1

    def __iter__(self):
        self.prime_numbers = []
        self.last_prime = 1
        return self

    def __next__(self):
        for number in range(self.last_prime + 1, self.numbers_count + 1):
            for prime in self.prime_numbers:
                if number % prime == 0:
                    break
            else:
                self.prime_numbers.append(number)
                self.last_prime = number
                return number
        raise StopIteration()


# prime_number_iterator = PrimeNumbers(n=10000)
# for number in prime_number_iterator:
#     print(number)


# TODO после подтверждения части 1 преподователем, можно делать
# Часть 2
# Теперь нужно создать генератор, который выдает последовательность простых чисел до n
# Распечатать все простые числа до 10000 в столбик


def prime_numbers_generator(n):
    prime_numbers = []
    for number in range(2, n + 1):
        for prime in prime_numbers:
            if number % prime == 0:
                break
        else:
            prime_numbers.append(number)
            yield number
    return prime_numbers


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


def is_lucky(number):
    number = str(number)
    left_half = number[:len(number) // 2]
    right_half = number[-(len(number) // 2):]
    left_sum = sum([int(digit) for digit in left_half])
    right_sum = sum([int(digit) for digit in right_half])
    return left_sum == right_sum


def is_palindrome(number):
    return str(number) == str(number)[::-1]


# TODO хотел сначала извиниться и отделаться каким-нибудь простым алгоритмом вроде проверки числа на квадрат
#  (находим корень от числа, а потом проверяем у него наличие дробной части с помощью math.modf),
#  но потом наткнулся на полупростые числа (https://vk.cc/atWbrH),
#  разработка алгоритма поиска которых показалась мне простой, но интересной
def is_semiprime(number):
    primes = []
    for prime in prime_numbers_generator(n=number):
        primes.append(prime)
        if number / prime in primes:
            return True
    return False


print(is_lucky(92083))
print(is_palindrome(92028))
print(is_semiprime(920))
