"""
Здесь находятся все сценарии бота.
В списке INTENTS хранятся намерения пользователей, которые будут извлекаться из сообщений по токену.
В словаре SCENARIOS хранятся сценарии: описания пошагового взаимодействия с пользователем
    в формате "вопрос-ответ" (например регистрация)
DEFAULT_ANSWER - ответ бота на случай, когда он не находит токен в интентах
"""
INTENTS = [
    {
        'name': 'Дата проведения',
        'tokens': ['когда', 'сколько', 'дата', 'дату', '1', ],
        'scenario': None,
        'answer': 'Конференция пройдёт с 15 по 18 августа 1969 года',
    },
    {
        'name': 'Место проведения',
        'tokens': ['где', 'место', 'локация', 'адрес',  'метро', '2', ],
        'scenario': None,
        'answer': 'Конференция пройдёт на ферме Макса Ясгура в городе Бетел, штат Нью-Йорк',
    },
    {
        'name': 'Регистрация',
        'tokens': ['билет', 'регист', 'добав', 'купить', '3', ],
        'scenario': 'registration',
        'answer': None,
    },
]

SCENARIOS = {
    'registration': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Чтобы зарегистрироваться, введите ваше имя. \n'
                        'На это имя вы сможете получить парковочное место, '
                        'палатку и обед в полевой кухне',
                'failure': 'Имя должно состоять из 3-30 букв и дефиса. Попробуйте ещё раз',
                'handler': 'handle_name',
                'next_step': 'step2',
            },
            'step2': {
                'text': 'Введите email. На него мы пришлём пригласительный',
                'failure': 'Во введённом адресе ошибка. Попробуйте ещё раз',
                'handler': 'handle_email',
                'next_step': 'step3',
            },
            'step3': {
                'text': 'Спасибо за регистрацию {name}. Мы отправили пригласительный на {email}. \n'
                        'Вы сможете получить его в ближайшем почтовом отделении',
                'failure': None,
                'handler': None,
                'next_step': None,
            },

        }
    }
}

DEFAULT_ANSWER = 'Я не знаю как на это ответить. \n' \
                 'Я могу рассказать когда и где пройдёт крупнейшая в мире коференция, ' \
                 'а также зарегистрировать вас'
