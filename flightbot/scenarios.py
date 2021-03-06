"""
Здесь находятся все сценарии бота.
В списке INTENTS хранятся намерения пользователей, которые будут извлекаться из сообщений по токену.
В словаре SCENARIOS хранятся сценарии: описания пошагового взаимодействия с пользователем
    в формате "вопрос-ответ" (например регистрация)
WELCOME_ANSWER - сообщение, которое бот будет высылать всем вновь подключившимся к нему
DEFAULT_ANSWER - ответ бота на случай, когда он не находит токен в интентах
HELP_ANSWER - сообщение со шпаргалкой для пользователдя

Описание структуры сценария - словаря, который добавляется в SCENARIOS:
'имя_сценария': {
    'help': str, опционально - перегружает /help при выполнении данного сценария,
    'first_step': 'имя_шага' - указывает имя шага, с которого начнётся сценарий
    steps: {
        'имя_шага': {
            'text': str - сообщение, которое будет отправлено в начале выполнения шага
            'handler': None или имя функции - имя функции, которая будет обрабатывать сообщение от пользователя
                       Если хендлер равен None, то после отправки сообщения из 'text', сценарий корректно завершится.
                       Хендлеры должны возвращать код результата. Соответственно этому коду  в шаг
                       добавляются записи вида 'result_<код>'
            'result_0': (сообщение_для_отправки, следующий_шаг)
                        Если сообщение - это строка, то следующий шаг из этой записи будет игнорироваться,
                        вместо этого повторится текущий шаг.
                        Если же сообщение равно None, то произойдёт переход на следующий шаг.
                        Какая-нибудь из этих позиций обязательно должна присутствовать,
                        Иначе бот будет падать со ScenarioResultError
        }
    }
}
"""


DEFAULT_ANSWER = 'Я не знаю как на это ответить.\n' \
                 'Для вывода помощи введите /помощь'

HELP_ANSWER = 'Для поиска рейса введите /билет\n' \
              'Для вывода помощи (этого сообщения) - /помощь'

WELCOME_ANSWER = 'Здесь вы можете найти удобный для вас авиарейс.\n' + HELP_ANSWER


INTENTS = [
    {
        'name': 'Помощь',
        'tokens': ['помог', 'помощь', '/помощь'],
        'scenario': None,
        'answer': HELP_ANSWER,
    },
    {
        'name': 'Приветствие',
        'tokens': ['привет', 'здравствуй', ],
        'scenario': None,
        'answer': WELCOME_ANSWER,
    },
    {
        'name': 'Регистрация',
        'tokens': ['билет', '/билет', 'купить', ],
        'scenario': 'find_flights',
        'answer': None,
    },
]

SCENARIOS = {
    'find_flights': {
        'help': 'Для поиска рейса введите /ticket\n'
                'Для вывода помощи (этого сообщения) - /help\n'
                'Если хотите выйти - /выход',
        'first_step': 'enter_arrival',
        'steps': {
            'enter_arrival': {
                'text': 'Давайте попробуем найти ваш рейс.\nВведите город отправления',
                'result_0': (None, 'enter_dest'),
                'result_1': ('Город не найден. Попробуйте ещё раз или отправьте /выход для выхода', None),
                'handler': 'handle_origin_city',
            },
            'enter_dest': {
                'text': 'Город вылета {origin.name}, {origin.country}.\n'
                        'Теперь укажите, в какой город вы хотите полететь',
                'result_0': (None, 'enter_date'),
                'result_1': ('Город не найден. Попробуйте ещё раз или отправьте /выход для выхода', None),
                'handler': 'handle_dest_city',
            },
            'enter_date': {
                'text': 'Город прибытия {dest.name}, {dest.country}. Отличный выбор!\n'
                        'А теперь введите желаемую дату вылета в формате ДД-ММ-ГГГГ, например 18-03-2021',
                'handler': 'handle_arrival_date',
                'result_0': (None, 'enter_seats'),
                'result_1': ('Некорректный формат даты. попробуйте ещё раз или отправьте /выход для выхода', None),
                'result_2': ('На выбранную вами дату рейсов нет.\n'
                             'Вот список ближайших дат в этом месяце:\n'
                             '{dates}'
                             '\nВыберите из них наиболее удобную.\n'
                             'Если предложенные даты вам не подходят, то попродуйте выбрать '
                             'другой месяц, либо отправьте /выход для выхода',
                             None),
                'result_3': ('К сожалению, в этом месяце подходящих для вас рейсов нет.\n'
                             'Попробуйте выбрать другой месяц или отправьте /выход для выхода', None)
            },
            'enter_seats': {
                'text': 'На эту дату есть рейс {flight.origin.name} - {flight.dest.name}\n '
                        'авиакомпании {flight.carrier}.\n'
                        'Минимальная стоимость билета составит {flight.price}₽\n'
                        'Введите количество мест, которое вы хотите забронировать',
                'result_0': (None, 'enter_comment'),
                'result_1': ('Вы ввели не число. Попробуйте ещё раз или отправьте /выход для выхода', None),
                'result_2': ('Вы выбрали больше мест, чем достумно в самолёте. '
                             'Попробуйте ещё раз или отправьте /выход для выхода',
                             None),
                'result_3': ('Вы выбрали меньше, чем одно место. '
                             'Попробуйте ещё раз или отправьте /выход для выхода',
                             None),
                'handler': 'seats_handler',
            },
            'enter_comment': {
                'text': 'Вы можете добавить комментарий к заказу.\n'
                        'Если не хотите, то отправьте прочерк (без кавычек) - "-"',
                'handler': 'comment_handler',
                'result_0': (None, 'verify_data'),
            },
            'verify_data': {
                'text': 'Проверьте данные вашего рейса:\n'
                        'рейс {flight.origin.name} - {flight.dest.name}\n'
                        'авиакомпания {flight.carrier}\n'
                        'дата вылета {flight.arrival_date}\n'
                        'количество мест: {seats}\n'
                        'ваш комментарий: "{comment}"\n\n'
                        'Если всё верно, то отправьте "далее",\n'
                        ' - хотите поменять город вылета - "вылет"\n'
                        ' - поменять город прибытия - "прилёт"\n'
                        ' - изменить дату вылета - "дата"\n'
                        ' - поменять количество мест - "места"\n'
                        ' - ввести новый комментарий - "коммент"\n',
                'result_0': (None, 'enter_phone'),
                'result_1': ('Я не понял вашего ответа. Введите "да" или "нет", либо отправьте /выход для выхода',
                             None),
                'result_2': (None, 'edit_arrival'),
                'result_3': (None, 'edit_dest'),
                'result_4': (None, 'edit_date'),
                'result_5': (None, 'edit_seats'),
                'result_6': (None, 'enter_comment'),
                'handler': 'verify_data_handler',
            },
            'enter_phone': {
                'text': 'Введите номер телефона в формате +7 999 123 45 67\n'
                        'По этому номеру с вами свяжется наш оператор для уточнения деталей заказа',
                'result_0': (None, 'finish'),
                'result_1': ('Некорректный формат номера. Введите номер в формате +7 999 123 45 67',
                             None),
                'handler': 'phone_handler',
            },
            'finish': {
                'text': 'Благодарим за то, что выбрали нас!\n'
                        'В течение часа мы вам позвоним для уточнения деталей заказа.\n'
                        'Всего доброго!',
                'handler': None,
            },

            'edit_arrival': {
                'text': 'Давайте попробуем заменить город отправления.\nВведите его',
                'result_0': (None, 'verify_data'),
                'result_1': ('Город не найден. Попробуйте ещё раз или отправьте /выход для выхода', None),
                'result_2': (None, 'edit_date_after_city'),
                'handler': 'handle_edit_origin_city',
            },
            'edit_dest': {
                'text': 'Давайте попробуем заменить город прибытия.\nВведите его',
                'result_0': (None, 'verify_data'),
                'result_1': ('Город не найден. Попробуйте ещё раз или отправьте /выход для выхода', None),
                'result_2': (None, 'edit_date_after_city'),
                'handler': 'handle_edit_dest_city',
            },
            'edit_date': {
                'text': 'Введите желаемую дату вылета в формате ДД-ММ-ГГГГ, например 18-03-2021',
                'handler': 'handle_arrival_date',
                'result_0': (None, 'verify_data'),
                'result_1': ('Некорректный формат даты. попробуйте ещё раз или отправьте /выход для выхода', None),
                'result_2': ('На выбранную вами дату рейсов нет.\n'
                             'Вот список ближайших дат в этом месяце:\n'
                             '{dates}'
                             '\nВыберите из них наиболее удобную.\n'
                             'Если предложенные даты вам не подходят, то попродуйте выбрать '
                             'другой месяц, либо отправьте /выход для выхода',
                             None),
                'result_3': ('К сожалению, в этом месяце подходящих для вас рейсов нет.\n'
                             'Попробуйте выбрать другой месяц или отправьте /выход для выхода', None)
            },
            'edit_date_after_city': {
                'text': 'К сожалению, на выбранную вами дату рейса между\n'
                        '{origin.name} и {dest.name} нет.\n'
                        'Попробуйте ввести другую дату вылета в формате ДД-ММ-ГГГГ, например 18-03-2021',
                'handler': 'handle_arrival_date',
                'result_0': (None, 'verify_data'),
                'result_1': ('Некорректный формат даты. попробуйте ещё раз или отправьте /выход для выхода', None),
                'result_2': ('На выбранную вами дату рейсов нет.\n'
                             'Вот список ближайших дат в этом месяце:\n'
                             '{dates}'
                             '\nВыберите из них наиболее удобную.\n'
                             'Если предложенные даты вам не подходят, то попродуйте выбрать '
                             'другой месяц, либо отправьте /выход для выхода',
                             None),
                'result_3': ('К сожалению, в этом месяце подходящих для вас рейсов нет.\n'
                             'Попробуйте выбрать другой месяц или отправьте /выход для выхода', None)
            },
            'edit_seats': {
                'text': 'Введите количество мест, которое вы хотите забронировать',
                'result_0': (None, 'verify_data'),
                'result_1': ('Вы ввели не число. Попробуйте ещё раз или отправьте /выход для выхода', None),
                'result_2': ('Вы выбрали больше мест, чем достумно в самолёте. '
                             'Попробуйте ещё раз или отправьте /выход для выхода',
                             None),
                'result_3': ('Вы выбрали меньше, чем одно место. '
                             'Попробуйте ещё раз или отправьте /выход для выхода',
                             None),
                'handler': 'seats_handler',
            },
        }
    }
}

