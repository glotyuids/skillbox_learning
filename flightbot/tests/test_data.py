from datetime import datetime
import scenarios
from unittest.mock import patch
patch.dict('os.environ', {'RAPIDAPI_KEY': 'AAA'}, clear=True).start()
import skyscanner_api as skyapi


RAW_EVENT = {
    'type': 'message_new',
    'object': {
        'message': {
            'date': 1602440563, 'from_id': 25833442, 'id': 86, 'out': 0,
            'peer_id': 25833442, 'text': 'Hello', 'conversation_message_id': 84,
            'fwd_messages': [], 'important': False, 'random_id': 0, 'attachments': [],
            'is_hidden': False
        },
        'client_info': {
            'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link'],
            'keyboard': True, 'inline_keyboard': True, 'carousel': False,
            'lang_id': 0
        }
    },
    'group_id': 197090073,
    'event_id': 'cda2978fe40bb257ba476407ad8ca57c5d3c6b08'}
ORIGIN = skyapi.Place('Москва', 'MOW', 'Россия')
DEST = skyapi.Place('Белгород', 'EGO', 'Россия')
FLIGHT = skyapi.Flight(
    price=500,
    direct=True,
    origin=ORIGIN,
    dest=DEST,
    arrival=datetime(2021, 2, 12),
    carrier='S7'
)
SEATS = '2'
COMMENT = 'Это коммент'
CONTEXT = {
    'origin': ORIGIN,
    'dest': DEST,
    'flight': FLIGHT,
    'seats': SEATS,
    'comment': COMMENT
}
STEPS = scenarios.SCENARIOS['find_flights']['steps']
INTENTS = [
    ('Привет', scenarios.INTENTS[1]['answer']),
    ('/помощь', scenarios.INTENTS[0]['answer']),
    ('вапвапв', scenarios.DEFAULT_ANSWER),
    ('/билет', STEPS['enter_arrival']['text']),
    ('/выход', scenarios.WELCOME_ANSWER),
    ]
TICKET = [
    ('/билет', STEPS['enter_arrival']['text']),
    ('/помощь', scenarios.SCENARIOS['find_flights']['help']),
    ('sdfsdfsfd', STEPS['enter_arrival']['result_1'][0]),
    ('Москва', STEPS['enter_dest']['text'].format(**CONTEXT)),
    ('sdfsdfsfd', STEPS['enter_dest']['result_1'][0]),
    ('Белгород', STEPS['enter_date']['text'].format(**CONTEXT)),
    ('sdfsdfsfd', STEPS['enter_date']['result_1'][0]),
    ('12-02-2021', STEPS['enter_seats']['text'].format(**CONTEXT)),
    ('sdfsdfsfd', STEPS['enter_seats']['result_1'][0]),
    ('100000', STEPS['enter_seats']['result_2'][0]),
    ('0', STEPS['enter_seats']['result_3'][0]),
    (SEATS, STEPS['enter_comment']['text']),
    (COMMENT, STEPS['verify_data']['text'].format(**CONTEXT)),
    ('далее', STEPS['enter_phone']['text']),
    ('sdfsdfsfd', STEPS['enter_phone']['result_1'][0]),
    ('+7 999 123 45 67', STEPS['finish']['text']),
    ('Привет', scenarios.INTENTS[1]['answer']),
]
