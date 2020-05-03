# -*- coding: utf-8 -*-

# Есть файл с протоколом регистраций пользователей на сайте - registrations.txt
# Каждая строка содержит: ИМЯ ЕМЕЙЛ ВОЗРАСТ, разделенные пробелами
# Например:
# Василий test@test.ru 27
#
# Надо проверить данные из файла, для каждой строки:
# - присутсвуют все три поля
# - поле имени содержит только буквы
# - поле емейл содержит @ и .
# - поле возраст является числом от 10 до 99
#
# В результате проверки нужно сформировать два файла
# - registrations_good.log для правильных данных, записывать строки как есть
# - registrations_bad.log для ошибочных, записывать строку и вид ошибки.
#
# Для валидации строки данных написать метод, который может выкидывать исключения:
# - НЕ присутсвуют все три поля: ValueError
# - поле имени содержит НЕ только буквы: NotNameError (кастомное исключение)
# - поле емейл НЕ содержит @ и .(точку): NotEmailError (кастомное исключение)
# - поле возраст НЕ является числом от 10 до 99: ValueError
# Вызов метода обернуть в try-except.

INPUT_RECORDS = 'registrations.txt'
VALID_RECORDS = 'registrations_good.log'
INVALID_RECORDS = 'registrations_bad.log'


# Для обоих кастомных классов хорошо подходит ValueError: поддерживаемый тип, неподдерживаемое значение
class NotEmailError(ValueError):
    def __str__(self):
        return f'must include an @ and a dot, got {self.args[0]}'


class NotNameError(ValueError):
    def __str__(self):
        return f'must only contain the letters, got {self.args[0]}'


def check_record(string):
    name, email, age = string.split()
    if not name.isalpha():
        raise NotNameError(name)
    if ('@' not in email or
            '.' not in email[email.find('@') + 1:]):
        raise NotEmailError(email)
    if int(age) not in range(10, 100):
        raise ValueError(f'invalid age (expected from 10 to 99, got {age})')


with open(INPUT_RECORDS, mode='r', encoding='utf8') as records:
    with open(VALID_RECORDS, mode='w', encoding='utf8') as valids:
        with open(INVALID_RECORDS, mode='w', encoding='utf8') as invalids:
            for line in records:
                line = line[:-1]
                try:
                    check_record(line)
                except (ValueError, NotEmailError, NotNameError) as exc:
                    print(f'{exc.__class__.__name__}: {exc}: {line}')
                    invalids.write(line + '\n')
                else:
                    valids.write(line + '\n')

