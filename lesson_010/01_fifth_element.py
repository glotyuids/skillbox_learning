# -*- coding: utf-8 -*-

# Умножить константу BRUCE_WILLIS на пятый элемент строки, введенный пользователем

BRUCE_WILLIS = 42


# TODO подобную конструкцию я использовал для утаскивания данных с сетевых ресурсов или из последовательного порта
#  для того, чтобы скрипт не падал, а ждал когда сервер или устройство станут доступны
correct_input = False
while not correct_input:
    input_data = input('Если хочешь что-нибудь сделать, сделай это сам: ')
    try:
        leeloo = int(input_data[4])
    except IndexError as exc:
        print(f'Нужно ввести не меньше 5 символов. Вы ввели {len(input_data)} символов')
    except ValueError as exc:
        print(f'Пятым символом должна быть цифра. У вас это "{input_data[4]}"')
    except BaseException as exc:
        print('Неожиданная ошибка', exc.__class__.__name__)
        print(exc)
    else:
        result = BRUCE_WILLIS * leeloo
        print(f"- Leeloo Dallas! Multi-pass № {result}!")
        correct_input = True

print('Всего доброго!')


# Ообернуть код и обработать исключительные ситуации для произвольных входных параметров
# - ValueError - невозможно преобразовать к числу
# - IndexError - выход за границы списка
# - остальные исключения
# для каждого типа исключений написать на консоль соотв. сообщение




